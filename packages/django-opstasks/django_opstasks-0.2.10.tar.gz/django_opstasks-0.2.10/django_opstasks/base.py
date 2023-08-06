from time import time, strftime, localtime
from pytz import utc, timezone
from json import dumps
from celery import Task
from logging import getLogger
from django.conf import settings
from redis import ConnectionPool, Redis
from django_opstasks.models import TaskResult
from django_opstasks.common.notifications import EnterpriseWeXinAgent


LOGGER = getLogger('django')
CONSUL_CONFIGS = settings.CONSUL_CONFIGS
CONSUL_SECRETS = settings.CONSUL_SECRETS

REDIS_CONNECTION_POOL = ConnectionPool(
    host=CONSUL_CONFIGS.get('REDIS_HOST', 'opstasks-redis.devops.svc.cluster.local'),
    port=CONSUL_CONFIGS.get('REDIS_PORT', 6379),
    db=CONSUL_CONFIGS.get('REDIS_RECORD_DB', 2)
)
REDIS_RECORD_TTL = CONSUL_CONFIGS.get('REDIS_RECORD_TTL', 5184000)


def record_start_datetime(func):
    """
    Decorator: record task start time
    """
    def _inner(*args, **kwargs):
        date_start_timestamp = time()
        date = strftime('%Y-%m-%d', localtime(date_start_timestamp))
        _result = func(*args, **kwargs)
        task_id = _result.task_id
        _data = dumps({"date_start": date_start_timestamp, "task_id": task_id})
        redis_connection = Redis(connection_pool=REDIS_CONNECTION_POOL)
        redis_connection.set(f'{date}/{task_id}', _data, ex=REDIS_RECORD_TTL)
        return _result
    return _inner


class CustomTask(Task):
    """ Custom Base Task
    """

    def run(self, *args, **kwargs):
        """The body of the task executed by workers."""
        raise NotImplementedError('Tasks must define the run method.')

    @record_start_datetime
    def apply(self, args=None, kwargs=None,
              link=None, link_error=None, task_id=None, retries=None,
              throw=None, logfile=None, loglevel=None, headers=None, **options):
        """
        Execute this task locally, by blocking until the task returns.

          Arguments:
            args (Tuple): positional arguments passed on to the task.
            kwargs (Dict): keyword arguments passed on to the task.
            throw (bool): Re-raise task exceptions.
                Defaults to the :setting:`task_eager_propagates` setting.

          Returns:
            celery.result.EagerResult: pre-evaluated result.
        """
        LOGGER.warning("task should not be started in apply, forward to apply_async")
        return super().apply_async(
            args=args, kwargs=kwargs, task_id=task_id,
            link=link, link_error=link_error, **options)

    @record_start_datetime
    def apply_async(self, args=None, kwargs=None, task_id=None,
                    producer=None, link=None, link_error=None, shadow=None, **options):
        """Apply tasks asynchronously by sending a message.

        Arguments:
            args (Tuple): The positional arguments to pass on to the task.

            kwargs (Dict): The keyword arguments to pass on to the task.

            countdown (float): Number of seconds into the future that the
                task should execute.  Defaults to immediate execution.

            eta (~datetime.datetime): Absolute time and date of when the task
                should be executed.  May not be specified if `countdown`
                is also supplied.

            expires (float, ~datetime.datetime): Datetime or
                seconds in the future for the task should expire.
                The task won't be executed after the expiration time.

            shadow (str): Override task name used in logs/monitoring.
                Default is retrieved from :meth:`shadow_name`.

            connection (kombu.Connection): Re-use existing broker connection
                instead of acquiring one from the connection pool.

            retry (bool): If enabled sending of the task message will be
                retried in the event of connection loss or failure.
                Default is taken from the :setting:`task_publish_retry`
                setting.  Note that you need to handle the
                producer/connection manually for this to work.

            retry_policy (Mapping): Override the retry policy used.
                See the :setting:`task_publish_retry_policy` setting.

            queue (str, kombu.Queue): The queue to route the task to.
                This must be a key present in :setting:`task_queues`, or
                :setting:`task_create_missing_queues` must be
                enabled.  See :ref:`guide-routing` for more
                information.

            exchange (str, kombu.Exchange): Named custom exchange to send the
                task to.  Usually not used in combination with the ``queue``
                argument.

            routing_key (str): Custom routing key used to route the task to a
                worker server.  If in combination with a ``queue`` argument
                only used to specify custom routing keys to topic exchanges.

            priority (int): The task priority, a number between 0 and 9.
                Defaults to the :attr:`priority` attribute.

            serializer (str): Serialization method to use.
                Can be `pickle`, `json`, `yaml`, `msgpack` or any custom
                serialization method that's been registered
                with :mod:`kombu.serialization.registry`.
                Defaults to the :attr:`serializer` attribute.

            compression (str): Optional compression method
                to use.  Can be one of ``zlib``, ``bzip2``,
                or any custom compression methods registered with
                :func:`kombu.compression.register`.
                Defaults to the :setting:`task_compression` setting.

            link (Signature): A single, or a list of tasks signatures
                to apply if the task returns successfully.

            link_error (Signature): A single, or a list of task signatures
                to apply if an error occurs while executing the task.

            producer (kombu.Producer): custom producer to use when publishing
                the task.

            add_to_parent (bool): If set to True (default) and the task
                is applied while executing another task, then the result
                will be appended to the parent tasks ``request.children``
                attribute.  Trailing can also be disabled by default using the
                :attr:`trail` attribute

            publisher (kombu.Producer): Deprecated alias to ``producer``.

            headers (Dict): Message headers to be included in the message.

        Returns:
            celery.result.AsyncResult: Promise of future evaluation.

        Raises:
            TypeError: If not enough arguments are passed, or too many
                arguments are passed.  Note that signature checks may
                be disabled by specifying ``@task(typing=False)``.
            kombu.exceptions.OperationalError: If a connection to the
               transport cannot be made, or if the connection is lost.

        Note:
            Also supports all keyword arguments supported by
            :meth:`kombu.Producer.publish`.
        """
        return super().apply_async(
            args=args, kwargs=kwargs, task_id=task_id,
            producer=producer, link=link, link_error=link_error, shadow=shadow, **options)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        snoopy = EnterpriseWeXinAgent(
            CONSUL_CONFIGS.get('SNOOPY_CORPID', '110844d972c62d9'),
            CONSUL_CONFIGS.get('SNOOPY_AGENT_ID', '0000002'),
            CONSUL_SECRETS.get('SNOOPY_CORPSECRET', 'bT2XAXzTiPadNw')
        )
        result = TaskResult.objects.filter(task_id=task_id, ).first()
        # Convert utc datetime to local strftime
        utc_to_local_strftime = lambda utc_datetime: utc_datetime.replace(
            tzinfo=utc).astimezone(timezone(settings.TIME_ZONE)).strftime("%Y-%m-%d %H:%M:%S")
        message = dumps({
            "task_name": result.task_name,
            "date_created": utc_to_local_strftime(result.date_created),
            "task_id": task_id,
        })
        send_to = CONSUL_SECRETS.get('TASK_FAILURE_SENDTO', 'huaxingliu@yangqianguan.com')
        snoopy.error(send_to=send_to, message=message)

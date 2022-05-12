import backoff
import pika
from pika import BlockingConnection
from pika.exceptions import AMQPConnectionError

from workers.event_listeners.core.config import settings


@backoff.on_exception(
    wait_gen=backoff.expo,
    exception=(RuntimeError, TimeoutError, AMQPConnectionError),
    max_time=settings.max_backoff,
)
def rabbit_conn_consume() -> BlockingConnection:
    credentials = pika.PlainCredentials(
        username=settings.r_name, password=settings.r_password
    )
    parameters = pika.ConnectionParameters(
        host=settings.r_host, credentials=credentials, virtual_host="/vhost1"
    )

    connection_rabbit = pika.BlockingConnection(parameters)
    return connection_rabbit

import backoff
import pika
from pika import BlockingConnection
from pika.exceptions import AMQPConnectionError

from ..core.config import settings


@backoff.on_exception(
    wait_gen=backoff.expo,
    exception=(RuntimeError, TimeoutError, AMQPConnectionError),
    max_time=settings.backoff_timeout,
)
def rabbit_conn_consume() -> BlockingConnection:
    credentials = pika.PlainCredentials(
        username=settings.rabbit.name, password=settings.rabbit.password
    )
    parameters = pika.ConnectionParameters(
        host=settings.rabbit.host, credentials=credentials, virtual_host="/vhost1"
    )

    connection_rabbit = pika.BlockingConnection(parameters)
    return connection_rabbit

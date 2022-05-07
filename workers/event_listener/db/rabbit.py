import backoff
import pika
from pika.exceptions import AMQPConnectionError

from workers.event_listener.core.config import settings


@backoff.on_exception(
    wait_gen=backoff.expo,
    exception=(RuntimeError, TimeoutError, AMQPConnectionError),
    max_time=30,
)
def rabbit_conn():
    credentials = pika.PlainCredentials(
        username=settings.r_name, password=settings.r_password
    )
    parameters = pika.ConnectionParameters(
        host=settings.r_host, credentials=credentials, virtual_host="/vhost1"
    )

    connection_rabbit = pika.BlockingConnection(parameters)
    return connection_rabbit
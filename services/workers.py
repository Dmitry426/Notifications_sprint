__all__ = ["producer", "consumer", "consumer"]

import backoff
import pika

from pika.exceptions import AMQPConnectionError
from Configs import config
from Configs.logger_notifications import logger

R_HOST = config.settings.r_host
R_NAME = config.settings.r_name
R_PASSWORD = config.settings.r_password


@backoff.on_exception(
    wait_gen=backoff.expo,
    exception=(RuntimeError, TimeoutError, AMQPConnectionError),
    max_time=30,
)
def rabbit_conn():
    logger.info("\n\n --20--\n\n")
    credentials = pika.PlainCredentials(
        username=R_NAME, password=R_PASSWORD
    )
    logger.info("\n\n --24--\n\n")
    parameters = pika.ConnectionParameters(
        host=R_HOST, credentials=credentials, virtual_host="/vhost1"
    )
    logger.info("\n\n --28--\n\n")
    connection_rabbit = pika.BlockingConnection(parameters)
    logger.info("\n\n --30--\n\n")
    return connection_rabbit


def producer(body, queue, exchange=''):
    logger.info("\n\n --36--\n\n")
    channel = rabbit_conn().channel()
    logger.info("\n\n --38--\n\n")
    channel.basic_publish(exchange=exchange,
                          routing_key=queue,
                          body=body,
                          properties=pika.BasicProperties(
                              delivery_mode=2,  # make message persistent
                          )
                          )
    logger.info("\n\n [x] Данные отправлены\n\n")
    rabbit_conn().close()


def consumer(queue, callback):
    logger.info('\n\n---52---\n\n')
    channel = rabbit_conn().channel()
    logger.info(' [*] Waiting for messages. To exit press CTRL+C')
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue,
                          on_message_callback=callback,
                          )
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    finally:
        rabbit_conn().close()

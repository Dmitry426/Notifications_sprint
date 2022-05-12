__all__ = ["producer", "consumer", "consumer"]

import os
import backoff
import pika

from pika.exceptions import AMQPConnectionError

R_NAME = os.getenv('R_NAME')
R_PASSWORD = os.getenv('R_PASSWORD')
R_HOST = os.getenv('R_HOST')


@backoff.on_exception(
    wait_gen=backoff.expo,
    exception=(RuntimeError, TimeoutError, AMQPConnectionError),
    max_time=30,
)
def rabbit_conn():
    credentials = pika.PlainCredentials(
        username=R_NAME, password=R_PASSWORD
    )
    parameters = pika.ConnectionParameters(
        host=R_HOST, credentials=credentials, virtual_host="/vhost1"
    )
    connection_rabbit = pika.BlockingConnection(parameters)
    return connection_rabbit


def producer(body, queue):
    channel = rabbit_conn().channel()
    channel.basic_publish(exchange='',
                          routing_key=queue,
                          body=body,
                          properties=pika.BasicProperties(
                              delivery_mode=2,  # make message persistent
                          )
                          )
    # print("\n\n [x] Данные отправлены\n\n")
    rabbit_conn().close()


def consumer(queue, callback):
    channel = rabbit_conn().channel()
    # print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue,
                          on_message_callback=callback,
                          # auto_ack=True)
                          # auto_ack=False)
                          )
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    finally:
        rabbit_conn().close()

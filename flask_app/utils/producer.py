__all__ = ["producer", "consumer"]

import os
# import backoff
import pika
import functools

from pika.exceptions import AMQPConnectionError

#from workers.event_listener.core.logger import get_logger

#logger = get_logger(__name__)

# R_NAME = os.getenv('R_NAME')
# R_PASSOWRD = os.getenv('R_PASSOWRD')
# R_HOST = os.getenv('R_HOST')

R_HOST="localhost"
R_NAME="user1"
R_PASSOWRD="pass1"


# @backoff.on_exception(
#     wait_gen=backoff.expo,
#     exception=(RuntimeError, TimeoutError, AMQPConnectionError),
#     max_time=30,
# )
def rabbit_conn():
    credentials = pika.PlainCredentials(
        username=R_NAME, password=R_PASSOWRD
    )
    parameters = pika.ConnectionParameters(
        host=R_HOST, credentials=credentials, virtual_host="/vhost1"
    )

    connection_rabbit = pika.BlockingConnection(parameters)
    print('\nconnect\n')
    return connection_rabbit


def producer(body):
    print('\n--37++\n')
    channel = rabbit_conn().channel()
    print('\n--39++\n')
    # channel.queue_declare(queue='auth_notification')
    print('\n--41++\n')
    channel.basic_publish(exchange='',
                          routing_key='auth_notification',
                          body=body)
    print("\n\n [x] Sent 'Hello World!'\n\n")

    rabbit_conn().close()


def on_message(chan, method_frame, header_frame, body, userdata=None):
    # """Called when a message is received. Log message and ack it."""
    # logger.info(
    #     "Delivery properties: %s, message metadata: %s", method_frame, header_frame
    # )
    # logger.info("Userdata: %s, message body: %s", userdata, body)
    chan.basic_ack(delivery_tag=method_frame.delivery_tag)


def consumer(queue):
    print('\n--65++\n')
    channel = rabbit_conn().channel()
    print('\n--67++\n')

    # on_message_callback = functools.partial(on_message, userdata="on_message_userdata")
    print('\n--70++\n')
    # channel.basic_consume(queue, on_message_callback)

    print(' [*] Waiting for messages. To exit press CTRL+C')

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % (body,))

    on_message_callback = functools.partial(on_message, userdata="on_message_userdata")


    channel.basic_consume(queue=queue,
                          on_message_callback=on_message_callback,
                          auto_ack=True)

    print('\n--73++\n')

    try:
        channel.start_consuming()
        print('\n--77++\n')
    except KeyboardInterrupt:
        print('\n--79++\n')
        channel.stop_consuming()
    finally:
        print('\n--82++\n')
        rabbit_conn().close()
    print('\n--84++\n')


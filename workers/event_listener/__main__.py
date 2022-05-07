import functools

from workers.event_listener.core.logger import get_logger
from workers.event_listener.db.rabbit import rabbit_conn

logger = get_logger(__name__)


def on_message(chan, method_frame, header_frame, body, userdata=None):
    """Called when a message is received. Log message and ack it."""
    logger.info(
        "Delivery properties: %s, message metadata: %s", method_frame, header_frame
    )
    logger.info("Userdata: %s, message body: %s", userdata, body)
    chan.basic_ack(delivery_tag=method_frame.delivery_tag)


def main():
    """Main method."""
    channel = rabbit_conn().channel()
    on_message_callback = functools.partial(on_message, userdata="on_message_userdata")
    channel.basic_consume("auth_notification", on_message_callback)

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    finally:
        rabbit_conn().close()


if __name__ == "__main__":
    main()

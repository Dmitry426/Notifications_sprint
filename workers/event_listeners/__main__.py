import argparse

from workers.event_listeners.auth_service import ConsumerAuth
from workers.event_listeners.db.postgres import postgres_connect
from workers.event_listeners.db.rabbit import rabbit_conn_consume
from workers.event_listeners.ugc_service import ConsumerUgc
from workers.event_listeners.websocket import ConsumerUgcWebsock


def auth_service():
    """Main method."""
    consumer = ConsumerAuth(
        write_connection=rabbit_conn_consume(), read_connection=rabbit_conn_consume()
    )
    consumer.start_auth()


def ugc_service():
    """Main method."""
    consumer = ConsumerUgc(
        write_connection=rabbit_conn_consume(), read_connection=rabbit_conn_consume()
    )
    consumer.start_ugc()


def ugc_service_websock():
    """Main method."""
    consumer = ConsumerUgcWebsock(
        read_connection=rabbit_conn_consume(), postgres_connection=postgres_connect
    )
    consumer.start_ugc()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--queue", choices=("auth", "ugc", "ugc_websocket"))
    args = parser.parse_args()
    if args.queue == "auth":
        auth_service()
    if args.queue == "ugc":
        ugc_service()
    if args.queue == "ugc_websocket":
        ugc_service_websock()

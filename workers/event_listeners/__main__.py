from workers.event_listener.auth_service import ConsumerAuth
from workers.event_listener.db.rabbit import rabbit_conn_consume
import argparse

from workers.event_listener.ugc_service import ConsumerUgc


def auth_service():
    """Main method."""
    consumer = ConsumerAuth(write_connection=rabbit_conn_consume(),
                            read_connection=rabbit_conn_consume())
    consumer.start_auth()


def ugc_service():
    """Main method."""
    consumer = ConsumerUgc(write_connection=rabbit_conn_consume(),
                           read_connection=rabbit_conn_consume())
    consumer.start_ugc()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--queue", choices=('auth', 'ugc'))
    args = parser.parse_args()
    if args.queue == "auth":
        auth_service()
    if args.queue == "ugc":
        ugc_service()

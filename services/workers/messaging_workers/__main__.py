import argparse
from logging import config as logging_config

from .core.logger import LOGGING
from .db.rabbit import rabbit_conn_consume
from .worker_mail import WorkerMail
from .worker_websocket import websocket_server

logging_config.dictConfig(LOGGING)


def mail_service():
    """Main method."""
    consumer = WorkerMail(read_connection=rabbit_conn_consume())
    consumer.start_mailing()


def websocket_service():
    """Main method."""
    websocket_server()


if __name__ == "__main__":
    types = {
        "mail": mail_service,
        "websocket": websocket_service,
    }

    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--type", choices=types.keys(), required=True)
    args = parser.parse_args()
    types[args.type]()

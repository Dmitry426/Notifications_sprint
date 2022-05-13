import argparse

from workers.messaging_workers.db.rabbit import rabbit_conn_consume
from workers.messaging_workers.worker_mail import WorkerMail
from workers.messaging_workers.worker_websocket import websocket_server


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

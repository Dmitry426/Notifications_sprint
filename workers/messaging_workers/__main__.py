import argparse

from workers.messaging_workers.db.rabbit import rabbit_conn_consume
from workers.messaging_workers.worker_mail import WorkerMail
from workers.messaging_workers.worker_websocket import websocket_server


def mail_service():
    """Main method."""
    consumer = WorkerMail(read_connection=rabbit_conn_consume())
    consumer.start_mailing()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", choices=("mail", "websocket"))
    args = parser.parse_args()
    if args.type == "mail":
        mail_service()
    if args.type == "websocket":
        websocket_server()

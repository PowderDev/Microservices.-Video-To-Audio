import pika, sys, os, time, logging
from send import email

logging.basicConfig(level=logging.INFO)


def main():
    logging.info("Starting notification service...")
    q_conn = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
    channel = q_conn.channel()

    def callback(ch, method, properties, body):
        print(f"Received {body}")
        err = email.notification(body)

        if err:
            ch.basic_nack(delivery_tag=method.delivery_tag)
            logging.error(f"Error: {err}")
        else:
            ch.basic_ack(delivery_tag=method.delivery_tag)
            logging.info(f"Done {body}")

    channel.basic_consume(queue="output", on_message_callback=callback)

    logging.info("Waiting for messages...")

    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Exiting...")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

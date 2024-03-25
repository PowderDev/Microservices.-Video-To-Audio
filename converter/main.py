import pika, sys, os, time
from pymongo import MongoClient
import gridfs
from convert import to_mp3


def main():
    client = MongoClient("mongodb", 27017)
    db_input = client.input
    db_output = client.output

    fs_input = gridfs.GridFS(db_input)
    fs_output = gridfs.GridFS(db_output)

    q_conn = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
    channel = q_conn.channel()

    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")
        input_fid, err = to_mp3.start(body, fs_input, fs_output, ch)
        if err:
            ch.basic_nack(delivery_tag=method.delivery_tag)
            print(f" [x] Error: {err}")
        else:
            ch.basic_ack(delivery_tag=method.delivery_tag)
            print(f" [x] Done {input_fid}")

    channel.basic_consume(queue="input", on_message_callback=callback)

    print("Waiting for messages...")

    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(" [x] Exiting...")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

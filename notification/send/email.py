import smtplib, os, json, logging
from email.message import EmailMessage


def notification(qMsg):
    try:
        qMessage = json.loads(qMsg)

        output_fid = qMessage["output_fid"]
        receiver_address = qMessage["username"]

        sender_address = os.environ.get("SENDER_ADDRESS")
        sender_password = os.environ.get("SENDER_PASSWORD")
        hostname = os.environ.get("HOSTNAME")

        msg = EmailMessage()

        msg["Subject"] = "Your conversion from video to audio is ready!"
        msg["From"] = sender_address
        msg["To"] = receiver_address
        msg.set_content(
            f"Your file is ready for download: http://{hostname}/download/{output_fid}"
        )

        logging.info("HERE")
        s = smtplib.SMTP("smtp.yandex.com", 587)
        logging.info("HERE 2")
        s.starttls()
        logging.info("HERE 3")
        s.login(sender_address, sender_password)
        logging.info("HERE 4")
        s.send_message(msg)
        logging.info("HERE 5")
        s.quit()

        return None

    except Exception as e:
        return e

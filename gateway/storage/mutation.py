import pika, json


def upload(f, fs, channel, access):
    try:
        fid = fs.put(f, filename=f.filename)
    except Exception as e:
        print(e)
        return None, ("Internal server error", 500)

    message = {
        "input_fid": str(fid),
        "output_fid": None,
        "username": access["username"],
    }

    try:
        channel.basic_publish(
            exchange="",
            routing_key="input",
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )
    except Exception as e:
        print(e)
        fs.delete(fid)
        return None, ("Internal server error", 500)

    return str(fid), None

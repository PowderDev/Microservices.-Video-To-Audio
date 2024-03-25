import pika, json, tempfile, os
from bson.objectid import ObjectId
import moviepy.editor as mp


def start(message, fs_input, fs_output, ch):
    message = json.loads(message)

    out = fs_input.get(ObjectId(message["input_fid"]))

    tf = tempfile.NamedTemporaryFile()
    tf.write(out.read())

    audio = mp.VideoFileClip(tf.name).audio

    tf.close()

    tf_path = tempfile.gettempdir() + f"/{message['input_fid']}.mp3"
    audio.write_audiofile(tf_path)

    with open(tf_path, "rb") as f:
        output_fid = fs_output.put(
            f, filename=f"{message['input_fid']}.mp3", input_fid=message["input_fid"]
        )
        message["output_fid"] = str(output_fid)

    os.remove(tf_path)

    try:
        ch.basic_publish(
            exchange="",
            routing_key="output",
            body=json.dumps(message),
            properties=pika.BasicProperties(delivery_mode=2),
        )
        return message["input_fid"], None
    except Exception as e:
        fs_output.delete(output_fid)
        return None, e

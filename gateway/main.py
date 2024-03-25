import os, gridfs, pika, json
from flask import Flask, request, send_file, render_template
from flask_pymongo import PyMongo
from auth import access
from storage import mutation
from bson.objectid import ObjectId

app = Flask(__name__)

mongo_output = PyMongo(app, uri=os.getenv("MONGO_URI") + "/output")
mongo_input = PyMongo(app, uri=os.getenv("MONGO_URI") + "/input")

fs_output = gridfs.GridFS(mongo_output.db)
fs_input = gridfs.GridFS(mongo_input.db)

q_conn = pika.BlockingConnection(
    pika.ConnectionParameters(
        host="rabbitmq",
        connection_attempts=12,
        retry_delay=5,
        blocked_connection_timeout=None,
        heartbeat=0,
    )
)
channel = q_conn.channel()


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/output/<id>", methods=["GET"])
def output(id):
    return render_template("output.html")


@app.route("/login", methods=["POST"])
def login():
    token, err = access.login(request)

    if not err:
        return token, 200
    else:
        return err[0], err[1]


@app.route("/upload", methods=["POST"])
def upload():
    auth_payload, err = access.check_auth(request)

    if err:
        return err[0], err[1]

    if "file" not in request.files:
        return "Exactly one file must be uploaded", 400

    f = request.files["file"]
    fid, err = mutation.upload(f, fs_input, channel, auth_payload)

    if err:
        return err[0], err[1]

    return fid, 200


@app.route("/download/<id>", methods=["GET"])
def download(id):
    file = fs_output.find_one({"_id": ObjectId(id)})
    if not file:
        return "File not found", 404

    return send_file(file, download_name=file.filename)


@app.route("/check-status/<id>", methods=["GET"])
def check_status(id):
    file = fs_output.find_one({"input_fid": id})

    if not file:
        return "File is still processing", 400
    else:
        return str(file._id), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

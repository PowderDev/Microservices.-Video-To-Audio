import jwt, datetime, os
from flask import Flask, request
import json
import mariadb
import database

app = Flask(__name__)
db_pool = database.create_connection_pool()


@app.route("/login", methods=["POST"])
def login():
    auth = request.authorization
    if not auth:
        return "Missing credentials", 401

    conn = get_db_connection()
    conn.execute("SELECT email, password FROM user WHERE email=%s", (auth.username,))

    if conn.rowcount == 0:
        return "Invalid credentials", 401

    row_headers = [x[0] for x in conn.description]
    row = conn.fetchone()
    user = dict(zip(row_headers, row))

    conn.close()

    if auth.password != user["password"]:
        return "Invalid credentials", 401
    else:
        return createJWT(auth.username, os.environ.get("JWT_SECRET"), True)


@app.route("/validate", methods=["POST"])
def validate():
    encoded_jwt = request.headers["Authorization"]

    if not encoded_jwt:
        return "missing credentials", 401

    encoded_jwt = encoded_jwt.split(" ")[1]

    try:
        decoded = jwt.decode(
            encoded_jwt, os.environ.get("JWT_SECRET"), algorithms=["HS256"]
        )
    except Exception as e:
        app.logger.error(e)
        return "Not authorized", 403

    return decoded, 200


def createJWT(username, secret, authz):
    return jwt.encode(
        {
            "username": username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(weeks=52),
            "admin": authz,
        },
        secret,
        algorithm="HS256",
    )


def get_db_connection():
    return database.get_connection_from_pool(db_pool)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000, debug=True)

import os, requests, json

AUTH_URL = os.environ.get("AUTH_URL")


def login(request):
    auth = request.authorization
    if not auth:
        return None, ("No credentials provided", 401)

    basicAuth = (auth.username, auth.password)

    res = requests.post(f"http://{AUTH_URL}/login", auth=basicAuth)

    if res.status_code != 200:
        return None, (res.text, res.status_code)

    return res.text, None


def validate(request):
    if not request.headers.get("Authorization"):
        return None, ("No credentials provided", 401)

    token = request.headers.get("Authorization")

    res = requests.post(f"http://{AUTH_URL}/validate", headers={"Authorization": token})

    if res.status_code != 200:
        return None, (res.text, res.status_code)
    else:
        return res.text, None


def check_auth(request):
    result, err = validate(request)

    if err:
        return None, err

    data = json.loads(result)

    if data["admin"] == False:
        return None, ("Unauthorized", 401)

    return data, None

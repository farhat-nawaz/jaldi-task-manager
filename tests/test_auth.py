from flask.testing import FlaskClient


def test_signup(client: FlaskClient, json_header, signup_payload):
    res = client.post(
        "/api/signup",
        headers=json_header,
        json=signup_payload,
    ).get_json()

    assert "status_code" in res
    assert "message" in res
    assert "error" in res
    assert "data" in res

    assert res["status_code"] == 201
    assert res["message"] == "success"
    assert res["error"] is False
    assert res["data"]["name"] == "Marty Bird"


def test_signup_fail(client: FlaskClient, json_header, signup_payload):
    res = client.post(
        "/api/signup",
        headers=json_header,
        json=signup_payload,
    ).get_json()

    assert "status_code" in res
    assert "message" in res
    assert "error" in res
    assert "data" in res

    assert res["status_code"] == 400
    assert res["message"] == "BAD REQUEST"
    assert res["error"] is True
    assert res["data"] is None


def test_signin(client: FlaskClient, json_header, signin_payload):
    res = client.post(
        "/api/signin",
        headers=json_header,
        json=signin_payload,
    ).get_json()

    assert "status_code" in res
    assert "message" in res
    assert "error" in res
    assert "data" in res

    assert res["status_code"] == 200
    assert res["message"] == "success"
    assert res["error"] is False
    assert "access_token" in res["data"]


def test_signin_no_payload(client: FlaskClient, json_header):
    res = client.post("/api/signin", headers=json_header)

    assert res.status_code == 400


def test_signin_wrong_credentials(client: FlaskClient, json_header, signin_payload):
    data = {"username": "abc", "password": "abc"}

    # Checks wrong username
    res = client.post(
        "/api/signin",
        headers=json_header,
        json=data,
    ).get_json()

    assert "status_code" in res
    assert "message" in res
    assert "error" in res
    assert "data" in res

    assert res["status_code"] == 400
    assert res["message"] == "INVALID USERNAME"
    assert res["error"] is True
    assert res["data"] is None

    # Checks wrong password
    data["username"] = signin_payload["username"]
    res = client.post(
        "/api/signin",
        headers=json_header,
        json=data,
    ).get_json()

    assert "status_code" in res
    assert "message" in res
    assert "error" in res
    assert "data" in res

    assert res["status_code"] == 400
    assert res["message"] == "INVALID PASSWORD"
    assert res["error"] is True
    assert res["data"] is None

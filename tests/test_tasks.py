import pytest
from flask.testing import FlaskClient


@pytest.mark.parametrize(
    "data,expected",
    [
        ({}, (2, ("name", "description"))),
        ({"name": "ABC"}, (1, ("description",))),
        ({"description": "ABC"}, (1, ("name",))),
    ],
)
def test_new_task_payload_validation(client: FlaskClient, json_header, data, expected):
    res = client.post("/api/tasks", headers=json_header, json=data)

    assert res.status_code == 400

    res = res.get_json()

    assert "validation_error" in res
    assert "body_params" in res["validation_error"]
    assert len(res["validation_error"]["body_params"]) == expected[0]

    for param in res["validation_error"]["body_params"]:
        assert param["type"] == "missing"
        assert param["loc"][0] in expected[1]


def test_new_task(client: FlaskClient, json_header, new_task, access_token):
    json_header["Authorization"] = f"Bearer {access_token()}"
    res = client.post("/api/tasks", headers=json_header, json=new_task)

    assert res.status_code == 201

    res = res.get_json()

    assert "status_code" in res
    assert "message" in res
    assert "error" in res
    assert "data" in res
    assert "id" in res["data"]
    assert "created_ts" in res["data"]
    assert "modified_ts" in res["data"]

    assert res["message"] == "success"
    assert res["error"] is False
    assert res["data"]["name"] == new_task["name"]
    assert res["data"]["description"] == new_task["description"]


def test_delete_task(client: FlaskClient, json_header, new_task, access_token):
    json_header["Authorization"] = f"Bearer {access_token()}"

    task_id = client.post("/api/tasks", headers=json_header, json=new_task).get_json()[
        "data"
    ]["id"]

    res = client.delete(f"/api/tasks/{task_id}", headers=json_header)

    assert res.status_code == 200

    res = res.get_json()

    assert "status_code" in res
    assert "message" in res
    assert "error" in res
    assert "data" in res
    assert "id" in res["data"]
    assert "created_ts" in res["data"]
    assert "modified_ts" in res["data"]

    assert res["message"] == "success"
    assert res["error"] is False
    assert res["data"]["name"] == new_task["name"]
    assert res["data"]["description"] == new_task["description"]


def test_put_task(client: FlaskClient, json_header, new_task, access_token):
    json_header["Authorization"] = f"Bearer {access_token()}"

    task_id = client.post("/api/tasks", headers=json_header, json=new_task).get_json()[
        "data"
    ]["id"]

    new_name = "Create Web API"
    new_description = "This is new task description."
    new_task["name"] = new_name
    new_task["description"] = new_description

    res = client.put(f"/api/tasks/{task_id}", headers=json_header, json=new_task)

    assert res.status_code == 200

    res = res.get_json()

    assert "status_code" in res
    assert "message" in res
    assert "error" in res
    assert "data" in res
    assert "id" in res["data"]
    assert "created_ts" in res["data"]
    assert "modified_ts" in res["data"]

    assert res["message"] == "success"
    assert res["error"] is False
    assert res["data"]["name"] == new_name
    assert res["data"]["description"] == new_description

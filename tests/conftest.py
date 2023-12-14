import copy
import functools

import pytest

from jaldi_task_manager.web.application import create_app

mock_users = [
    {"name": "Marty Bird", "username": f"martybird{i}", "password": "password"}
    for i in range(5)
]


@pytest.fixture(scope="session")
def app():
    _app = create_app("testing")

    yield _app


@pytest.fixture(scope="session")
def client(app):
    return app.test_client()


@pytest.fixture(scope="function", params=mock_users)
def signup_payload(request):
    return request.param


@pytest.fixture(scope="function", params=mock_users)
def signin_payload(request):
    payload = copy.deepcopy(request.param)
    payload.pop("name")

    return payload


@pytest.fixture(scope="function", params=[i for i in range(10)])
def new_task(request):
    i = request.param
    return {"name": f"Task{i}", "description": f"Task{i} added as test"}


@pytest.fixture(scope="session")
def json_header():
    return {"Content-Type": "application/json"}


@pytest.fixture(scope="session")
def access_token(client, json_header):
    @functools.cache
    def _access_token():
        token = client.post(
            "/api/signin",
            headers=json_header,
            json=mock_users[0],
        ).get_json()["data"]["access_token"]
        return token

    return _access_token

import pytest
from jaldi_task_manager.web.application import create_app


@pytest.fixture(scope="session")
def app():
    _app = create_app("testing")

    yield _app


@pytest.fixture(scope="function")
def client(app):
    return app.test_client()


@pytest.fixture(scope="function", params=[i for i in range(3)])
def signup_payload(request):
    i = request.param
    return {"name": "Marty Bird", "username": f"martybird{i}", "password": "password"}


@pytest.fixture(scope="function", params=[i for i in range(3)])
def login_payload(signup_payload):
    signup_payload.pop("name")
    return signup_payload


@pytest.fixture(scope="function", params=[i for i in range(3)])
def new_task(request):
    i = request.param
    return {"name": f"Task{i}", "description": f"Task{i} added as test"}


@pytest.fixture(scope="function")
def json_header():
    return {"Content-Type": "application/json"}

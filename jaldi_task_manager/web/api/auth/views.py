import jaldi_task_manager.web.api.auth.schema as auth_schema
from flask import Response
from flask.views import MethodView
from flask_pydantic import validate
from jaldi_task_manager.db.models.user import User
from jaldi_task_manager.web.utils import APIError, HTTPResponse
from werkzeug.security import generate_password_hash


class SignUpAPI(MethodView):
    init_every_request = False

    def __init__(self) -> None:
        self.model = User

    @validate()
    def post(self, body: auth_schema.SignUpParams) -> Response:
        user: User = self.model.get(username=body.username)

        if user:
            return HTTPResponse.err(APIError.BAD_REQUEST)

        new_user = User(
            username=body.username,
            name=body.name,
            password_hash=generate_password_hash(
                body.password,
                method="scrypt",
                salt_length=16,
            ),
        )
        new_user.flush()

        return HTTPResponse.ok(new_user.into_pydantic(auth_schema.UserOut), 201)

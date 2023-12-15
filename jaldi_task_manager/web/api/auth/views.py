from flask import Response
from flask.views import MethodView
from flask_jwt_extended import create_access_token
from flask_pydantic import validate
from werkzeug.security import check_password_hash, generate_password_hash

from jaldi_task_manager.db.models.user import User
from jaldi_task_manager.web.api.auth.schema import (
    JWTResponse,
    SignInParams,
    SignUpParams,
    UserOut,
)
from jaldi_task_manager.web.utils import APIError, HTTPResponse


class SignUpAPI(MethodView):
    init_every_request = False

    def __init__(self) -> None:
        self.model = User

    @validate()
    def post(self, body: SignUpParams) -> tuple[Response, int]:
        user: User = self.model.get(username=body.username)

        if user:
            return HTTPResponse.err(APIError.BAD_REQUEST), 400

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

        return HTTPResponse.ok(UserOut.model_validate(new_user), 201), 201


class SignInAPI(MethodView):
    init_every_request = False

    def __init__(self) -> None:
        self.model = User

    @validate()
    def post(self, body: SignInParams) -> Response:
        user: User | None = self.model.get(username=body.username)

        if user is None:
            return HTTPResponse.err(APIError.INVALID_USERNAME)
        elif check_password_hash(str(user.password_hash), body.password) is False:
            return HTTPResponse.err(APIError.INVALID_PASSWORD)

        resp = dict(access_token=create_access_token(identity=body.username))
        return HTTPResponse.ok(JWTResponse.model_validate(resp))

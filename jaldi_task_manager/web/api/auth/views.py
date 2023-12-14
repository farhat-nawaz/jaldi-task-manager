import jaldi_task_manager.web.api.auth.schema as auth_schema
from flask import Response
from flask.views import MethodView
from flask_jwt_extended import create_access_token
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


class SignInAPI(MethodView):
    init_every_request = False

    def __init__(self) -> None:
        self.model = User

    @validate()
    def post(self, body: auth_schema.SignInParams) -> Response:
        user: User | None = self.model.get(username=body.username)

        if user is None:
            return HTTPResponse.err(APIError.INVALID_REQUEST_DATA)

        access_token = create_access_token(identity=body.username)
        return HTTPResponse.ok(
            auth_schema.JWTResponse.model_construct(access_token=access_token),  # type: ignore
        )

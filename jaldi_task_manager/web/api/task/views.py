from uuid import UUID

from flask import Response
from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_pydantic import validate

from jaldi_task_manager.db.models.task import Task
from jaldi_task_manager.db.models.user import User
from jaldi_task_manager.web.api.task.schema import (
    TaskCreateParams,
    TaskOut,
    TaskUpdateParams,
)
from jaldi_task_manager.web.utils import APIError, HTTPResponse


class TaskAPI(MethodView):
    init_every_request = False

    @jwt_required()
    def get(self) -> tuple[Response, int]:
        current_user = User[get_jwt_identity()]  # type: ignore
        tasks = [TaskOut.model_validate(t.to_dict()) for t in current_user.tasks]  # type: ignore

        if len(tasks) == 0:
            return HTTPResponse.err(APIError.ENTITY_NOT_FOUND), 204

        return HTTPResponse.ok(tasks), 200

    @validate()
    @jwt_required()
    def post(self, body: TaskCreateParams) -> tuple[Response, int]:
        current_user = User[get_jwt_identity()]  # type: ignore

        task = Task(created_by=current_user, **body.model_dump())
        task.flush()

        return HTTPResponse.ok(TaskOut.model_validate(task.to_dict()), 201), 201


class TaskDetailAPI(MethodView):
    init_every_request = False

    def __init__(self) -> None:
        self.model = Task

    def _get(self, id: UUID) -> Task | APIError:
        user = User[get_jwt_identity()]  # type: ignore
        task = Task.get(id=id, created_by=user)

        return task or APIError.ENTITY_NOT_FOUND

    @validate()
    @jwt_required()
    def get(self, id: UUID) -> tuple[Response, int]:
        task = self._get(id)

        if isinstance(task, APIError):
            return HTTPResponse.err(task), 204

        return HTTPResponse.ok(TaskOut.model_validate(task.to_dict())), 200

    @validate()
    @jwt_required()
    def put(self, id: UUID, body: TaskUpdateParams) -> Response:
        task = self._get(id)

        if isinstance(task, APIError):
            return HTTPResponse.err(task)

        task.set(**body.model_dump())
        return HTTPResponse.ok(TaskOut.model_validate(task.to_dict()))

    @validate()
    @jwt_required()
    def delete(self, id: UUID) -> Response:
        task = self._get(id)

        if isinstance(task, APIError):
            return HTTPResponse.err(task)

        resp = TaskOut.model_validate(task.to_dict())
        task.delete()

        return HTTPResponse.ok(resp)

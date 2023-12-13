import enum
from typing import Any, Optional
from uuid import UUID

from flask import Response, jsonify
from flask.views import MethodView
from flask_pydantic import validate
from jaldi_task_manager.db.models.task import Task
from pydantic import BaseModel


class APIError(str, enum.Enum):
    BAD_REQUEST = "Bad Request"
    ENTITY_NOT_FOUND = "ENTITY NOT FOUND"


class TaskParams(BaseModel):
    name: str
    description: str


class TaskCreateParams(TaskParams):
    pass


class TaskUpdateParams(TaskParams):
    pass


class TaskAPI(MethodView):
    init_every_request = False

    def __init__(self, model: Task):
        self.model = model

    def get(self) -> Response:
        tasks = [t.to_dict() for t in self.model.select()]

        return _respond_with_success(200, tasks)

    @validate()
    def post(self, body: TaskCreateParams) -> Response:
        task: Task = self.model(**body.model_dump())
        task.flush()

        return _respond_with_success(201, task.to_dict())


class TaskDetailAPI(MethodView):
    init_every_request = False

    def __init__(self, model: Task):
        self.model = model

    def _get(self, id: UUID) -> Task | APIError:
        return self.model.get(id) or APIError.ENTITY_NOT_FOUND

    @validate()
    def get(self, id: UUID) -> Response:
        task = self._get(id)

        if isinstance(task, APIError):
            return _respond_with_error(400, task.value)

        return _respond_with_success(200, task.to_dict())

    @validate()
    def put(self, id: UUID, body: TaskUpdateParams) -> Response:
        task = self._get(id)

        if isinstance(task, APIError):
            return _respond_with_error(400, task.value)

        task.set(**body.model_dump())
        return jsonify(task.to_dict())

    @validate()
    def delete(self, id: UUID) -> Response:
        task = self._get(id)

        if isinstance(task, APIError):
            return _respond_with_error(400, task.value)

        task.delete()

        return _respond_with_success(204, task.to_dict())


def _respond(
    status_code: int,
    message: str,
    data: Optional[dict[str, Any] | list[dict[str, Any]]],
    error: bool,
) -> Response:
    return jsonify(
        {"error": error, "message": message, "status_code": status_code, "data": data},
    )


def _respond_with_success(
    status_code: int,
    data: dict[str, Any] | list[dict[str, Any]],
) -> Response:
    return _respond(status_code, "success", data, False)


def _respond_with_error(status_code: int, message: str) -> Response:
    return _respond(status_code, message, None, True)

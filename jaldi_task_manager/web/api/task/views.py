import enum
from typing import Any, Optional
from uuid import UUID

from flask import Response, jsonify
from flask.views import MethodView
from flask_pydantic import validate
from jaldi_task_manager.db.models.task import Task
from pydantic import BaseModel


class APIError(enum.Enum):
    ENTITY_NOT_FOUND = (204, "ENTITY NOT FOUND")
    SERVICE_ERROR = (500, "INTERNAL SERVER ERROR")

    def into_response(self) -> Response:
        return _respond_with_error(self.value[0], self.value[1])


class TaskParams(BaseModel):
    name: str
    description: str


class TaskCreateParams(TaskParams):
    pass


class TaskUpdateParams(TaskParams):
    pass


# from pony.orm.core import EntityMeta
# class IntoResponse:
#     def into_response[T: EntityMeta](self, data: T | list[T], status_code=200):
#         if isinstance(data, list):
#             data = [d.to_dict() for d in data]
#         else:
#             data = data.to_dict()
#         return jsonify(
#         {"error": False, "message": "success", "status_code": status_code, "data": data},
#     )


class TaskAPI(MethodView):
    init_every_request = False

    def __init__(self) -> None:
        self.model = Task

    def get(self) -> Response:
        tasks = [t.to_dict() for t in self.model.select()]

        return _respond_with_success(200, tasks)

    @validate()
    def post(self, body: TaskCreateParams) -> Response:
        task: Task = self.model(**body.model_dump())
        task.flush()

        return _respond_with_success(201, task)


class TaskDetailAPI(MethodView):
    init_every_request = False

    def __init__(self) -> None:
        self.model = Task

    def _get(self, id: UUID) -> Task | APIError:
        return self.model.get(id=id) or APIError.ENTITY_NOT_FOUND

    @validate()
    def get(self, id: UUID) -> Response:
        task = self._get(id)

        if isinstance(task, APIError):
            return task.into_response()

        return _respond_with_success(200, task)

    @validate()
    def put(self, id: UUID, body: TaskUpdateParams) -> Response:
        task = self._get(id)

        if isinstance(task, APIError):
            return task.into_response()

        task.set(**body.model_dump())
        return _respond_with_success(200, task)

    @validate()
    def delete(self, id: UUID) -> Response:
        task = self._get(id)

        if isinstance(task, APIError):
            return task.into_response()

        task.delete()
        return _respond_with_success(200, task)


# class CustomResponse:
#     status_code: int
#     message: str
#     error: str
#     data: dict[str, Any] | list[dict[str, Any]]

#     def __init__(
#       self, status_code: Optional[int] = None,
#       message: Optional[str] = None,
#       error: Optional[str] = None,
#       data: Optional[int] = None)


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

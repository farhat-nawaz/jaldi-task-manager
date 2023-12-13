import enum
from typing import Any, Optional
from uuid import UUID

from flask import Response, jsonify, request
from flask.views import MethodView
from jaldi_task_manager.db.models.task import Task
from pony.orm.core import ObjectNotFound


class APIError(str, enum.Enum):
    BAD_REQUEST = "Bad Request"
    ENTITY_NOT_FOUND = "ENTITY NOT FOUND"


class TaskAPI(MethodView):
    init_every_request = False

    def __init__(self, model: Task):
        self.model = model
        # self.validator = generate_validator(model)

    def _get(self, id: UUID) -> Task | APIError:
        try:
            return self.model[id]
        except ObjectNotFound:
            return APIError.ENTITY_NOT_FOUND

    def get(self, id: UUID) -> Response:
        task = self._get(id)

        if isinstance(task, APIError):
            return _respond_with_error(400, task.value)

        return _respond_with_success(200, task.to_dict())

    def post(self, id: UUID) -> Response:
        # errors = self.validator.validate(request.json)

        # if errors:
        #     return jsonify(errors), 400

        task: Task = self.model(**request.json)
        task.flush()

        return _respond_with_success(200, task.to_dict())

    def put(self, id: UUID) -> Response:
        task = self._get(id)

        if isinstance(task, APIError):
            return _respond_with_error(400, task.value)
        # errors = self.validator.validate(item, request.json)

        # if errors:
        #     return jsonify(errors), 400

        task.set(**request.json)
        return jsonify(task.to_dict())

    def delete(self, id: UUID) -> Response:
        task = self._get(id)

        if isinstance(task, APIError):
            return _respond_with_error(400, task.value)

        task.delete()

        return _respond_with_success(204, task.to_dict())


def _respond(
    status_code: int,
    message: str,
    data: Optional[dict[str, Any]],
    error: bool,
) -> Response:
    return jsonify(
        {"error": error, "message": message, "status_code": status_code, "data": data},
    )


def _respond_with_success(status_code: int, data: dict[str, Any]) -> Response:
    return _respond(status_code, "success", data, False)


def _respond_with_error(status_code: int, message: str) -> Response:
    return _respond(status_code, message, None, True)

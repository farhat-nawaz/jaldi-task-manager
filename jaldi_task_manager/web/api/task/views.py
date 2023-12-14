from uuid import UUID

from flask import Response
from flask.views import MethodView
from flask_pydantic import validate
from jaldi_task_manager.db.models.task import Task
from jaldi_task_manager.web.api.task.schema import (
    TaskCreateParams,
    TaskOut,
    TaskUpdateParams,
)
from jaldi_task_manager.web.utils import APIError, HTTPResponse


class TaskAPI(MethodView):
    init_every_request = False

    def __init__(self) -> None:
        self.model = Task

    def get(self) -> Response:
        tasks = [t.into_pydantic(TaskOut) for t in self.model.select()]

        return HTTPResponse.ok(tasks)

    @validate()
    def post(self, body: TaskCreateParams) -> Response:
        task: Task = self.model(**body.model_dump())
        task.flush()

        return HTTPResponse.ok(task.into_pydantic(TaskOut), 201)


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
            return HTTPResponse.err(task)

        return HTTPResponse.ok(task.into_pydantic(TaskOut))

    @validate()
    def put(self, id: UUID, body: TaskUpdateParams) -> Response:
        task = self._get(id)

        if isinstance(task, APIError):
            return HTTPResponse.err(task)

        task.set(**body.model_dump())
        return HTTPResponse.ok(task.into_pydantic(TaskOut))

    @validate()
    def delete(self, id: UUID) -> Response:
        task = self._get(id)

        if isinstance(task, APIError):
            return HTTPResponse.err(task)

        task.delete()
        return HTTPResponse.ok(task.into_pydantic(TaskOut))

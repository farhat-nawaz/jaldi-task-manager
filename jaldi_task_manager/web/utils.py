import enum
from typing import Type

from flask import Response, jsonify
from pydantic import BaseModel


class APIError(enum.Enum):
    BAD_REQUEST = (400, "BAD REQUEST")
    ENTITY_NOT_FOUND = (204, "ENTITY NOT FOUND")
    SERVICE_ERROR = (500, "SERVICE ERROR")


class PydanticModel:
    def into_pydantic(self, model: Type[BaseModel]) -> Type[BaseModel]:
        return model.model_validate(self)  # type: ignore


class HTTPResponse:
    @staticmethod
    def ok(
        data: Type[BaseModel] | list[Type[BaseModel]],
        status_code: int = 200,
    ) -> Response:
        if isinstance(data, list):
            data = [d.model_dump() for d in data]  # type: ignore
        else:
            data = data.model_dump()  # type: ignore

        return jsonify(
            {
                "error": False,
                "message": "success",
                "status_code": status_code,
                "data": data,
            },
        )

    @staticmethod
    def err(error: APIError) -> Response:
        return jsonify(
            {
                "error": True,
                "message": error.value[1],
                "status_code": error.value[0],
                "data": None,
            },
        )

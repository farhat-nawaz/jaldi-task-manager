from uuid import UUID

from pydantic import BaseModel, ConfigDict


class TaskParams(BaseModel):
    name: str
    description: str


class TaskCreateParams(TaskParams):
    pass


class TaskUpdateParams(TaskParams):
    pass


class TaskOut(BaseModel):
    id: UUID
    name: str
    description: str
    created_ts: float
    modified_ts: float

    model_config = ConfigDict(from_attributes=True)

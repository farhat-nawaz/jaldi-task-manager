from pydantic import BaseModel, ConfigDict


class SignUpParams(BaseModel):
    name: str
    username: str
    password: str


class UserOut(BaseModel):
    username: str
    name: str
    created_ts: float
    modified_ts: float

    model_config = ConfigDict(from_attributes=True)

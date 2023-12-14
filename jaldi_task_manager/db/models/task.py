import datetime
import uuid

from jaldi_task_manager.db import db
from jaldi_task_manager.web.utils import PydanticModel
from pony import orm


def _current_timestamp() -> float:
    return datetime.datetime.utcnow().timestamp()


class Task(db.Entity, PydanticModel):
    _table_: str = "tasks"

    id = orm.PrimaryKey(uuid.UUID, default=uuid.uuid4)
    name = orm.Required(str, max_len=40)
    description = orm.Required(str, max_len=500)
    created_ts = orm.Required(float, default=_current_timestamp)
    modified_ts = orm.Required(float, default=_current_timestamp)

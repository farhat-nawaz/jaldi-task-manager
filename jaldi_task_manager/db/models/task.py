import datetime
import uuid

from jaldi_task_manager.db import db
from pony import orm


def _current_timestamp() -> float:
    return datetime.datetime.utcnow().timestamp()

class Task(db.Entity):
    _table_: str = "tasks"

    id = orm.PrimaryKey(uuid.UUID, default=uuid.uuid4)
    name = orm.Required(str, max_len=40)
    description = orm.Required(orm.LongStr)
    created_ts = orm.Required(float, default=_current_timestamp)
    modified_ts = orm.Required(float, default=_current_timestamp)
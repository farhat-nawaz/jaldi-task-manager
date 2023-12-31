import datetime

from pony import orm

from jaldi_task_manager.db import db


def _current_timestamp() -> float:
    return datetime.datetime.utcnow().timestamp()


class User(db.Entity):
    _table_: str = "users"

    username = orm.PrimaryKey(str, max_len=20)
    password_hash = orm.Required(str, max_len=196)
    name = orm.Required(str, max_len=30)
    tasks = orm.Set("Task")
    created_ts = orm.Required(float, default=_current_timestamp)
    modified_ts = orm.Required(float, default=_current_timestamp)

    def before_insert(self) -> None:
        self.created_ts = _current_timestamp()
        self.modified_ts = _current_timestamp()

    def before_update(self) -> None:
        self.modified_ts = _current_timestamp()

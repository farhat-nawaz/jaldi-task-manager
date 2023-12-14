import os

from dotenv import load_dotenv
from flask import Flask
from pony.flask import Pony

load_dotenv()


def create_app() -> Flask:
    app = Flask("jaldi_task_manager")

    env = os.environ["ENVIRONMENT"].capitalize()
    app.config.from_object(f"jaldi_task_manager.config.{env}Config")

    from jaldi_task_manager.db import db
    from jaldi_task_manager.web.api.task.views import TaskAPI, TaskDetailAPI

    db.bind(**app.config["PONY"])
    db.generate_mapping(create_tables=True)
    Pony(app)

    app.add_url_rule("/api/tasks", view_func=TaskAPI.as_view("task"))
    app.add_url_rule(
        "/api/tasks/<uuid:id>",
        view_func=TaskDetailAPI.as_view("task_detail"),
    )

    return app

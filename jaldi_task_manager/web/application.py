import os

from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended import JWTManager
from pony.flask import Pony

load_dotenv()


def create_app() -> Flask:
    app = Flask("jaldi_task_manager")

    env = os.environ["ENVIRONMENT"].capitalize()
    app.config.from_object(f"jaldi_task_manager.config.{env}Config")

    # JWT setup
    jwt = JWTManager(app)  # noqa: F841

    import jaldi_task_manager.web.api.auth.views as auth_views
    import jaldi_task_manager.web.api.task.views as task_views
    from jaldi_task_manager.db import db

    # DB initialization
    db.bind(**app.config["PONY"])
    db.generate_mapping(create_tables=True)
    Pony(app)

    # Add URLs for views
    app.add_url_rule("/api/tasks", view_func=task_views.TaskAPI.as_view("task"))
    app.add_url_rule(
        "/api/tasks/<uuid:id>",
        view_func=task_views.TaskDetailAPI.as_view("task_detail"),
    )
    app.add_url_rule(
        "/api/signup",
        view_func=auth_views.SignUpAPI.as_view("signup"),
    )
    app.add_url_rule(
        "/api/signin",
        view_func=auth_views.SignInAPI.as_view("signin"),
    )

    return app

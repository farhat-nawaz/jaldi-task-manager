import os
from dotenv import load_dotenv
from flask import Flask
from pony.flask import Pony


load_dotenv()


def create_app() -> Flask:
    app = Flask(__name__)

    env = os.environ["ENVIRONMENT"].capitalize()
    app.config.from_object(f"jaldi_task_manager.config.{env}Config")

    from jaldi_task_manager.db import db
    from jaldi_task_manager.db.models.task import Task

    db.bind(**app.config["PONY"])
    db.generate_mapping(create_tables=True)
    Pony(app)

    # from yourapplication.views.admin import admin
    # from yourapplication.views.frontend import frontend
    # app.register_blueprint(admin)
    # app.register_blueprint(frontend)

    return app

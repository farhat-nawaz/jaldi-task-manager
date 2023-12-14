from jaldi_task_manager.web.application import create_app

app = create_app()

if __name__ == "__main__":
    host = app.config["HOST"]
    port = app.config["PORT"]
    debug = app.config["DEBUG"]
    app.run(host, port, debug)

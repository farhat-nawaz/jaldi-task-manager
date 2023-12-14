from jaldi_task_manager.web.application import create_app

if __name__ == "__main__":
    app = create_app("development")

    app.run()

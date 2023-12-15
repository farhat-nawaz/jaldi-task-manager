
# Jaldi Task Manager
This is a task management application that allows management of tasks, including creating new tasks,
updating existing tasks, retrieving task details, and deleting tasks.

## Requirements
In order to run this app, you will need the following tools installed:
- **Python 3.11:** This project requires Python 3.11 or above.
- **Poetry:** This is a dependency management tool which will install all the dependencies.
- **MySQL:** You will also need a MySQL database.

## Configuration

This application can be configured with environment variables.

You can create `.env` file in the root directory and place all
environment variables here. A file `.env.example` containing all the available environment variables has been added in the repository for reference.

Environment variable `USE_SQLITE` can be set to indicate that you want to use SQLITE database instead of MySQL. This overrides the use of MySQL even if its env vars are set.

## Running the Project

This project uses poetry. It's a modern dependency management
tool.

The project includes a `run.sh` shell script containing commands to run the project for ease of use. You can run it like so:
```bash
$ ./run.sh
```

Or in order to use poetry directly, use this set of commands:

```bash
poetry install
poetry run gunicorn -w 4 -b 127.0.0.1:8000 'server:create_app()'
```

This will start the server.


## Endpoints
The API expeoses following endpoints:
- `/api/signup`
    - **POST:**
        - will create a new user with given payload
        - payload: `{"name": "XX", "username": "XX", "password": "XX"}`
- `/api/signin`
    - **POST:**
        - will return an access token required for CRUD operations
        - payload: `{"username": "XX", "password": "XX"}`
- `/api/tasks`
     - **GET:**
        - will fetch all tasks for the authenticated user
     - **POST:**
        - will create a new task using json payload
        - payload: `{"name": "XX", "description": "XX"}`
- `/api/tasks/<uuid:id>`
    - **GET:**
        - will fetch task for the given id
    - **PUT:**
        - will update the task for the given id with json payload data
        - payload: `{"name": "XX", "description": "XX"}`
    - **DELETE:**
        - will delete task for the given id

All CRUD endpoints expect JWT Token as a header (`Authorization: Bearer XXXX`) for authentication.


## Project structure

```bash
$ tree "jaldi-task-manager"
jaldi-task-manager
├── README.md
├── jaldi_task_manager
│   ├── __init__.py
│   ├── config.py
│   ├── db
│   │   ├── __init__.py
│   │   └── models
│   │       ├── __init__.py
│   │       ├── task.py
│   │       └── user.py
│   └── web
│       ├── __init__.py
│       ├── api
│       │   ├── __init__.py
│       │   ├── auth
│       │   │   ├── __init__.py
│       │   │   ├── schema.py
│       │   │   └── views.py
│       │   └── task
│       │       ├── __init__.py
│       │       ├── schema.py
│       │       └── views.py
│       ├── application.py
│       └── utils.py
├── poetry.lock
├── pyproject.toml
├── run.sh
├── server.py
└── tests
    ├── __init__.py
    ├── conftest.py
    ├── test_auth.py
    └── test_tasks.py
```

## Pre-commit

To install pre-commit simply run inside the shell:
```bash
pre-commit install
```

pre-commit is very useful to check your code before publishing it.
It's configured using .pre-commit-config.yaml file.

By default it runs:
* black (formats your code);
* mypy (validates types);
* isort (sorts imports in all files);
* flake8 (spots possible bugs);

## Running tests

For running tests, run this command:
```bash
$ poetry run pytest --disable-warnings .
```

## Screenshots
#### SignUp
![alt text][signup]
#### SignIn
![alt text][signin]
#### Create Task
![alt text][new_task]
#### Get tasks
![alt text][get_tasks]
#### Get task by id
![alt text][get_task]
#### Update task
![alt text][update_task]
#### Delete task
![alt text][delete_task]

[signup]: ./jaldi_task_manager/static/signup.png "SignUp"
[signin]: ./jaldi_task_manager/static/signin.png "SignIn"
[new_task]: ./jaldi_task_manager/static/new_task.png "Create new task"
[get_tasks]: ./jaldi_task_manager/static/get_tasks.png "Get all tasks"
[get_task]: ./jaldi_task_manager/static/get_task.png "Get a task"
[update_task]: ./jaldi_task_manager/static/update_task.png "Update a task"
[delete_task]: ./jaldi_task_manager/static/delete_task.png "Delete a task"

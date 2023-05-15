# README

## Overview

This application provides task management functionality through a RESTful API using Flask.

## Assumptions
1. Each task has a boolean flag that indicates whether it is completed or not.
2. In order to complete a task it must be marked as completed. Deletion is kept seperate from completion due to the fact that the user may want to keep a record of the completed tasks.
3. The user can only view, create, update, and delete their own tasks. Backend level restriction weren't added due to time constraints. However, we assume their is app-level security that does not allow the user to view, create, update, or delete tasks that do not belong to them.
4. Since the flask framework being new to me, I didn't know the conventional directory structure or best practices for it's use. Therefore, I used a similar directory structure to the one I use for NodeJS projects.
5. Performance was not a priority for this project. Therefore, I did not implement any caching or other performance optimizations. Some methods might prefer readability over performance.

## Requirements

- Python 3.7 or higher
- Refer to `requirements.txt` or `Pipenv` for other required libraries.

## Installation

1. Clone or download this repository.
2. Install the required libraries.
    - If you're using Pipenv, run the following command:
        ```
        pipenv install
        ```
    - If you're using pip, run the following command:
        ```
        pip install -r requirements.txt
        ```
3. Create a `envs` directory in the root directory of the application.
    - Create a `.env.dev` file in the `envs` directory.
        - Add the following environment variables to the `.env.dev` file:
            ```
            DB_CONNECTION_URI=YOUR CONNECTION URI e.g. mysql+mysqlconnector://username:password@host:port/DATABASE?ssl_ca=rds-combined-ca-bundle.pem
            PORT=SOME PORT NUMBER e.g. 5000
            JWT_SECRET_KEY=SOME STRING e.g. cqVNhsnS4xEhDJOhVhFZwtv9peix2rm2YVo2VkjLf5CESvIwN9OgpRzjPx3lmQA
            JWT_EXPIRATION_HOURS=1
            FLASK_ENV=development
            FLASK_APP=app.py
            FLASK_DEBUG=True
            ```
4. Initialize the MySQL database and setup migrations.
    - Run the command inside the shell using pipenv:
        ```
        pipenv run init-dev-db
        ```
    - **OR** Run `scripts/init_dev_db.sh`
5. Start the application.
   - To run the development environment, execute the following command:
     ```
     pipenv run dev
     ```

## API Documentation

It wasn't added to the project due to time constraints, but some API documentation can be found in the Postman API shared on email.

## Implementation Details

### `src/config/routes.py`

Maps API endpoints to resource classes.

### `src/config/services.py`

Initializes services included in the application.

### `src/config/settings.py`

Manages application settings.

### `src/config/errors.py`

Defines errors that can occur in the application.

### `src/controllers/auth_controller.py`

Manages API endpoints related to authentication.

### `src/controllers/todos_controller.py`

Manages API endpoints related to tasks.

### `src/dtos/auth_dto.py`

Defines DTOs related to authentication.

### `src/dtos/todo_create_dto.py`

Defines the request format for the task creation API.

### `src/dtos/todo_update_dto.py`

Defines the request format for the task update API.

### `src/models/todo_model.py`

Defines the task model.

### `src/models/user_model.py`

Defines the user model.

### `src/config/__init__.py`

Performs package initialization.

## License

MIT License

# Configuration Diagram

```mermaid
graph TD
A[app.py] --> B((.envs))
A --> C((Pipfile))
A --> D((Pipfile.lock))
A --> E((requirements.txt))
A --> F((src))
B --> G(.env.development)
B --> H(.env.production)
C --> I(python_version = '3.7')
C --> J(flask = "*")
C --> K(flask-restful = "*")
D --> L(flask==1.1.2)
D --> M(flask-restful==0.3.8)
F --> N((config))
F --> O((controllers))
F --> P((dtos))
F --> Q((models))
F --> R((__init__.py))
N --> S(routes.py)
N --> T(services.py)
N --> U(settings.py)
O --> V(auth_controller.py)
O --> W(todos_controller.py)
P --> X(auth_dto.py)
P --> Y(todo_create_dto.py)
P --> Z(todo_update_dto.py)
Q --> AA(todo_model.py)
Q --> BB(user_model.py)
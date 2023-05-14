from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from werkzeug.exceptions import BadRequest

from resources.errors import NotFoundException, ValidationException

todos = [
    {
        "id": 1,
        "task": "Do this",
        "created_at": "2023-11-05 10:00:00",
    },
    {
        "id": 2,
        "task": "Do that",
        "created_at": "2023-11-05 10:00:00",
    },
    {
        "id": 3,
        "task": "Do this and that",
        "created_at": "2023-11-05 10:00:00",
    },
]

class TodosApi(Resource):
    method_decorators = [jwt_required()]
    
    def __init__(self) -> None:
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('task', type=str, required=True, help='No task provided', location='json')
        super(TodosApi, self).__init__()

    def get(self):
        return todos, 200

    def post(self):
        # Validate the request body
        try:
            self.reqparse.parse_args(strict=True)
        except BadRequest as e:
            raise ValidationException(e.description)

        # Retrieve the request body
        todo = request.get_json()
        todo['id'] = len(todos) + 1
        todos.append(todo)
        return todo, 200
    
class TodoApi(Resource):
    method_decorators = [jwt_required()]

    def __init__(self) -> None:
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('task', type=str, required=True, help='No task provided', location='json')
        super(TodoApi, self).__init__()

    def put(self, id):
        # Validate the request body
        try:
            self.reqparse.parse_args(strict=True)
        except BadRequest as e:
            raise ValidationException(e.description)

        # Retrieve the request body
        body = request.get_json()
        id = int(id)
        todo = [t for t in todos if t['id'] == id]
        if not todo:
            raise NotFoundException('Todo not found')
        todo[0]['task'] = body['task']
        return todo[0], 200

    def delete(self, id):
        id = int(id)
        todo = [t for t in todos if t['id'] == id]
        if not todo:
            raise NotFoundException('Todo not found')
        todos.remove(todo[0])
        return {'message': 'Todo deleted successfully'}, 200
    
    def get(self, id):
        id = int(id)
        todo = [t for t in todos if t['id'] == id]
        if not todo:
            raise NotFoundException('Todo not found')
        return todo[0], 200
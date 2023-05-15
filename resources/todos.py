from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from werkzeug.exceptions import BadRequest

from resources.errors import NotFoundException, ValidationException
from resources.models.todo_model import TodoModel, todos_schema, todo_schema
from resources.models.user_model import UserModel

class TodosApi(Resource):
    method_decorators = [jwt_required()]
    
    def __init__(self) -> None:
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('task', type=str, required=True, help='No task provided', location='json')
        self.reqparse.add_argument('author_id', type=int, required=True, help='No author_id provided', location='json')
        super(TodosApi, self).__init__()

    def get(self):
        author_id = request.args.get('author_id')
        todos = TodoModel.findAll(author_id)
        return todos_schema.dump(todos), 200

    def post(self):
        # Validate the request body
        try:
            self.reqparse.parse_args(strict=True)
        except BadRequest as e:
            raise ValidationException(e.description)

        # Retrieve the request body
        todo = request.get_json()

        # Create model
        author = UserModel.findOne(todo['author_id'])
        todo = TodoModel(task=todo['task'], author=author)
        todo = todo.create()
        return todo_schema.dump(todo), 201
    
class TodoApi(Resource):
    method_decorators = [jwt_required()]

    def __init__(self) -> None:
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('task', type=str, required=True, help='No task provided', location='json')
        super(TodoApi, self).__init__()
        
    def get(self, id:int):
        todo = TodoModel.findOne(id)
        if not todo:
            raise NotFoundException('Todo not found')
        return todo_schema.dump(todo), 200

    def put(self, id:int):
        # Validate the request body
        try:
            self.reqparse.parse_args(strict=True)
        except BadRequest as e:
            raise ValidationException(e.description)

        # Retrieve the request body
        body = request.get_json()
        todo = TodoModel.findOne(id)
        if not todo:
            raise NotFoundException('Todo not found')
        todo.update(body)
        return todo_schema.dump(todo), 200

    def delete(self, id:int):
        todo = TodoModel.findOne(id)
        if not todo:
            raise NotFoundException('Todo not found')
        todo.delete()
        return {'message': 'Todo deleted successfully'}, 200
    
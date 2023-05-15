from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from ..config.errors import NotFoundException, ValidationException
from ..models.todo_model import TodoModel, todos_schema, todo_schema
from ..models.user_model import UserModel
from ..dtos.todo_create_dto import TodoCreateDTO, todo_create_schema
from ..dtos.todo_update_dto import todo_update_schema

class TodosController(Resource):
    method_decorators = [jwt_required()]

    def get(self):
        author_id = request.args.get('author_id')
        todos = TodoModel.findAll(author_id)
        return todos_schema.dump(todos), 200

    def post(self):
        body = request.get_json()

        # Validate the request body
        errors = todo_create_schema.validate(body)
        if errors:
            raise ValidationException(errors)
        
        # Retrieve the request body
        todo = TodoCreateDTO(**body)

        # Create model
        author = UserModel.findOne(todo.author_id)
        todo = TodoModel(task=todo.task, author=author)
        todo = todo.create()
        return todo_schema.dump(todo), 201
    
class TodoController(Resource):
    method_decorators = [jwt_required()]
        
    def get(self, id:int):
        todo = TodoModel.findOne(id)
        if not todo:
            raise NotFoundException('Todo not found')
        return todo_schema.dump(todo), 200

    def put(self, id:int):
        body = request.get_json()

        # Validate the request body
        errors = todo_update_schema.validate(body)
        if errors:
            raise ValidationException(errors)

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
    
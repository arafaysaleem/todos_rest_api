from flask import request
from flask_restful import Resource, reqparse
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from werkzeug.exceptions import BadRequest
from datetime import timedelta

from src.config.errors import NotFoundException, DuplicateException, UnauthorizedException, ValidationException
from src.models.user_model import UserModel, user_schema
from src.models.auth_model import AuthDTO, auth_dto_schema

from src.config.settings import Settings

def hash_password(password):
    return generate_password_hash(password).decode('utf8')
 
def check_password(original_password, password):
    return check_password_hash(original_password, password)

def generate_token(email):
    expires = timedelta(hours=Settings.JWT_EXPIRATION_HOURS)
    return create_access_token(identity=str(email), expires_delta=expires)

class RegisterController(Resource):
    def __init__(self) -> None:
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('email', type=str, required=True, help='No email provided', location='json')
        self.reqparse.add_argument('password', type=str, required=True, help='No password provided', location='json')
        super(RegisterController, self).__init__()
    
    def post(self):
        errors = auth_dto_schema.validate(request.get_json())
        if errors:
            raise ValidationException(errors)
        
        # Retrieve the request body
        auth_dto = AuthDTO(**request.get_json())

        # Check if the user exists
        if UserModel.findByEmail(auth_dto.email):
            raise DuplicateException('User already exists')
        else:
            # Hash the password
            auth_dto.password = hash_password(auth_dto.password)
            user = UserModel(email=auth_dto.email, password=auth_dto.password).create()
            access_token = generate_token(user.email)
            user = dict(user_schema.dump(user))
            return {'token': access_token, **user}, 200

class LoginController(Resource):
    def __init__(self) -> None:
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('email', type=str, required=True, help='No email provided', location='json')
        self.reqparse.add_argument('password', type=str, required=True, help='No password provided', location='json')
        super(LoginController, self).__init__()

    def post(self):
        errors = auth_dto_schema.validate(request.get_json())
        if errors:
            raise ValidationException(errors)
        
        # Retrieve the request body
        auth_dto = AuthDTO(**request.get_json())
        
        # Retrieve user
        user = UserModel.findByEmail(auth_dto.email)

        # Check if the user exists
        if user:
            # Check if the password matches
            if check_password(user.password, auth_dto.password):
                access_token = generate_token(user.email)
                user = dict(user_schema.dump(user))
                return {'token': access_token, **user}, 200
            else:
                raise UnauthorizedException
            
        raise NotFoundException('User not found')

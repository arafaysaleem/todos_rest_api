from flask import request
from flask_restful import Resource, reqparse
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from werkzeug.exceptions import BadRequest
import datetime

from resources.errors import NotFoundException, DuplicateException, UnauthorizedException, ValidationException

from resources.settings import Settings

users = [
    {
        "id": 1,
        "email": "john.doe@gmail.com",
        "password": "$2b$12$stMLMuSw6KFKa0ei8LLLfeGYYdnfp4U3DW6HGWv9IhlwdiKqLr/oS",
        "created_at": "2023-11-05 10:00:00",
    },
    {
        "id": 2,
        "email": "mary.jane@gmail.com",
        "password": "$2b$12$stMLMuSw6KFKa0ei8LLLfeGYYdnfp4U3DW6HGWv9IhlwdiKqLr/oS",
        "created_at": "2023-11-05 10:00:00",
    },
]

def hash_password(password):
    return generate_password_hash(password).decode('utf8')
 
def check_password(original_password, password):
    return check_password_hash(original_password, password)

def generate_token(email):
    expires = datetime.timedelta(hours=Settings.JWT_EXPIRATION_HOURS)
    return create_access_token(identity=str(email), expires_delta=expires)

class RegisterApi(Resource):
    def __init__(self) -> None:
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('email', type=str, required=True, help='No email provided', location='json')
        self.reqparse.add_argument('password', type=str, required=True, help='No password provided', location='json')
        super(RegisterApi, self).__init__()
    
    def post(self):
        # Validate the request body
        try:
            self.reqparse.parse_args(strict=True)
        except BadRequest as e:
            raise ValidationException(e.description)
        body = request.get_json()

        # Check if the user exists
        existing_users = [user for user in users if user['email'] == body['email']]
        if existing_users:
            raise DuplicateException('User already exists')
        else:
            # Hash the password
            body['password'] = hash_password(body['password'])
            body['created_at'] = datetime.datetime.now().isoformat()
            body['id'] = len(users) + 1
            users.append(body)
            access_token = generate_token(body['email'])
            return {'token': access_token, **body}, 200

class LoginApi(Resource):
    def __init__(self) -> None:
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('email', type=str, required=True, help='No email provided', location='json')
        self.reqparse.add_argument('password', type=str, required=True, help='No password provided', location='json')
        super(LoginApi, self).__init__()

    def post(self):
        try:
            self.reqparse.parse_args(strict=True)
        except BadRequest as e:
            raise ValidationException(e.description)
        
        # Retrieve the request body
        body = request.get_json()
        email = body['email']
        # Check if the user exists
        for user in users:
            if user['email'] == email:
                # Check if the password matches
                if check_password(user['password'], body['password']):
                    access_token = generate_token(email)
                    return {'token': access_token, **user}, 200
                else:
                    raise UnauthorizedException
        raise NotFoundException('User not found')

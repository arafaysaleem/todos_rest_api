from marshmallow import fields, Schema

class AuthDTO():
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password
    
class AuthDTOSchema(Schema):
    email = fields.Email(required=True, help='No email provided')
    password = fields.Str(required=True, help='No password provided')

    class Meta:
        make_instance = True

    def make_object(self, data):
        return AuthDTO(**data)

auth_dto_schema = AuthDTOSchema()
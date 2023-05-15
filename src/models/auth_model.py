from marshmallow import fields, Schema

class AuthDTO():
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password
    
class AuthDTOSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)

    class Meta:
        make_instance = True

    def make_object(self, data):
        return AuthDTO(**data)

auth_dto_schema = AuthDTOSchema()
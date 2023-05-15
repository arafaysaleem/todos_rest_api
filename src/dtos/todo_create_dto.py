from marshmallow import fields, Schema

class TodoCreateDTO():
    def __init__(self, task: str, author_id: int):
        self.task = task
        self.author_id = author_id
    
class TodoCreateDTOSchema(Schema):
    task = fields.Str(required=True, help='No task provided')
    author_id = fields.Int(required=True, help='No author_id provided')

    class Meta:
        make_instance = True

    def make_object(self, data):
        return TodoCreateDTOSchema(**data)

todo_create_schema = TodoCreateDTOSchema()
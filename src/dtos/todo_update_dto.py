from marshmallow import fields, Schema

class TodoUpdateDTO():
    def __init__(self, task: str, author_id: int, is_done: bool):
        self.task = task
        self.author_id = author_id
        self.is_done = is_done
    
class TodoUpdateDTOSchema(Schema):
    task = fields.Str(required=False)
    author_id = fields.Int(required=False)
    is_done = fields.Bool(required=False)

    class Meta:
        make_instance = True

    def make_object(self, data):
        return TodoUpdateDTOSchema(**data)

todo_update_schema = TodoUpdateDTOSchema()
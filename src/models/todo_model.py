from datetime import datetime

from config.services import db, ma

class TodoModel(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    task = db.Column(db.String(100), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    is_done = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    def __repr__(self):
        return f'<Todo "{self.task[:20]}...">'
    
    @staticmethod
    def findAll(author_id) -> list:
        return TodoModel.query.filter_by(author_id=author_id).all()

    @staticmethod
    def findOne(id):
        return TodoModel.query.get(id)

    @staticmethod
    def exists(id) -> bool:
        return TodoModel.query.filter_by(id=id).exists()
    
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    def update(self, updates):
        for key, val in updates.items():
            setattr(self, key, val)
        db.session.commit()
        return self
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
class TodoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TodoModel
        load_instance = True
        sqla_session = db.session

todo_schema = TodoSchema()
todos_schema = TodoSchema(many=True)
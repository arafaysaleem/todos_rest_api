from datetime import datetime

from config.services import db, ma
from models.todo_model import TodoModel

class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.Text, nullable=False)
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
    tasks = db.relationship('TodoModel', backref='author', lazy=True)

    def __repr__(self):
        return f'<User "{self.email}">'
    
    @staticmethod
    def findAll() -> list:
        return UserModel.query.all()
    
    @staticmethod
    def findByEmail(email: str):
        return UserModel.query.filter_by(email=email).first()
    
    @staticmethod
    def findOne(id):
        return UserModel.query.get(id)
    
    @staticmethod
    def exists(id) -> bool:
        return UserModel.query.filter_by(id=id).exists()

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
    
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        load_instance = True
        sqla_session = db.session

user_schema = UserSchema()
users_schema = UserSchema(many=True)
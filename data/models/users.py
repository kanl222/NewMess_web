import datetime
import sqlalchemy
from ..db_session import SqlAlchemyBase
from sqlalchemy import orm
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    serialize_only = ('id', 'login', 'email', 'role_id')
    id = sqlalchemy.Column(sqlalchemy.Integer,primary_key=True, autoincrement=True)
    username = sqlalchemy.Column(sqlalchemy.String,nullable=True,unique=True)
    email = sqlalchemy.Column(sqlalchemy.String,nullable=True,unique=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String,nullable=True)
    creation_time = sqlalchemy.Column(sqlalchemy.DATETIME,nullable=True,default=datetime.datetime.now())
    icon = sqlalchemy.Column(sqlalchemy.LargeBinary,nullable=True)
    

    def __repr__(self):
        return f'<User> {self.id} {self.username}'

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

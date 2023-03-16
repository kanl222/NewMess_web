import datetime
import sqlalchemy
from ..db_session import SqlAlchemyBase
from sqlalchemy import orm

class messages(SqlAlchemyBase):
    __tablename__ = 'messages'
    id = sqlalchemy.Column(sqlalchemy.Integer,primary_key=True,autoincrement=True,nullable=True)
    id_user = sqlalchemy.Column(sqlalchemy.Integer,sqlalchemy.ForeignKey("users.id"),nullable=True)
    id_chat = sqlalchemy.Column(sqlalchemy.Integer,sqlalchemy.ForeignKey("chats.id"),nullable=True)
    send_time_message = sqlalchemy.Column(sqlalchemy.DATETIME,nullable=True,default=datetime.datetime.now())
    message = sqlalchemy.Column(sqlalchemy.String,nullable=True)
    
    def __repr__(self):
        return f'<User> {self.id} {self.username}'
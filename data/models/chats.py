import datetime
import sqlalchemy
from ..db_session import SqlAlchemyBase
from sqlalchemy import orm


class Chats(SqlAlchemyBase):
    __tablename__ = 'chats'
    id = sqlalchemy.Column(sqlalchemy.Integer,primary_key=True,autoincrement=True,nullable=True)
    tittle = sqlalchemy.Column(sqlalchemy.String,nullable=True,unique=True)
    chat_participant = sqlalchemy.Column(sqlalchemy.BLOB,nullable=True)
    icon = sqlalchemy.Column(sqlalchemy.LargeBinary,nullable=True)


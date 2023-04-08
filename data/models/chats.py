import datetime
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import Column, Integer, String, LargeBinary
from ..db_session import SqlAlchemyBase
from sqlalchemy.orm import declarative_base




class Chat(SqlAlchemyBase,SerializerMixin):
    __tablename__ = 'chat'

    id = Column(Integer, primary_key=True, autoincrement=True,unique=True,nullable=True)
    title = Column(String, nullable=False, unique=True)
    icon = Column(String, nullable=True)
    __serialize_only__ = ('id', 'title','icon')


    def to_dict(self):
        return {attr: getattr(self, attr) for attr in self.__serialize_only__}

    def __repr__(self):
        return f"Chat(id={self.id}, title='{self.title}')"

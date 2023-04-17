import datetime
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import Column, Integer, String, LargeBinary,ForeignKey
from ..db_session import SqlAlchemyBase
from sqlalchemy.orm import declarative_base,relationship




class Chat(SqlAlchemyBase,SerializerMixin):
    __tablename__ = 'chat'

    id = Column(Integer, primary_key=True, autoincrement=True,unique=True,nullable=True)
    title = Column(String, unique=True)
    admin_chat = Column(Integer, ForeignKey('user.id'), nullable=False)
    is_private_chats = Column(Integer,default=0, nullable=False)
    icon = Column(String)
    __serialize_only__ = ('id', 'title','icon')
    
    user = relationship("User")


    def to_dict(self):
        return {attr: getattr(self, attr) for attr in self.__serialize_only__}

    def __repr__(self):
        return f"Chat(id={self.id}, title='{self.title}')"

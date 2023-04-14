from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from ..db_session import SqlAlchemyBase


class ChatsRead(SqlAlchemyBase,SerializerMixin):
    __tablename__ = 'chats_read'
    id = Column(Integer, primary_key=True,autoincrement=True,unique=True)
    id_user = Column(Integer, ForeignKey('user.id'),nullable=True)
    id_chat = Column(Integer, ForeignKey('message.id'),nullable=True)

    user = relationship("User")
    message = relationship("Message")
    
    __serialize_only__ = ('id', 'id_user', 'id_chat')
    
    def __repr__(self):
        return f'MessagesRead(id={self.id},id_user={self.id_user},id_chat={self.id_chat})'
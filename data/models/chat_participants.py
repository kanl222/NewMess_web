from sqlalchemy import Column, Integer, ForeignKey
from ..db_session import SqlAlchemyBase
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin


class ChatParticipant(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'chatparticipants'

    id = Column(Integer, primary_key=True, autoincrement=True,nullable=False,unique=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    chat_id = Column(Integer, ForeignKey('chat.id'), nullable=False)

    user = relationship('User')
    chat = relationship('Chat')

    __serialize_only__ = ('id', 'user_id', 'chat_id')

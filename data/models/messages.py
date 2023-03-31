import datetime
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from ..db_session import SqlAlchemyBase


class Message(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'message'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    chat_id = Column(Integer, ForeignKey('chat.id'), nullable=False)
    send_time = Column(DateTime, default=datetime.datetime.now, nullable=False)
    text = Column(String, nullable=False)

    user = relationship("User")
    chat = relationship("Chat")

    __serialize_only__ = ('id', 'user_id', 'chat_id', 'send_time', 'text')

    def __repr__(self):
        return f"<Message(id={self.id}, user_id={self.user_id}, chat_id={self.chat_id},send_time={self.send_time!r}, text={self.text!r})>"

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'chat_id': self.chat_id,
            'send_time': str(self.send_time),
            'text': self.text
        }
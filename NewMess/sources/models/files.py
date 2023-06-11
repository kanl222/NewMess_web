from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from ..db_session import SqlAlchemyBase


class Files(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'files'
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    type_file = Column(String)

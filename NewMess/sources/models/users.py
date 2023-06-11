import datetime, time
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, LargeBinary, Boolean
from ..db_session import SqlAlchemyBase
from sqlalchemy import orm
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=True, unique=True, index=True)
    email = Column(String, nullable=True, unique=True, index=True)
    hashed_password = Column(String, nullable=True)
    _creation_time = Column(DateTime, nullable=True, default=datetime.datetime.now())
    icon = Column(String(), nullable=True)
    is_admin = Column(Boolean, nullable=True, default=0)

    __serialize_only__ = ['id', 'username', 'email', 'creation_time', 'icon']

    def __repr__(self):
        return f'<User> {self.id} {self.username}'

    def set_password(self, password: str) -> None:
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.hashed_password, password)

    @property
    def creation_time(self):
        return str(self._creation_time)

    def to_dict(self) -> dict:
        user_dict = {attr: getattr(self, attr) for attr in self.__serialize_only__}
        user_dict['creation_time'] = f"{user_dict['creation_time']}"
        return user_dict

    def date_to_millis(self):
        return int(time.mktime(self._creation_time.timetuple())) * 1000

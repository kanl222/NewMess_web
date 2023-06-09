import logging
import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec
from sqlalchemy.pool import QueuePool

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SqlAlchemyBase = dec.declarative_base()
__factory = None


def global_init(db_file: str):
    global __factory
    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("Необходимо указать адрес БД.")

    logger.info(f"Устанавливаем подключение к базе данных {db_file}")
    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'

    engine = sa.create_engine(conn_str,
                              echo=False,
                              poolclass=QueuePool,
                              pool_size=60,
                              max_overflow=20,
                              pool_timeout=30)
    __factory = orm.sessionmaker(bind=engine)
    from . import __all_models
    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    if __factory is None:
        raise ValueError("Необходимо вызвать функцию global_init сначала")
    session = __factory()
    session.expire_on_commit = False
    return session


def get_base():
    return SqlAlchemyBase

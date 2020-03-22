# encoding: utf-8
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


def make_engine(sql_uri, autocommit=False, **kws):
    options = {
        'connect_timeout': 60,
        'autocommit': autocommit,
    }
    return create_engine(sql_uri, pool_size=20, max_overflow=-1, pool_recycle=300, connect_args=options, **kws)


def get_db_session(db_url=None, autocommit=True):
    engine = make_engine(db_url, autocommit=autocommit, echo=False)
    session = scoped_session(sessionmaker(bind=engine))
    return session

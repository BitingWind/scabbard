# encoding: utf-8
from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker, scoped_session

from config import ConfigManager


def _init_database():
    """
    初始化 SQLAlchemy for MySQL
    """
    config = ConfigManager.get_config()

    # 初始化数据库连接
    engine_1 = engine_from_config(config.DB_1_CONFIG, prefix='')

    # 创建DBSession类型
    session_1_factory = sessionmaker(bind=engine_1, autoflush=False)

    # 托管到 scoped_session
    session_read_class = scoped_session(session_1_factory)

    return session_read_class


# Session Factory
#   1. 一般情况下都使用 DBSessionWrite
#   2. 导出数据、定时任务等只读性的批量任务使用 DBSessionRead
_DB1Session, = _init_database()


def db_1_session():
    """
    """
    session_ = _DB1Session()
    return session_
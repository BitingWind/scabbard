# encoding: utf-8
from datetime import datetime
from pymysql import DATETIME
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class OperatorMixedIn(object):
    """
    creator / modifier / optimistic_lock
    """
    creator_id = Column(INTEGER(11), nullable=False, default=0, doc=u'创建人ID')
    creator_name = Column(VARCHAR(64, collation=u'utf8mb4_bin'), nullable=False, default='', doc=u'创建人姓名')
    create_time = Column(DATETIME(fsp=6), nullable=False, default=datetime.utcnow, doc=u'创建时间')

    modifier_id = Column(INTEGER(11), nullable=False, default=0, doc=u'修改人ID')
    modifier_name = Column(VARCHAR(64, collation=u'utf8mb4_bin'), nullable=False, default='', doc=u'修改人姓名')
    modify_time = Column(DATETIME(fsp=6), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow, doc=u'最后修改时间')

    version = Column(INTEGER(11), nullable=False, default=1, doc=u'乐观锁')

    __mapper_args__ = {
        "version_id_col": version
    }
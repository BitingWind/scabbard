# encoding: utf-8
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import BIGINT, CHAR

from projects.project.model import Base, OperatorMixedIn


class TableModel(Base, OperatorMixedIn):
    """普通表model"""
    __tablename__ = 'table_name'

    id = Column(BIGINT(20), primary_key=True, doc=u'记录ID')
    name = Column(CHAR(128, collation=u'utf8mb4_bin'), nullable=False, default='', doc=u'名称')

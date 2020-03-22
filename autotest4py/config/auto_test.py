# encoding: utf-8
from config.common import Config


class AutoTestConfig(Config):
    """
    测试环境配置信息
    """
    DB_1_CONFIG = dict(
        url='mysql+pymysql://root:test@1.0.0.127:3306/db1?charset=utf8',
        pool_size=100,
        max_overflow=100,
        echo=False
    )
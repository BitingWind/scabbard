# -*- coding: utf-8 -*-
import os

from config.auto_test import AutoTestConfig
from config.auto_test1 import AutoTest1Config

_ENV_CONFIG_MAP = {
    'autotest': DevConfig,
    'autotest1': Test1Config
}


class ConfigManager(object):
    """
    configuration manager
    """

    @staticmethod
    def get_config():
        """
        grab global configuration
        """
        env = os.environ.get('ENV_PARAM') or 'autotest'
        config = _ENV_CONFIG_MAP.get(env)
        return config

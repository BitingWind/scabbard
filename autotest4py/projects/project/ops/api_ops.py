# encoding: utf-8

from base.my_requests import MyRequests
from projects.project import env_config
from utils.common.log_util import LogUtil


class APIOps(object):

    def __init__(self, host=env_config.api_hostname):
        self.HOST = host

        self.GET_API = self.HOST + '/get'
        self.POST_API = self.HOST + '/post'

    def post_for_xxx(self, param_1, param_2):
        LogUtil.step(u"--- 通过API xxxx {} {}".format(param_1, param_2))

        data = {
            "param_1": param_1,
            "param_2": param_2,
        }
        req = MyRequests.post(self.POST_API, data=data, is_json=True)
        return req.json().get('code'), req.json().get('msg'), req.json().get('data')

    def get_for_xxx(self, param_1, param_2):
        LogUtil.step(u"--- 通过API xxxx {} {}".format(param_1, param_2))

        params = {
            "param_1": param_1,
            "param_2": param_2,
        }
        rsp = MyRequests.get(self.GET_API, params=params)
        return rsp.json().get('data')
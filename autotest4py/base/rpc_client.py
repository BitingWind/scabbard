# encoding: utf-8
import datetime
import json
import requests
from test_env_config import VALID_TEST_HOST
from utils.common.log_util import LogUtil


class RPCClient(object):
    """
    获取一个rpc client
    """

    def __init__(self, rpc_host, rpc_port, rpc_server_name):
        """
        构建一个client实例
        :param rpc_host: 被调用的host ip
        :param rpc_port: 被调用的 port
        :param rpc_server_name: rpc_server_name 全拼
        """
        self.rpc_host = rpc_host
        self.rpc_port = rpc_port
        self.rpc_server_name = rpc_server_name

    @property
    def address(self):
        if self.rpc_host not in VALID_TEST_HOST:
            raise Exception(
                "测试环境可用机器列表: {}, 不包含 当前请求的rpc host: {}\n "
                " -- 如果有例外,local 使用时候,可以屏蔽这里\n"
                "['注意!!!']不可以把线上ip push上去,自动化干的事情,谁也保不齐!!!".format(
                    VALID_TEST_HOST, self.rpc_host))

        if self.rpc_port and self.rpc_port:
            return "{}:{}".format(self.rpc_host, self.rpc_port)
        else:
            LogUtil.error(u'本次没有指定rpc的IP和端口，本次请求会打到线上!')
            return

    def rpc_request(self, func_name, params_body):
        """
        通过MS测试通用接口调用rpc接口获取结果
        :param func_name: rpc方法名 不带括号，不带参数描述，支持下划线形式 如 query_a_b_c
        :param params_body: dict 该方法req的 params map
        :return: 调用成功的结果
        """
        LogUtil.info(u"-----------------【rpc Request】 ----------------")

        LogUtil.info(u"  基础参数  rpc_server_name: {}, address: {}".format(self.rpc_server_name, self.address))
        payload = self._gen_rpc_payload(func_name, params_body)

        start = datetime.datetime.now()

        errno, data, msg = rpcOps().request_rpc_server_name_rpc(data=payload)
        end = datetime.datetime.now()

        diff_seconds = (end - start).total_seconds()

        LogUtil.info(u"-----------------【rpc Response】 ----------------")
        LogUtil.info(u" errno: {}, msg: {}, data: {}".format(errno, msg, data.__repr__().decode("unicode-escape")))
        LogUtil.info(u"-----------------------------------------------")
        LogUtil.info(u"【性能】请求花费时间 {} s ".format(diff_seconds))
        LogUtil.info(u"-----------------------------------------------")
        if errno:
            raise Exception(u"MS 接口调用结果错误，msg:{}".format(msg))

        return data

    def _gen_rpc_payload(self, func_name, params_body):
        body = {}
        body['rpc_server_name'] = self.rpc_server_name
        body['func_name'] = func_name
        body['request'] = json.dumps(params_body)
        if self.address:
            body['address'] = self.address
        LogUtil.print_dict_in_lines(body, u"rpc payload")
        return json.dumps(body)


class rpcOps:
    """
    rpc 准化成 api 调用
    """

    url_api = "http://domain/rpc_api"

    def request_rpc_server_name_rpc(self, data):
        headers = {"Content-Type": "application/json"}
        req = requests.post(self.url_api, data=data, json=json, headers=headers)
        data = req.json().get("data")
        return int(req.json().get("error_code")), json.loads(data) if data else None, req.json().get("error_message")

# encoding: utf-8
from base.rpc_client import RPCClient
from projects.project import env_config


class ProjectRpcOps(object):
    RPC_FUNC_NAME = "RpcFuncName"


    def __init__(self, rpc_env):
        self.cont_rpc_client = RPCClient(rpc_env, rpc_env, env_config.rpc_server_name)


    def rpc_func(self, param_1, param_2):
        """
        调用rpc
        """
        params = {
            "param_1": param_1,
            "param_2": param_2
        }
        data = self.cont_rpc_client.rpc_request(self.RPC_FUNC_NAME, params_body=params)
        self._check_rpc_base_rsp(data, self.RPC_FUNC_NAME)
        return data

    def _check_rpc_base_rsp(self, data, func_name):
        """
        返回结果，基础检查
        """
        base_resp = data.get("BaseResp")
        # 返回code 不为0 报错
        if base_resp.get('StatusCode'):
            raise Exception(" RPC 接口调用失败，func: {}".format(func_name))

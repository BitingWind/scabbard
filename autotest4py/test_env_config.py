# encoding: utf-8
import os


# 出于安全考虑，这里放http/thrift 接口调用时可用的host
VALID_TEST_HOST = ['1.0.0.127']

is_scp_to_remote = True
tomcat_server = "1.0.0.127:8080"  # server report IP：port
server_tomcat_dir = "~/jenkins_home/tomcat/webapps/auto_reports/"

# 是否发送IM通知
IM_report_send = True
IM_group_id = 123

# 以下配置，暂时丢弃
report_url = u""

local_tomcat_dir = "~/tomcat/webapps/auto_reports/"
local_sever = "1.0.0.127:8080"

# 根目录获取
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))


def get_rpc_host_port_by_project_name(project_name):
    """获取每个项目的RPC环境配置"""
    rpc_env_config = os.environ.get('RPC_ENV_CONFIG')
    # parse by project_name
    return ''

def get_api_hostname_by_project_name(project_name):
    """获取每个项目的WEB API环境配置"""
    ci_hostname = os.environ.get('API_ENV_CONFIG')
    # parse by project_name
    return ''
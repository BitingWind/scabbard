# encoding: utf-8
import test_env_config
from base import db_base_param

# db 地址
db_1_url = "mysql+pymysql://root:test@1.0.0.127:3306/db_1?charset=utf8"
DB_1_Session = db_base_param.get_db_session(db_1_url)


# rpc 地址
rpc_server_name = 'project_rpc'
rpc_default_env = "1.0.0.127:1234"
ci_rpc_env = test_env_config.get_rpc_host_port_by_project_name('my_project_name')


# api 地址
default_hostname = "http://1.0.0.127:8080"
rpc_env = ci_rpc_env or rpc_default_env

ci_hostname = test_env_config.get_api_hostname_by_project_name('my_project_name')
api_hostname = ci_hostname or default_hostname
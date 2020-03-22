# encoding: utf-8
"""
本文件，主要包含基础的装饰器，编织
"""
import time
from functools import wraps

from urllib.parse import urlparse

from utils.common.log_util import LogUtil
from test_env_config import VALID_TEST_HOST


def statistic_request_url(func):
    """
    将http req的接口请求信息存起来，用于分析打印
    """

    def decorator_proxy(*args, **kwargs):
        url = kwargs.get('url') or args[0]
        url_parse_result = urlparse(url)
        path_exclude_var = ''
        for x in url_parse_result.path.split("/"):
            x = x if not x.isdigit() else '<var_num>'
            path_exclude_var = path_exclude_var + x + '/'
        host_path = url_parse_result.netloc + ' ' + path_exclude_var

        # check host is valid
        ip_port_list = url_parse_result.netloc.split(':')
        # ip:port格式，非域名，域名暂不做限制
        if len(ip_port_list) == 2 and ip_port_list[0] not in VALID_TEST_HOST:
            raise Exception(
                "测试环境可用机器列表: {}, \n"
                "不包含当前请求的host: {}\n "
                " -- 如果有例外,local 使用时候,可以屏蔽这里\n"
                "如果长期可用，可以维护到 /test_env_config.py中 VALID_TEST_HOST中"
                "['注意!!!']不可以把线上ip push上去, 自动化干的事情,谁也保不齐!!!".format(
                    VALID_TEST_HOST, ip_port_list[0]))

        # 过了校验，再发送请求
        _result = func(*args, **kwargs)
        request_path_set.add(host_path)
        return _result

    return decorator_proxy


def loop_interval_overtime(interval, overtime):
    """
    如果不抛异常停止循环，否则继续直到结束，返回False
    因为不会启异步线程调用，运行时间最长为 （overtime + 函数执行时间）
    注意：函数不能有返回值，会被替换，建议在函数上传入结果参数，在函数内部做修改 举例 func(parm*, result_dict)
    示例参考：projects/cont/test/API/cont_type_by_case/dcd_cont_case.py 中 verify_dcd_single_count 方法使用
    :param interval: 间隔 s
    :param overtime: 总超时 s
    :return: 是否最终成功 True or False
    """

    def loop_decorator(func):
        @wraps(func)
        def loop_decorator_proxy(*args, **kwargs):
            LogUtil.info(u'这是一个循环调用，每{}秒调用一次方法{}, 超时为{}秒'.format(interval, func.__name__, overtime))
            start = time.time()
            cur = time.time()
            i = 1
            while cur < start + overtime:
                try:
                    LogUtil.info(u'第{}次循环'.format(i))
                    i += 1
                    func(*args, **kwargs)
                    return True
                except Exception as e:
                    time.sleep(interval)
                    cur = time.time()
            return False

        return loop_decorator_proxy

    return loop_decorator

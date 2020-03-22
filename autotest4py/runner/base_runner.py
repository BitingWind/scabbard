# encoding: utf-8
import os
import sys
import time
import unittest
from abc import ABCMeta, abstractmethod
from importlib import reload

import test_env_config
from base import cached_data
from base import HTMLTestRunner
from test_env_config import tomcat_server, server_tomcat_dir
from utils.IM_notification import IM_report
from utils.IM_notification.IM_utils import IMUtils
from utils.common.data_formatter import DataFormatter
from utils.common.log_util import LogUtil


class BaseRunner:
    __metaclass__ = ABCMeta

    def __init__(self, project_name, report_title, group_id=None, report_receiver_list=None, is_scp_to_remote=None,
                 is_send_IM=None, description=None):
        """
        构造一个runner
        :param project_name: 项目名称
        :param report_title: 报告title名
        :param group_id: report通知 飞书群id 默认自动化通知群
        :param report_receiver_list 报告接受人list 传用户的邮箱前缀
        :param is_scp_to_remote: 是否copy到远程 以下两者，优先级：自定义 > 统一config配置
        :param is_send_IM: 是否发送结果的IM通知
        """
        self.project_name = project_name
        self.report_title = report_title
        self.group_id = group_id or test_env_config.IM_group_id
        self.is_send_IM = is_send_IM if is_send_IM is not None else test_env_config.IM_report_send
        self.is_scp_to_remote = is_scp_to_remote if is_scp_to_remote is not None else test_env_config.is_scp_to_remote
        self.report_description = '' if description is None else description
        self.unittest_results = None
        self.report_receiver_list = set() if not report_receiver_list else set(report_receiver_list)
        self.IM_client = IMUtils()

    @abstractmethod
    def suite(self):
        all_suite = unittest.TestSuite()
        # common test_case
        return all_suite

    def run(self):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        self._pre()
        self._act()
        self._post()

    def _pre(self):
        """
        预处理 数据准备，初始环境检测等，这里暂时不留钩子
        """
        # check_remote()
        # data_prepare()
        # 这里暂时不放在pre里面 pre单独用于继承
        # self._generate_var()
        pass

    def _act(self):
        """
        执行case，产生结果
        """
        self._generate_var()
        LogUtil.info(u"[RUN BEGIN] 结果输出到本地路径: {}".format(self.local_report_file_full_path))
        local_out_stream = open(self.local_report_file_full_path, 'wb')
        runner = HTMLTestRunner.HTMLTestRunner(stream=local_out_stream, title=self.report_title,
                                               description=self.report_description)
        self.unittest_results = runner.run(self.suite())
        LogUtil.info(u"[RUN END] 结果输出到本地路径: {}".format(self.local_report_file_full_path))

    def _post(self):
        """
        后处理 用于处理数据，结果处理，展示等 这里暂时不留钩子
        """
        # 拷贝到远程
        if self.is_scp_to_remote:
            self._scp_to_remote()
        else:
            LogUtil.info(u"[REMOTE] 指定不拷贝到远程！本地文件名不带时间戳。")
        # 发送IM通知
        if self.is_send_IM:
            self._send_IM()
        else:
            LogUtil.info(u"[IM] 指定不发送IM")
        LogUtil.info(u"最后再次打印报告存放位置： \n" + self.local_report_file_full_path)

        # 最后打印一下，性能可能超标的请求 set
        self._print_request_cost_info(cached_data.request_list)
        self._print_cover_request_url_set(cached_data.request_path_set)

    def _print_request_cost_info(self, request_list):
        LogUtil.info(u"\n-----------------------------------------------------------------------")
        LogUtil.info(u"【性能】接口耗时，超过 '{}' s 的接口请求如下： ".format(cached_data.time_cost_threshold))

        if len(request_list) == 0:
            LogUtil.info(u"棒棒的，没有任何请求超过阈值！")

        request_url_dict = {}

        for request in request_list:
            request_url_dict[request.get('request').get('url')] = request.get('time')

        DataFormatter().print_dict_in_lines(request_url_dict)

    def _print_cover_request_url_set(self, request_url_set):
        LogUtil.info(u"\n-----------------------------------------------------------------------")
        LogUtil.info(u"【URL 覆盖】当前项目【{}】 覆盖的url，接口如下： ".format(self.project_name))
        sorted = list(request_url_set)
        sorted.sort()
        print('\n'.join(sorted))

    def _generate_var(self):
        """
        确定一些通用变量
        """
        self.__generate_report_file_name()
        self.__generate_local_report_file_path()

    def __generate_report_file_name(self):
        """
        文件名生成
        """
        time_stamp = ""
        if self.is_scp_to_remote:
            time_stamp = time.strftime("_%Y-%m-%d_%H-%M-%S", time.localtime())
        report_file_name = self.project_name + '_regression_report{}.html'.format(time_stamp)
        self.report_file_name = report_file_name

    def __generate_local_report_file_path(self):
        """
        生成本地文件路径，这里用的根路径加report
        """
        local_report_file_full_path = os.path.abspath(
            os.path.join(test_env_config.ROOT_DIR, "report", self.report_file_name))
        LogUtil.info("Report_name=" + self.report_file_name)
        LogUtil.info(u"报告存放位置： \n" + local_report_file_full_path)

        # 确定生成报告的本地全路径
        self.local_report_file_full_path = local_report_file_full_path

    def _scp_to_remote(self):
        """
        拷贝到远程
        """
        server_location = "{}:{}{}/".format(tomcat_server.split(":")[0],
                                            server_tomcat_dir, self.project_name)

        scp_command = 'scp {} {}'.format(self.local_report_file_full_path, server_location)
        LogUtil.info(u"[SCP REMOTE BEGIN] 拷贝到远程 命令: {}".format(scp_command))
        os.system(scp_command)
        LogUtil.info(u"[SCP REMOTE END] 拷贝完成 remote tomcat server ： \n    {}".format(scp_command))

        remote_url_head = "http://{}/auto_reports/{}/".format(tomcat_server, self.project_name, self.report_file_name)
        remote_full_path = remote_url_head + self.report_file_name
        LogUtil.info(u"远端服务器URL： {}".format(remote_full_path))

    def _send_IM(self):
        """
        IM report 发送到IM群
        如果需要自定义内容，可实现_custom_IM_body方法
        """
        LogUtil.info(u"[IM SEND BEGIN] 开始发送IM 群通知。。。")
        IM_body, pass_rate = IM_report.format_simple_summary(self.unittest_results)

        # 当前服务请求接口数量
        covered_api_counter = self.__counter_current_project_covered_api()
        if covered_api_counter:
            IM_body += "\ncovered_api_counter : {}\n".format(covered_api_counter)

        # 自定义内容
        custom_IM_body = self._custom_IM_body()

        final_IM_body = u"{}\n详细报告 ：<a href=http://{}/auto_reports/{}/{}>Report Link</a> \n{}".format(IM_body,
                                                                                                        tomcat_server,
                                                                                                        self.project_name,
                                                                                                        self.report_file_name,
                                                                                                        custom_IM_body)
        title_time = time.strftime("%Y-%m-%d_%H:%M", time.localtime())
        msg_title = u"{} 自动化测试报告_{} - 通过率 ： {} %".format(self.project_name.upper(), title_time, pass_rate)
        self.IM_client.bot_join_group(self.group_id)
        self.IM_client.send_msg_to_group(msg_title, final_IM_body, self.group_id)
        for receiver in self.report_receiver_list:
            self.IM_client.send_msg_to_person(msg_title, final_IM_body, receiver)

    def _custom_IM_body(self):
        """
        自定义IM内容，嵌入在数据汇总报告下面
        """
        return ""

    def __counter_current_project_covered_api(self):
        ci_hostname = os.environ.get('API_ENV')
        if not ci_hostname:
            return 0
        current_project_api = [a for a in cached_data.request_path_set if a.startswith(ci_hostname)]
        return len(current_project_api)

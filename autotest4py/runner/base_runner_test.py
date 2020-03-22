# encoding: utf-8
import datetime
import os
import sys
import time
from importlib import reload

import test_env_config
from base import cached_data
from base import HTMLTestRunner
from base import project_ownership
from test_env_config import tomcat_server, server_tomcat_dir
from utils.IM_notification import IM_report
from utils.IM_notification.IM_utils import IMUtils
from utils.common.log_util import LogUtil
from utils.common.data_formatter import DataFormatter


class BaseRunnerTest:

    def __init__(self, project_name, report_title, group_id=None, report_receiver_list=None, is_scp_to_remote=None,
                 is_send_IM=None, description=None, suite=None):
        """
        构造一个runner
        :param project_name: 项目名称
        :param report_title: 报告title名
        :param group_id: report通知 群id 默认自动化通知群
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
        self.report_receiver_list = project_ownership.get_receiver_set_by_project_name(self.project_name) if not report_receiver_list else set(report_receiver_list)
        self.IM_client = IMUtils()
        self.suite = suite

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
        self.unittest_results = runner.run(self.suite)
        LogUtil.info(u"[RUN END] 结果输出到本地路径: {}".format(self.local_report_file_full_path))

    # 单个run方法屏蔽发送IM通知
    def _post(self):
        """
        后处理 用于处理数据，结果处理，展示等 这里暂时不留钩子
        """
        # 拷贝到远程
        if self.is_scp_to_remote:
            self._scp_to_remote()
        else:
            LogUtil.info(u"[REMOTE] 指定不拷贝到远程！本地文件名不带时间戳。")


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
        print('\n'.join(request_url_set))

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
        import datetime
        time_stamp = ""
        if self.is_scp_to_remote:
            time_stamp = datetime.datetime.now().strftime("_%Y-%m-%d_%H-%M-%S.%f")
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

    def _custom_IM_body(self):
        """
        自定义IM内容，嵌入在数据汇总报告下面
        """
        return ""

    def scp_merge_file_to_remote(self, merge_report_file_name):
        """
        拷贝到远程
        """
        server_location = "{}:{}{}/".format(tomcat_server.split(":")[0],
                                            server_tomcat_dir, self.project_name)
        import os
        local_report_file_full_path = os.path.abspath(
            os.path.join(test_env_config.ROOT_DIR, "report", merge_report_file_name))

        scp_command = 'scp {} {}'.format(local_report_file_full_path, server_location)
        LogUtil.info(u"[SCP REMOTE BEGIN] 拷贝到远程 命令: {}".format(scp_command))
        import os
        os.system(scp_command)
        LogUtil.info(u"[SCP REMOTE END] 拷贝完成 remote tomcat server ： \n    {}".format(scp_command))

        remote_url_head = "http://{}/auto_reports/{}/".format(tomcat_server, self.project_name, merge_report_file_name)
        remote_full_path = remote_url_head + merge_report_file_name
        LogUtil.info(u"远端服务器URL： {}".format(remote_full_path))

    def send_IM(self, pass_rate, total, _pass, failure, error, merge_report_file_name):
        """
        IM report 发送到IM群
        如果需要自定义内容，可实现_custom_IM_body方法
        """
        LogUtil.info(u"[IM SEND BEGIN] 开始发送IM 群通知。。。")
        IM_body, pass_rate = IM_report.format_report_for_temporary_test(pass_rate=pass_rate, total_case=total,
                                                                            pass_case=_pass, failure_case=failure,
                                                                            error_case=error,)

        # 自定义内容
        custom_IM_body = self._custom_IM_body()
        final_IM_body = u"{}\n详细报告 ：<a href=http://{}/auto_reports/{}/{}>Report Link</a> \n{}".format(IM_body,
                                                                                                        tomcat_server,
                                                                                                        self.project_name,
                                                                                                        merge_report_file_name,
                                                                                                        custom_IM_body)
        title_time = time.strftime("%Y-%m-%d_%H:%M", time.localtime())
        msg_title = u"{} 自动化测试报告_{} - 通过率 ： {} %".format(self.project_name.upper(), title_time, pass_rate)

        self.IM_client.send_msg_to_group(msg_title, final_IM_body, self.group_id)
        for receiver in self.report_receiver_list:
            self.IM_client.send_msg_to_person(msg_title, final_IM_body, receiver)

    def post_after_merge(self, pass_rate, total, _pass, failure, error, merge_report_file_name):
        """
        合并后发送IM消息
        """
        # 拷贝到远程
        if self.is_scp_to_remote:
            self.scp_merge_file_to_remote(merge_report_file_name)
        else:
            LogUtil.info(u"[REMOTE] 指定不拷贝到远程！本地文件名不带时间戳。")
        # 发送IM通知
        if self.is_send_IM:
            self.send_IM(pass_rate=pass_rate, total=total, _pass=_pass, failure=failure,
                           error=error, merge_report_file_name=merge_report_file_name)

    @staticmethod
    def generate_merge_report_file_name(project_name):
        time_stamp = datetime.datetime.now().strftime("_%Y-%m-%d_%H-%M-%S.%f")
        merge_report_file_name = project_name + '_regression_report{}_results.html'.format(time_stamp)
        return merge_report_file_name

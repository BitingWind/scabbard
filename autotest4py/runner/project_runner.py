# encoding: utf-8
from base import project_ownership
from runner.base_runner import BaseRunner
from test_suite import project_case_suite
from runner.base_args import parser


class ProjectRunner(BaseRunner):
    """
    CONT 自动化测试
    """
    # 是否需要 diff 的case
    basic_diff = True

    def suite(self):
        all_suite = BaseRunner.suite(self)
        all_suite.addTests(project_case_suite.pack_suite())
        return all_suite

    def _custom_lark_body(self):
        return ''


if __name__ == '__main__':
    # common parser
    project_name = 'project'
    report_title = 'project项目 自动化回归报告'

    args = parser.parse_args()
    default_owner_str = project_ownership.project_owner_dict[project_name]
    receiver_list_str = args.receivers or default_owner_str
    receiver_list = receiver_list_str.split(',') if receiver_list_str else []

    runner = ProjectRunner(project_name, report_title, group_id=args.group_id, report_receiver_list=receiver_list)

    # 自定义后续操作 是否copy到远程，是否发送IM
    # is_scp_to_remote = False
    # is_send_IM = False
    # runner = CONTRunner(project_name, report_title, group_id=args.group_id, report_receiver_list=receiver_list, is_scp_to_remote=is_scp_to_remote, is_send_IM=is_send_IM)

    runner.run()




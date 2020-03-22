# encoding: utf-8
from base import project_ownership
from runner.base_args import parser
from runner.base_runner_test import BaseRunnerTest
from test_suite import project_case_suite
from concurrent.futures import ProcessPoolExecutor
from runner.merge_html import MergeHtml
import time


class ProjectConcurrentBaseRunner(BaseRunnerTest):
    # 保留该类用于BaseRunnerTest方法调试
    pass

def run(suite=None):
    runner = ProjectConcurrentBaseRunner(project_name, report_title, group_id=args.group_id,
                       report_receiver_list=receiver_list, suite=suite)
    runner.run()

def process_pool_runner():
    start_time = time.time()
    tasks = []

    with ProcessPoolExecutor(max_workers=5) as pool:
        for suite in [suite_test for suite_test in project_case_suite.pack_suite()]:
            tasks.append(pool.submit(run, suite))

    end_time = time.time()
    duration = end_time - start_time
    deal_with_results(duration)


def deal_with_results(duration):
    merge_report_file_name = ProjectConcurrentBaseRunner.generate_merge_report_file_name(project_name=project_name)
    start_time, pass_rate, total, _pass, failure, error \
        = MergeHtml().merge_html(project_name=project_name, duration=duration,
                                 merge_report_file_name=merge_report_file_name)

    runner_for_IM = ProjectConcurrentBaseRunner(project_name, report_title, group_id=args.group_id, report_receiver_list=receiver_list)

    runner_for_IM.post_after_merge(pass_rate=pass_rate, total=total, _pass=_pass,
                                     failure=failure, error=error, merge_report_file_name=merge_report_file_name)


if __name__ == '__main__':
    # common parser
    project_name = 'project'
    report_title = 'project项目 自动化回归报告'

    args = parser.parse_args()
    receiver_list = args.receivers.split(',') if args.receivers else []

    process_pool_runner()






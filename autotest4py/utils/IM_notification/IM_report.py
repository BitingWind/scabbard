# encoding: utf-8

def format_simple_summary(unittest_results):
    """
    单测报告 数据简单加工
    :param unittest_results: 单测结果类
    :return: 结果组合 msg，测试通过率
    """
    # total_case = unittest_results.testsRun
    success_case = unittest_results.success_count
    fail_case = unittest_results.failure_count
    error_case = unittest_results.error_count
    total_case = success_case + fail_case + error_case

    pass_rate = round(float(success_case * 100) / float(total_case), 2)
    msg_str = u"Pass rate ： {} %\nPass : {}\nError : {}\nFailure : {}\nTotal : {}\n".format(pass_rate,
                                                                                            success_case,
                                                                                            error_case, fail_case,
                                                                                            total_case)
    return msg_str, pass_rate

def format_report_for_temporary_test(pass_rate, total_case, pass_case, failure_case, error_case):
    pass_rate = pass_rate
    total_case = total_case
    pass_case = pass_case
    failure_case = failure_case
    error_case = error_case

    msg_str = u"Pass rate ： {} %\nPass : {}\nFailure : {}\nError : {}\nTotal : {}\n".format(pass_rate,pass_case,
                                                                                            failure_case, error_case, total_case)
    return msg_str, pass_rate




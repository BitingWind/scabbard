# encoding: utf-8


# 去除dict中的指定field，暴力方式，非屏蔽直接抹掉
def case_list(l, fileds):
    """
    如果是list,得遍历里面看是不是dict来判断需不需要剔除
    """
    for i in l:
        if isinstance(i, dict):
            case_dict(i, fileds)
        if isinstance(i, list):
            case_list(i, fileds)


def case_dict(m, fileds):
    """
    如果是一个dict，递归遍历
    """
    ks = []
    for k, v in m.items():
        if k in fileds:
            # 需要剔除的，先记下来，遍历完了之后做剔除
            ks.append(k)
        else:
            if isinstance(v, dict):
                case_dict(v, fileds)
            if isinstance(v, list):
                case_list(v, fileds)

    for i in ks:
        del m[i]


# 原文链接：https://blog.csdn.net/u010080628/java/article/details/79538420
class JsonCompare:
    def __init__(self, expect_data, real_data, is_debug=False):
        self.expect_data = expect_data
        self.real_data = real_data
        self.data_compare_result = []  # 数据对比结果
        self.frame_compare_result = []  # 结构对比结果
        self.default_root = ''
        self.compare(expect_data, real_data, self.default_root)
        if is_debug:
            for i in self.data_compare_result: print(i)
            for i in self.frame_compare_result: print(i)

    def compare(self, expect_data, real_data, path='/'):
        try:
            if not isinstance(expect_data, (list, tuple, dict)):
                # 这里兼容下小数时而不同的情况，这里也有可能存在不同类型的微小差别
                if not str(expect_data) == str(real_data):
                    msg = '%s:预期值:%s%s,实际值:%s%s' % (path, str(expect_data), type(expect_data), str(real_data), type(real_data))
                    self.data_compare_result.append(msg)
            elif isinstance(expect_data, (list, tuple)):  # list,tuple
                if not isinstance(real_data, (list, tuple)):
                    raise IndexError('实际数据不是list:%s' % path)  # 实际数据为非list/tuple类型
                for index, value in enumerate(expect_data):
                    try:
                        if index < len(real_data):
                            self.compare(value, real_data[index], '%s[%d]' % (path, index))
                        else:
                            raise IndexError('不存在的下标：%s[%d]' % (path, index))
                    except Exception as e:
                        if IndexError:
                            self.frame_compare_result.append('结构异常or数据缺失:%s' % e.args)
                        else:
                            self.frame_compare_result.append('未知异常:%s' % e.args)
            else:  # dict
                if not isinstance(real_data, dict):
                    raise IndexError('实际数据不是dict:%s' % path)  # 实际数据为非dict类型
                for key,value in expect_data.items():
                    try:
                        if key in real_data.keys():
                            self.compare(value, real_data[key], '%s[\'%s\']' % (path, str(key)))
                        else:
                            raise IndexError('不存在的键：%s[\'%s\']' % (path, str(key)))
                    except Exception as e:
                        if IndexError:
                            self.frame_compare_result.append('结构异常or数据缺失:%s' % e.args)
                        else:
                            self.frame_compare_result.append('未知异常:%s' % e.args)
        except Exception as e:
            self.frame_compare_result.append('未知异常:%s' % e.args)

    def is_full_consistent(self):
        return len(self.data_compare_result) == 0 and len(self.frame_compare_result) == 0

    def print_diff(self):
        for i in self.data_compare_result:
            print(i)
        for i in self.frame_compare_result:
            print(i)


if __name__ == '__main__':
    master_dict = {"model_type":"event","metadata_id":"mid_api","table_conf":{"dims":[{"field_key":"2930","source_table":None,"field_name":"中间层分析查询结果","field_type":"string","dim_type":"custom"}],"indexs":[{"field_key":"count_all:mid_api","field_name":"中间层埋点[总次数]","unit":"","accuracy":"","is_percent":False}],"precise_remove_repetition":False,"user_groups":[]},"sample_ratio":1,"data_resource_id":2459,"uin_conf":{"field_key":"id","uin_type":"business_account"},"filters":{"logic":"and","wheres":[{"operator":"-is","value":"web_api,open_api","type":None,"field_key":"api_request_type","metadata_id":"mid_api","source_table":None,"custom_field_key":None},{"operator":"-is","value":"release_in","type":None,"field_key":"environment","metadata_id":"mid_api","source_table":None,"custom_field_key":None}]},"chart_type":"bar","chart_conf":{"limit":"1000","chart_show_type":None,"merge_date":None,"query_date":{"localDateTimes":None,"date_range":"24","date_type":"hour","date_format":"1","date_group":"","relative_type":0},"query_date_compare":None,"order_by":[{"field_key":"2930","field_type":"dim","source_table":None,"rule":"desc"}],"show_group":[],"index_filter":[],"secondary_y_axis":[]}}
    candidate_dict = {"uin_conf": {"field_key": "id", "uin_type": "business_account"}, "data_resource_id": 2459, "table_conf": {"dims": [{"field_key": "2930", "source_table": None, "field_name": "\u4e2d\u95f4\u5c42\u5206\u6790\u67e5\u8be2\u7ed3\u679c", "dim_type": "custom", "field_type": "string"}], "user_groups": [], "precise_remove_repetition": False, "indexs": [{"field_key": "count_all:mid_api", "is_percent": False, "field_name": "\u4e2d\u95f4\u5c42\u57cb\u70b9[\u603b\u6b21\u6570]", "unit": "", "accuracy": ""}]}, "chart_type": "pie", "filters": {"wheres": [{"custom_field_key": None, "source_table": None, "value": "web_api,open_api", "operator": "-is", "field_key": "api_request_type", "metadata_id": "mid_api", "type": None}, {"custom_field_key": None, "source_table": None, "value": "release_in", "operator": "-is", "field_key": "environment", "metadata_id": "mid_api", "type": None}], "logic": "and"}, "chart_conf": {"order_by": [{"field_key": "count_all:mid_api", "source_table": None, "rule": "desc", "field_type": "index"}], "index_filter": [], "query_date_compare": None, "secondary_y_axis": [], "show_group": [], "limit": "1000", "query_date": {"date_format": "1", "relative_type": 0, "date_type": "hour", "date_range": "24", "date_group": "", "localDateTimes": None}, "chart_show_type": None, "merge_date": None}, "model_type": "event", "metadata_id": "page_visit", "sample_ratio": 1.0}
    json_compare_result = JsonCompare(master_dict, candidate_dict)
    if not json_compare_result.is_full_consistent():
        print(u'-----------------------------------【DIFF FAIL】不一致结果: -----------------------------------')
        # Json 错误结果输出
        json_compare_result.print_diff()
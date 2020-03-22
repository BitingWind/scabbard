# encoding: utf-8


# 这个data用来存储时间比较久的 request 信息
# 数据格式为 request_data
# request_list 里面元素数据格式如下
# request_dict={'request':    ; 'time': time}
request_list = []

request_path_set = set()

time_cost_threshold = 1  # 请求超时监控的阈值！单位是秒！


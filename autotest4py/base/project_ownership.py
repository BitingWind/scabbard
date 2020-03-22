# encoding: utf-8
# 目录维护了项目与owner 之间的关系,方便发送IM

project_owner_dict = {}

project_owner_dict['project'] = 'shuangxing.zhang'


def get_owner_dict(project_partial_name):
    pro_key = None
    for project in project_owner_dict.keys():
        if project in project_partial_name:
            pro_key = project
            break

    if not pro_key:
        print(u"ERROR")
    return project_owner_dict[pro_key]


def get_receiver_set_by_project_name(project_name):
    receivers_str = project_owner_dict.get(project_name, '')
    return set(receivers_str.split(',')) if receivers_str else set()

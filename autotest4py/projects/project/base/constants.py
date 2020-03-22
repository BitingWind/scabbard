# encoding: utf-8
def make_de_dict(original_dict):
    '''
    把某一个dict，key 与 value反转并且增加到当前 dict里面
    '''
    copy_dict = original_dict.copy()
    for key, value in copy_dict.items():
        original_dict[value] = key
    return original_dict

"""
固化参数
"""
param_dict = dict()
name_1 = 1 # u'名称1'
name_2 = 2 # u'名称2'
param_dict[name_1] = u'名称1'
param_dict[name_2] = u'名称2'
# 反转存储
make_de_dict(param_dict)

param_list = []
param_list.append(name_1)
param_list.append(name_2)



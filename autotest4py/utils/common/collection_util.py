# encoding: utf-8
import random
from copy import deepcopy

from utils.common.log_util import LogUtil


class CollectionUtil(object):

    @staticmethod
    def get_random_from_list(list):
        '''
        随机从一个list里面，拿去一个item
        :param list:   目标list需要输入，必填
        :return:
        '''
        if len(list) < 1:
            return None
        elif len(list) == 1:
            return list[0]
        else:
            seed = random.randint(1, len(list)) - 1
            return list[seed]

    @staticmethod
    def get_last_item_from_list(list):
        '''
        随机从一个list里面，拿去最后一个item
        :param list:   目标list需要输入，必填
        :return:
        '''
        return list[-1] if len(list) > 0 else None

    @staticmethod
    def get_random_size_list(my_list, list_size=None):
        '''
        从一个list里面，生成随机大小的子集list；
        比如： [2,5,7,9] 可能随机的结果是 [2,5], 也可能是[5,7,9]
        :param my_list: 原始list
        :param list_size: 期望拿到的输出的list 长度，必须要小于原始list长度
        :return:
        '''
        if list_size is not None:
            if list_size > len(my_list):
                raise Exception("期望得到的list_size，超过了当前list 最大值 - {}！！！".format(len(list)))
            how_many = list_size
        else:
            if len(my_list) < 1:
                LogUtil.error("当前应该有错误，需要看一下 this_list: {}".format(str(my_list)))
                raise Exception(u" 期望de this_list长度小于1！！！")
            how_many = random.randint(1, len(my_list))

        tmp_list = deepcopy(my_list)
        final_list = []
        for i in xrange(how_many):
            rand_item = tmp_list[random.randint(1, len(tmp_list)) - 1]

            final_list.append(rand_item)
            tmp_list.pop(tmp_list.index(rand_item))

        return final_list

    @staticmethod
    def shuffle_a_list(my_list):
        '''
        打散 my_list 的顺序 修改原参数
        '''
        random.shuffle(my_list)

    @staticmethod
    def list_to_string_with_comma(my_list):
        """
        list 转化为 str 去除前后 []
        """
        return str(my_list)[1:-1]

    @staticmethod
    def list_to_string_with_comma_no_space(my_list):
        """
        逗号分隔 list return str
        """

        if not my_list:
            return ""
        return str(my_list)[1:-1].replace(' ', '')

    @staticmethod
    def string_to_list_splited_by_comma(str):
        """
        逗号分隔的string 转成list 去除空格
        :param str:
        :return:
        """
        if ',' not in str:
            return [str]

        my_list = []
        array = str.split(',')
        for item in array:
            my_list.append(item.strip())

        return my_list

    @staticmethod
    def get_max_in_list(my_list):
        '''
        抽取list里面最大的一个 不改变原值
        '''
        if len(my_list) <= 0:
            raise Exception(u"当前list为空！ ERROR")
        max = 0

        for item in my_list:
            if item >= max:
                max = item

        return max

    @staticmethod
    def contained_in_list(list_sub, list_father):
        '''
        list_sub 是否 完全是 list_father 的自己
        '''
        contained = True
        for item in list_sub:
            if item not in list_father:
                # 一旦发现不一样,就return false
                return False
            # 全部跑完了,是子集
        return contained

    @staticmethod
    def get_same_item_in_former_list(list1, list2):
        '''
        然后两个list 里面的 交集部分
        '''

        return list(set(list1).intersection(set(list2)))

    @staticmethod
    def get_same_item_between_sets(set1, set2):
        '''
        两个set 里面的 交集部分
        '''
        return set1 & set2

    @staticmethod
    def get_all_item_between_sets(set1, set2):
        '''
        两个set 里面的 并集部分
        '''
        return set1 | set2

    @staticmethod
    def get_diff_tiem_between_sets(set1, set2):
        '''
        两个set 里面差集的部分
        :param set1:
        :param set2:
        :return:
        '''
        return CollectionUtil.get_all_item_between_sets(set1, set2) - CollectionUtil.get_same_item_between_sets(set1,
                                                                                                                set2)

    @staticmethod
    def are_same_sets(set1, set2):
        '''
        两个set 是否完全一致
        '''
        if CollectionUtil.get_all_item_between_sets(set1, set2) == CollectionUtil.get_same_item_between_sets(set1,
                                                                                                             set2):
            return True
        else:
            return False

    @staticmethod
    def get_diff_item_in_former_list(list1, list2):
        '''
        left join，list 1 里面元素，找到不在list2 里面对应值，塞到list 里面返回
        '''
        diff_item_list_in_list1 = []
        for item in list1:
            if item not in list2:
                diff_item_list_in_list1.append(item)

        return diff_item_list_in_list1

    @staticmethod
    def get_length_larger_list(list1, list2):
        """
        返回更长的list
        """
        return list1 if len(list1) >= len(list2) else list2

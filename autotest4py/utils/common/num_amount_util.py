# encoding: utf-8
import random
from decimal import Decimal

from utils.common.log_util import LogUtil


class NumberUtil(object):
    """
    主要用于数字，金额等数据生成，加工
    """

    # 随机任何一个数字类型，正数与小数 随机返回
    # 强烈推荐 在数字加和的地方 使用
    @staticmethod
    def get_any_number(max, base=0, less_than=False):
        '''
        随机生成任何一个数字类型：50%概率生成整数，50%概率生成小数
        :param max: 期望随机的上限
        :param base: 从什么值开始
        :param less_than:true- 不能等于最大值,默认是false,可以随机等于最大值。
        :return:
        '''

        return NumberUtil.get_any_amount(max, less_than=less_than) + base if random.randint(0,
                                                                                            1) else NumberUtil.get_any_int(
            max, less_than=less_than) + base

    @staticmethod
    def get_any_amount(max, less_than=False):
        '''
        随机生成一个保留两位小数的浮点数
        :param max: 期望随机的上线。
        :return:
        '''
        if less_than:
            max = float(max) - 0.01

        if max <= 0:  # 1:
            raise Exception(u"[FATAL] max需要大于等于1！")
        randNumb = random.randint(1, int(max * 100))
        return float(round(Decimal(randNumb) / 100, 2))

    @staticmethod
    def get_any_int(max, less_than=False, base=0):
        '''
        随机生成一个整正数
        最大为 base + max
        less_than表示是否可包含上限
        '''
        if less_than:
            max = int(max) - 1

        if max < 1:
            raise Exception(u"[FATAL] max需要大于等于1！")

        randNumb = random.randint(1, int(max))
        return int(randNumb) + base

    @staticmethod
    def get_range_amount(l, h):
        '''
        随机生成任何区间的，保留两位小数的数字
        :param l: 随机下限
        :param h: 随机上限
        :return:
        '''
        return round(random.uniform(l, h), 2)

    @staticmethod
    def get_number_serial(length=None):
        '''
        随机生成一个数字序列号 返回 str 至少3位
        '''
        if length == None:
            return str(random.randint(19999999999999, 99999999999999))

        elif length > 3:
            number_of_zero = length - 1
            start_serial = "1{}".format("".rjust(number_of_zero, str('0')))
            start_long = long(start_serial)
            end_serial = "1{}".format("".rjust(length, str('0')))
            end_long = long(end_serial) - 1
            randNumb = random.randint(start_long, end_long)
        else:
            raise Exception(u'[ERROR]目前只支持三维以上随机数生成！！！')

        LogUtil.info(u"使用随机生成的长传数字：  " + str(randNumb))
        return randNumb

    @staticmethod
    def convert_number_to_fit_data_warehouse(number):
        '''
        把当前数字,转换为数仓需要的格式, 100000*number
        :param number:
        :return:
        '''

        # 处理一下尾差问题
        tmp_num = number * 100000
        tail = tmp_num % 1000
        if tail >= 500:
            result = (int(tmp_num / 1000) + 1) * 1000
        else:
            result = (int(tmp_num / 1000)) * 1000

        return result

    # 类似微信红包的方法，输入总金额amount，期望的list长度，随机拆分总和amount的两位小数的list
    @staticmethod
    def gen_random_list_with_total_amount(amount, list_size):
        '''
        随机生成一个微信红包，返回一个float类型的list （当年入职，就被李瑶面试了这道题目）
        :param amount: 红包总金额
        :param list_size: 期望拆分的个数
        :return:
        '''

        at_least_amount = list_size * 0.01
        result_list = []

        if amount <= 0:
            raise Exception(u"输入最大金额不可以为非正数 ：  amount ：{}, list_size : {}".format(amount, list_size))

        if amount < at_least_amount:
            raise Exception(u"以一分为单位，当前金额，不足以拆分这么多list ：  amount ：{}, list_size : {}".format(amount, list_size))
        elif amount == at_least_amount:  # 分为单位，刚好相等，直接拆分最小单位，范围
            for i in xrange(0, list_size):
                result_list.append(0.01)
            return result_list

        else:  # 分为单位，随机均分拆分

            total_amount = amount * 100
            current_list_size = list_size
            for i in xrange(list_size):
                if i == list_size - 1:
                    result_list.append(float(total_amount) / 100)
                    break
                current_amount = NumberUtil.__get_next_amount(total_amount, current_list_size)
                result_list.append(float(current_amount) / 100)
                total_amount = total_amount - current_amount
                current_list_size = current_list_size - 1

            return result_list

    @staticmethod
    def get_random_proportion():
        """
        获取分成比例 百分比
        :return:
        """
        i = random.randint(0, 100)
        return float(i) / 100

    @staticmethod
    def format_amount_with_serial(amount):
        '''
        金额，转换，如果是 正数，返回int，如果是小数，返回string
        :param amount:
        :return:
        '''
        result = None
        amount = round(float(amount), 2)
        amount_str = str(amount)
        if '.' in amount_str:

            small_part = amount_str.split('.')[1]

            if '00' in small_part or '0' == small_part:
                result = int(amount)
            else:
                result = str(amount)

        else:
            result = int(amount)

        return result

    @staticmethod
    def __get_next_amount(current_amount, current_list_size):
        # 需要乘以100进来，最小单位是1，代表1分
        mini_unit = 1

        remain_amount = int(current_amount - ((current_list_size - 1) * mini_unit))
        current_amount = random.randint(1, remain_amount)

        return current_amount


if __name__=="__main__":
    print float(1)/3
    print NumberUtil.convert_number_to_fit_data_warehouse(float(1)/3)


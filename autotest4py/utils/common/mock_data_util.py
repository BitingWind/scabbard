# encoding: utf-8
import random
import time

from constants import people_dict
from utils.common.log_util import LogUtil


class MockDataUtil(object):

    @staticmethod
    def get_name(sale_id=None):
        '''
        随机生成一个名称，有Auto关键字
        :param sale_id: 不填写没东西，如果填写了虚拟人员id，会拼写虚拟人员中文名
        :return:
        '''
        ticks = str(int(time.time()))
        # ran = str(random.randint(0, 50000))

        if sale_id:
            name = people_dict.get_name_by_id(sale_id)
        else:
            name = u"名字"
        name = u"Auto-{}{}".format(name, ticks)
        LogUtil.info(u"随机生成的名称： {}".format(name))
        return name

    @staticmethod
    def get_email():
        '''
        随机生成一个可用的邮箱
        :return:
        '''
        randNumb = random.randint(1, 9999999)
        mail = "auto.mail.{}@bytedance.com".format(randNumb)

        LogUtil.info(u"使用随机生成的email ：  " + str(mail))
        return mail

    @staticmethod
    def get_mobile_number():
        '''
        随机生成一个手机号码
        :return:
        '''
        str = random.randint(1000000, 9999999)
        return "1340{}".format(str)

    @staticmethod
    def get_pure_number_serials(n):
        '''
        随机生成一个长度为10的字符串
        :return:
        '''
        _str = ''
        if n > 0:
            min = 10 ** n
            max = 10 ** n + 10 * (n - 1)
            _str = str(random.randint(min, max))
        return _str

    @staticmethod
    def execute_occasionally(occur_probability=50):
        '''
        概率执行的方法,probability=50,是发生概率百分比  在0,100 之间
        :param probability: 发生概率 百分比, 默认是 一般发生,一般不发生
        :return:
        '''
        if occur_probability > 100 or occur_probability < 0:
            raise Exception(u"发生概率不可以超过100或小于0")

        seed = random.randint(1, 100)

        if seed <= occur_probability:
            return True
        else:
            return False

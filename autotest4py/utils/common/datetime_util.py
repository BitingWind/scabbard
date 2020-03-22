# encoding: utf-8
import calendar
import datetime
import random
import time
import pytz
from datetime import timedelta

# 时间格式
FORMAT_DAY = '%Y-%m-%d'
FORMAT_SECOND = '%Y-%m-%d %H:%M:%S'
DATE_ID_STR = "%Y%m%d"

# 常用时区
TIMEZONE_UTC = pytz.timezone('UTC')
TIMEZONE_SHANGHAI = pytz.timezone('Asia/Shanghai')
TIMEZONE_BEIJING = pytz.timezone('Asia/Shanghai')
TIMEZONE_NEW_YORK = pytz.timezone('America/New_York')


class DatetimeUtil(object):
    """
    时间处理工具
    """

    # ---------------------
    # 获取当前时间 timestamp
    # ---------------------

    @staticmethod
    def fmt_current_time():
        """
        str 1949-10-01 00:00:00
        """
        return datetime.datetime.now().strftime(FORMAT_SECOND)

    @staticmethod
    def fmt_current_date():
        """
        1949-10-01
        """
        return datetime.datetime.now().strftime(FORMAT_DAY)

    @staticmethod
    def str_to_date(date_str):
        """
        1949-10-01 -> date(1949, 10, 1)
        """
        return datetime.datetime.strptime(date_str, FORMAT_DAY)

    @staticmethod
    def date_to_str(date):
        """
        date(1949, 10, 1) -> 1949-10-01
        """
        return date.strftime(FORMAT_DAY)

    @staticmethod
    def get_any_two_day_in_a_month(year=None, month=None):
        if not year:
            year = datetime.date.today().year
        else:
            year = year
        if not month:
            month = datetime.date.today().month
        else:
            month = month
        week_dat, month_count_day = calendar.monthrange(year, month)
        first_day = datetime.date(year, month, day=1)
        last_day = datetime.date(year, month, day=month_count_day)
        start_date = first_day + datetime.timedelta(days=random.randint(0, 14))
        start_date = start_date.strftime('%Y-%m-%d')
        end_date = last_day + datetime.timedelta(days=random.randint(-14, 0))
        end_date = end_date.strftime('%Y-%m-%d')
        return start_date, end_date

    @staticmethod
    def get_any_date(future_date=None, delta_day_number=None, is_timestamp=False, from_start_date_str=None,
                     plus_day=None):
        '''
        随机生成任意一个日期类型的str 比如'2019-01-01' 或者输入当前日期的时间戳
        :param future_date: 是否是未来日期？ 置空=默认拿取今天
        :param delta_day_number: 加减天数，置空=不加减。
        :param is_timestamp: 是否返回时间戳？否的话，输出'2019-01-01'
        :param from_start_date_str:
        :return:
        '''

        if from_start_date_str is None:
            start_date = datetime.date.today()
        else:
            start_date = datetime.datetime.strptime(str(from_start_date_str),
                                                    '%Y-%m-%d')  # str(from_start_date_str).strftime('%Y-%m-%d')

        if plus_day == None:
            if future_date == None:
                ran_plus = 0
            elif future_date == True:
                if delta_day_number == None:
                    ran_plus = random.randint(1, 60)
                else:
                    ran_plus = delta_day_number
            else:
                if delta_day_number == None:
                    ran_plus = random.randint(-60, -1)
                else:
                    ran_plus = -delta_day_number
        else:
            ran_plus = plus_day

        result_date = start_date + datetime.timedelta(days=ran_plus)

        format_date = result_date.strftime('%Y-%m-%d')

        if not is_timestamp:
            return str(format_date)
        else:
            timestamp = int(time.mktime(datetime.datetime.strptime(str(format_date), '%Y-%m-%d').timetuple()))
            return (timestamp)

    @staticmethod
    def get_current_date_time_str():
        '''
        获取当前时间的时间戳
        :return:
        '''
        result_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        return result_str

    @staticmethod
    def get_current_month_last_date_str(date_str):
        '''
        获取当月的最后一天date str
        比如：'2019-01-21' ，期望输出为'2019-01-31'
        :param date_str:
        :return:
        '''

        next_month_first_day = DatetimeUtil.get_next_month_first_date_str(date_str)
        result_date = DatetimeUtil.get_any_date(future_date=False, delta_day_number=-1,
                                        from_start_date_str=next_month_first_day)

        return result_date

    @staticmethod
    def get_next_month_first_date_str(date=None):
        '''
        获取当月的最后一天date str 输入可兼容date示例，或者date string
        比如：'2019-01-21' ，期望输出为'2019-02-01'
        特殊场景：输入'2019-12-01'，输出为'2020-01-01'
        :param date:
        :return:
        '''
        date_str = date
        if not date:
            date_str = DatetimeUtil.fmt_current_date()
        if isinstance(date, datetime.date):
            date_str = DatetimeUtil.date_to_str(date)

        date_str_list = date_str.split('-')

        year = date_str_list[0]
        month = date_str_list[1]

        if str(month) == str(12):
            next_month = '01'
            next_year = int(year) + 1  # 跨年了，需要增加
            year = str(next_year)
        else:
            next_month = str(int(month) + 1)

        next_month_first_day = "{}-{}-01".format(year, next_month)

        return next_month_first_day

    @staticmethod
    def data_str_to_bigint(date_str):

        '''
        日期string格式，转换为数仓专用的bigint 格式，
        比如：'2019-01-21' 转换为 '20190121'
        :param date_str: '日期 string'
        :return:
        '''
        num = date_str.split('-')
        result = 0
        result += int(num[0]) * 10000
        result += int(num[1]) * 100
        result += int(num[2]) * 1

        return result

    @staticmethod
    def date_bitint_to_string(date_int):
        '''
        输入是 20190701，转换成 2019-07-01
        '''
        x = str(datetime.datetime.strptime(str(date_int),
                                           '%Y%m%d'))
        return x.split(' ')[0]

    @staticmethod
    def get_last_month_end_date_str(date_str):
        '''
        获取当月的上一个月最后一天date str
        比如：'2019-02-21' ，期望输出为'2019-01-31'；
        特殊场景：输入'2019-12-01'，输出为'2020-01-01'
        :param date_str:
        :return:
        '''
        this_month_first_date = DatetimeUtil.get_this_month_first_date_str(date_str)

        return DatetimeUtil.get_any_date(future_date=True, from_start_date_str=this_month_first_date, delta_day_number=-1)

    @staticmethod
    def get_this_month_first_date_str(date_str):
        '''
        获取当前月 第一天
        :param date_str:
        :return:
        '''

        date_str_list = date_str.split('-')

        year = date_str_list[0]
        month = date_str_list[1]

        this_month_first_day = "{}-{}-01".format(year, month)

        return this_month_first_day

    @staticmethod
    def get_first_day_of_this_month():
        '''获取当月第一天，例如：2019-07-01'''
        year = datetime.datetime.today().year
        month = datetime.datetime.today().month
        first_day = datetime.date(year, month, day=1)
        return first_day

    @staticmethod
    def get_first_day_of_this_year():
        '''获取本年第一天，例如：2019-01-01'''
        year = datetime.datetime.today().year
        month = 1
        first_day = datetime.date(year, month, day=1)
        return str(first_day)

    @staticmethod
    def get_last_day_of_this_year():
        '''获取本年 最后一天，例如：2019-12-31'''
        year = datetime.datetime.today().year
        month = 12
        last_day = datetime.date(year, month, day=31)
        return str(last_day)

    @staticmethod
    def get_this_month():
        '''返回当前月，例如：2019-07'''
        return datetime.datetime.strftime(datetime.datetime.today(), "%Y-%m")

    @staticmethod
    def sleep_for_what(sec=3):
        sleep_sec = sec
        while sleep_sec > 0:
            time.sleep(1)
            print(u"...   sleep 1 sec   ...")
            sleep_sec -= 1

    @staticmethod
    def now_time_delta_time(delta_days, is_utc0=False):
        """
        构造具体当前delta的时间:
        delta_days > 0 截止日期比当前时间晚
        delta_days < 0 截止日期比当前时间早
        :param delta_days:
        :param is_utc0: 是否utc0时间：当前localtime -8H
        :return:
        """
        now = datetime.now()
        nDays = timedelta(days=delta_days)
        delta_now = now + nDays
        if is_utc0:
            delta_now = delta_now + timedelta(hours=-8)
        return delta_now.strftime('%Y-%m-%d %H:%m:%S')

    @staticmethod
    def data_str_to_bigint(date_str):
        '''
        日期string格式，转换为数仓专用的bigint 格式，
        比如：'2019-01-21' 转换为 '20190121'
        :param date_str: '日期 string'
        :return:
        '''
        num = date_str.split('-')
        result = 0
        result += int(num[0]) * 10000
        result += int(num[1]) * 100
        result += int(num[2]) * 1

        return result

    @staticmethod
    def get_delta_of_two_date(start_date, end_date):
        """
        获取两个日期之差
        :param start_date: "2010-10-01"
        :param end_date: "2010-10-10"
        :return: int 9
        """
        start = datetime.datetime.strptime(start_date, FORMAT_DAY)
        end = datetime.datetime.strptime(end_date, FORMAT_DAY)
        return (end - start).days

    @staticmethod
    def date_to_datetime(date_obj):
        """
        转化date实例 成为 datetime 实例，用以数据库层查出来后的转换
        :param date: 如datetime.date(2020, 1, 1)
        :return: datetime.date(2020, 1, 1, 0, 0)
        """
        return datetime.datetime.combine(date_obj, datetime.time.min)


if __name__=='__main__':
    print(DatetimeUtil.get_any_two_day_in_a_month())
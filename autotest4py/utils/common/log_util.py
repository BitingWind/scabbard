# encoding: utf-8
import datetime
import json
import traceback

class LogUtil(object):
    """
    case日志输出 格式工具类
    ！！！注意：此类禁止引用本工程内其他类。以免造成循环引用！！！
    """

    @staticmethod
    def info(msg):
        """
        grab global LogUtil
        """
        LogUtil._base_level_print(msg)

    @staticmethod
    def debug(msg):
        """
        grab global LogUtil
        """
        LogUtil._base_level_print(msg, level="DEBUG")

    @staticmethod
    def warn(msg):
        """
        grab global LogUtil
        """
        LogUtil._base_level_print(msg, level="WARN")

    @staticmethod
    def error(msg):
        """
        grab global LogUtil
        """
        LogUtil._base_level_print(msg, level="ERROR")

    @staticmethod
    def exception(msg, e):
        """
        grab global LogUtil
        """
        LogUtil._base_level_print(msg, level="Exception")
        if e and isinstance(e, Exception):
                e_str = traceback.format_exc()
                print e_str

    @staticmethod
    def _base_level_print(msg, level="INFO", need_time=False):
        """
        grab global LogUtil
        """
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') if need_time else ''
        print u"[{}] {} {}".format(level, current_time, msg)


    @staticmethod
    def step(desc=None):
        """
        grab global LogUtil
        """
        print u"\n\n\n================【CASE STEP】================================"
        if desc:
            print u"          {}".format(desc)
            print u"================================================"

    @staticmethod
    def verify(desc=None):
        """
        添加 Console Handler 用以 HTMLRunner 收集
        """
        print u"\n\n\n================【CASE VERIFY】================================"
        if desc:
            print u"           {}".format(desc)
            print u"================================================"

    @staticmethod
    def print_fmt_json(obj, desc=None):
        """
        json 格式化数据，不建议输出超大json
        :param obj:
        :return:
        """
        print u"---------------------\n【Print JSON】【{}】".format(desc if desc else "")
        print "\n"
        print json.dumps(obj, default=lambda o: o.__dict__, indent=2).decode('unicode-escape')
        print "\n"

    @staticmethod
    def print_dict_in_lines(my_dict, desc=None, max_key_lenth=30):
        '''
        按照行打印 一个dict中的每一个元素
        :param my_dict:  一个字典对象
        :param max_key_lenth:   当前key 到 ：（双引号） 之间的最大距离，默认是30，可以更改
        :return:
        '''

        print u"\n------------------------ Print DICT【{}】------------------".format(desc if desc else "")

        if len(my_dict) == 0 or my_dict == None:
            print u"        No data ..."

        else:
            keys = my_dict.keys()
            for key in keys:
                try:
                    spaces = LogUtil._gen_spaces(len((str(key))),
                                                       max_key_lenth)  # self._gen_spaces(len(str(key), max_key_lenth))
                except Exception:
                    spaces = u"     "

                value = my_dict[(key)]
                print u"    {}{}  :  {} ".format(spaces, key, value.__repr__().decode(u"unicode-escape"))

                # print u"    {}  :  {} ".format(key, my_dict[key])

            print u"----------------------------------------------------\n"

    @staticmethod
    def _gen_spaces(key_lenth, max_key_lenth):
        # 格式化，data print
        default_key_lenth = max_key_lenth
        spaces_count = default_key_lenth - key_lenth
        spaces = u""

        for i in xrange(spaces_count):
            spaces += u" "

        return spaces

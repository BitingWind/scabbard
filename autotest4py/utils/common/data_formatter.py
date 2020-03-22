# encoding: utf-8
import json


class DataFormatter:
    def print_dict_in_lines(self, my_dict, max_key_lenth=30):
        '''
        按照行打印 一个dict中的每一个元素
        :param my_dict:  一个字典对象
        :param max_key_lenth:   当前key 到 ：（双引号） 之间的最大距离，默认是30，可以更改
        :return:
        '''

        print(u"----------------------------------------------------\n【Print】printing dict detailed data in lines。。。")

        if len(my_dict) == 0 or my_dict == None:
            print(u"        No data ...")

        else:
            keys = my_dict.keys()
            keys.sort()

            for key in keys:
                try:
                    spaces = self._gen_spaces(len((str(key))),
                                              max_key_lenth)  # self._gen_spaces(len(str(key), max_key_lenth))
                except Exception:
                    spaces = u"     "

                value = my_dict[(key)]
                print(u"    {}{}  :  {} ".format(spaces, key, value.__repr__().decode(u"unicode-escape")))

                # print u"    {}  :  {} ".format(key, my_dict[key])

            print(u"----------------------------------------------------\n")

    def print_obj_in_lines(self, obj, max_key_lenth=30):
        '''
        按照行打印,已个obj对象里面的所有dict元素
        特别适用于，某一个detial接口获取的data 结果，比如 contract,customer 等或者一个 DB Model对象
        :param obj:  一个对象
        :param max_key_lenth:   key 到 ：（双引号） 之间的最大距离，默认是30，可以更改
        :return:
        '''

        DataFormatter().print_dict_in_lines(obj.__dict__, max_key_lenth=max_key_lenth)

    def _gen_spaces(self, key_lenth, max_key_lenth):
        # 格式化，data print
        default_key_lenth = max_key_lenth
        spaces_count = default_key_lenth - key_lenth
        spaces = u""

        for i in range(spaces_count):
            spaces += u" "

        return spaces

    def print_list_in_lines(self, list):
        '''
        按照行打印 一个list中的每一个元素

        :param list: 待打印的list对象
        :return:
        '''

        print(u"----------------------------------------------------\n【Print】printing list detailed data in lines。。。")

        if list == None:
            print(u"        No data ...")
        else:
            for item in list:
                print(u"   {} ".format(item.__repr__().decode(u"unicode-escape")))
        print(u"----------------------------------------------------\n")

    def list_content_to_str(self, my_list):
        '''
        list 内容，中间拼接 逗号， 输出string
        :param my_list: 原始list
        :return:
        '''
        result = ""
        flag_for_first = True
        for item in my_list:
            if flag_for_first:
                result = item
                flag_for_first = False
            else:
                result = "{},{}".format(result, item)
        return result

    def obj_2_format_json_str(self, obj, indent=2):
        """
        将类的实例转换为格式化的json，
        :param obj: 类实例对象
        :param indent: 格式缩进
        """
        return json.dumps(obj, default=lambda o: o.__dict__, indent=indent).decode('unicode-escape')

    def format_float_with_human_friendly(self, my_float):
        return round(float(my_float), 2)

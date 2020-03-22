# encoding: utf-8
import datetime
import json
import time

import requests

from base.common_decorator import statistic_request_url
from utils.common.log_util import LogUtil


class MyRequests(object):
    u'''封装requests， 打印请求详情'''

    @staticmethod
    @statistic_request_url
    def get(url, headers=None, cookies=None, params=None):
        u'HTTP get 请求'

        my_cookies = MyRequests._update_default_cookie_for_auth(cookies)

        # request details
        request_obj = MyRequests.log_request_details(url, headers=headers, cookies=my_cookies, params=params,
                                                     method=u"GET")

        start = datetime.datetime.now()
        req = requests.get(url, headers=headers, cookies=my_cookies, params=params)
        MyRequests._record_performance(start, request_obj)
        MyRequests.log_response_details(req)

        return req

    @staticmethod
    @statistic_request_url
    def post(url, headers=None, params=None, cookies=None, data=None, is_json=False, files=None, json_data=None):
        my_cookies = MyRequests._update_default_cookie_for_auth(cookies)

        if is_json:
            if not headers:
                headers = {"content-type": "application/json"}
            else:
                headers['content-type'] = "application/json"
            data = json.dumps(data)

        request_obj = MyRequests.log_request_details(url, headers=headers, cookies=my_cookies, params=params,
                                                     data=data,
                                                     method=u"POST",
                                                     json_data=json_data)
        start = datetime.datetime.now()

        req = requests.post(url, headers=headers, cookies=my_cookies, params=params, data=data, files=files,
                            json=json_data)
        MyRequests._record_performance(start, request_obj)
        MyRequests.log_response_details(req)

        return req

    @staticmethod
    @statistic_request_url
    def put(url, headers=None, params=None, cookies=None, data=None, is_json=False):
        my_cookies = MyRequests._update_default_cookie_for_auth(cookies)

        if is_json:
            if not headers:
                headers = {"content-type": "application/json"}
            else:
                headers['content-type'] = "application/json"
            data = json.dumps(data)

        request_obj = MyRequests.log_request_details(url, headers=headers, cookies=my_cookies, params=params,
                                                     data=data,
                                                     method=u"PUT")
        start = datetime.datetime.now()
        rsp = requests.put(url, headers=headers, cookies=my_cookies, params=params, data=data)
        MyRequests._record_performance(start, request_obj)

        # response details
        MyRequests.log_response_details(rsp)

        return rsp

    @staticmethod
    def delete(url, headers=None, params=None, cookies=None, data=None):
        my_cookies = MyRequests._update_default_cookie_for_auth(cookies)

        request_obj = MyRequests.log_request_details(url, headers=headers, cookies=my_cookies, params=params,
                                                     data=data,
                                                     method=u"DELETE")
        start = datetime.datetime.now()

        req = requests.delete(url, headers=headers, cookies=my_cookies, params=params, data=data)

        MyRequests._record_performance(start, request_obj)
        # response details
        MyRequests.log_response_details(req)

        return req

    @staticmethod
    def log_request_details(url=None, headers=None, cookies=None, params=None, data=None, json_data=None, method=None):
        LogUtil.info("-----[REQUEST] details below : ----------------------------")

        time_stamp = datetime.datetime.now()
        LogUtil.info("  Current time  : {}".format(time_stamp.strftime('%Y.%m.%d-%H:%M:%S')))

        LogUtil.info("  Request : {}".format(url))

        if headers:
            LogUtil.info("  Headers : {}".format(headers))
        if cookies:
            LogUtil.info("  Cookies : {}".format(cookies))
        if params:
            try:
                LogUtil.info("  Parameters : {}".format(params.__repr__().decode("unicode-escape")))
            except:
                LogUtil.info("  Parameters : {}".format(params))

        if method:
            LogUtil.info("  Method : {}".format(method))
        if data:
            try:
                LogUtil.info("  Payload : {}".format(data.__repr__().decode("unicode-escape")))
            except:
                LogUtil.info("  Payload : {}".format(data))

        if json_data:
            try:
                LogUtil.info("  Payload-json : {}".format(json_data.__repr__().decode("unicode-escape")))
            except:
                LogUtil.info("  Payload-json : {}".format(json_data))

        request_obj = {}
        request_obj['url'] = url
        request_obj['method'] = method
        request_obj['headers'] = headers
        request_obj['cookies'] = cookies
        request_obj['parameters'] = params
        request_obj['payload'] = data
        return request_obj

    @staticmethod
    def log_response_details(response_body):
        LogUtil.info("-----[RESPONSE] details below : ----------------------------")

        LogUtil.info('Returned code: {}'.format(response_body.status_code))

        if response_body.status_code != 200:
            LogUtil.info(
                "[WARN]Return code is not 200!!!! but {} .".format(
                    response_body.status_code))

            err_msg = response_body.text
            try:
                json_body = response_body.json()
                s = str(json_body).replace('u\'', '\'')
                LogUtil.info('  Response: ')
                LogUtil.info(s.decode('unicode-escape'))
                err_msg = s.decode('unicode-escape')
            except Exception as e:
                LogUtil.error('Response raw data: ')
                LogUtil.exception(err_msg, e)

            LogUtil.error(u"\n【FATAL ERROR】检查请求细节是否出错，或者服务器是否有问题\n      ---->>  {}".format(err_msg))

        else:
            try:
                json_body = response_body.json()
                s = str(json_body).replace('u\'', '\'')
                LogUtil.info('  Response: ')
                LogUtil.info(s.decode('unicode-escape'))

            except:
                LogUtil.info(u'  Response raw data: \n{}'.format(response_body.text))
                raise Exception("http请求的返回不是Json格式，检查服务器是否有问题")

        LogUtil.info("------------------------------------------------------------------------")

    @staticmethod
    def _update_default_cookie_for_auth(cookies):
        """
        处理权限相关的cookie内容，加载缓存中的current info 切换人员。
        :param cookies: 原来的cookie
        :param is_json:
        :return:
        """
        my_auth_cookies = dict(common_param='%s' % '123_param')
        if cookies:
            my_auth_cookies.update(cookies)
        return my_auth_cookies

    @staticmethod
    def _record_performance(start, request_obj):
        """
        记录性能相关，如果超过阈值，记录下来请求内容
        """
        end = datetime.datetime.now()
        diff_seconds = (end - start).total_seconds()
        LogUtil.info(u"-----------------------------------------------")
        LogUtil.info(u"【性能】请求花费时间 {} s ".format(diff_seconds))
        LogUtil.info(u"-----------------------------------------------")

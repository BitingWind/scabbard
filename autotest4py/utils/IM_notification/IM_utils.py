# encoding=utf-8

import requests
import json

# user token
default_user_token = "ghjk"
# bot token
default_bot_token = "oiuythgjk"


class IMUtils:

    def __init__(self, user_token=None, bot_token=None):
        self.user_token = user_token or default_user_token
        self.bot_token = bot_token or default_bot_token

    def get_group_of_user(self, user_token):
        """
        获取开发者所在的群组列表
        :param user_token: 开发得token
        :return:
        """
        pass

    def create_bot(self, user_token):
        """
        创建一个机器人
        :param user_token: 开发者token
        :return:
        """
        pass

    def get_userid(self, bot_token, email_prefix):
        """
        获取开发者的userid
        :param bot_token: 开发者创建的一个机器人的token
        :param email_prefix: 开发者的邮箱前缀
        :return:
        """
        pass

    def __bot_join_group(self, user_token, bot_token, group_id):
        """
        把机器人拉到一个群里去
        :param user_token:  开发者token
        :param bot_token: 机器人token
        :param group_id: 群ID，通过调用get_group_of_user(user_token)获取
        :return:
        """
        pass

    def create_session(self, bot_token, userid):
        """
        创建一个私人会话ID
        :param bot_token: 机器人token
        :param userid: 准备跟谁聊天，调get_userid(bot_token, email_prefix)
        :return:
        """
        pass

    def __chat_with_person(self, bot_token, chat_id, message, title):
        """
        跟一个人（或一个群）聊天
        :param bot_token: 机器人token
        :param chat_id: 如果跟群聊天，则chat_id就是群的groupid；如果跟个人聊天，chat_id需要通过create_session(bot_token, userid)来创建
        :param message: 必填字段
        :param title: 必填字段
        :return:
        """
        pass

    def send_msg_to_group(self, title, msg, group_id=None):
        """
        专属的发送给 IM群的通知，默认先增加到一个群
        """
        self.__chat_with_person(self.bot_token, group_id, msg, title)

        return

    def send_msg_to_person(self, title, msg, user_email_prefix):
        """
        给个人发送消息, user_email_prefix 为完整的邮箱前缀
        这里量小，暂不做user id 和session id的缓存，走每次获取
        """
        pass

    def join_a_group(self, group_id):

        print(u"尝试加入下面的群，群ID为： {}\n".format(group_id))
        self.__bot_join_group(self.user_token, self.bot_token, group_id)


    def bot_join_group(self, group_id, user_token=None, bot_token=None):
        """
        把机器人拉到一个群里去
        :param user_token:  开发者token
        :param bot_token: 机器人token
        :param group_id: 群ID，通过调用get_group_of_user(user_token)获取
        :return:
        """
        pass
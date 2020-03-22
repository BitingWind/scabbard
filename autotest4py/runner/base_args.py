# encoding: utf-8

import argparse

# 非线程安全 通用参数模式
parser = argparse.ArgumentParser(description="For API Auto test common args, format: [options] <args>")

# 暂时仅支持一个 group id
parser.add_argument('-g', '--group_id', type=int, help='Api Report Group Id')
parser.add_argument('-r', '--receivers', help='Api Report Email Prefix List of Personal Receivers, Split by [,]')


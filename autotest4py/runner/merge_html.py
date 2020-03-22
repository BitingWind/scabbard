# encoding: utf-8
import glob
from pyquery import PyQuery as pq
from test_env_config import ROOT_DIR
from utils.common.log_util import LogUtil


class MergeHtml:

    def encode_utf8(self, string):
        return string.encode('utf-8')

    # local 参数本地调试时使用，已关闭入口，不要打开
    def merge_html(self, project_name, duration, merge_report_file_name, local=False):
        reports = {}
        index = 0
        head_list = []
        import os
        _re = project_name + '*html*'
        file_path = os.path.join(ROOT_DIR, "report", _re)
        for file in glob.glob(file_path):
            LogUtil.info(file)
            reports[index] = file
            index += 1

            d = pq(filename=file, parser='html')
            if not d:
                continue
            head_list.append(d('div').filter(".heading")('.attribute').text().split())

        start_time = min([head[2] for head in head_list]) + ' ' + min([head[3] for head in head_list])
        duration = duration
        total = sum([int(head[13]) for head in head_list])

        _pass = sum([int(head[17]) for head in head_list if head[15] == 'Pass'])
        # python 2.7 两个整数相除结果为整数，需要将至少一个转换为浮点数
        pass_rate = round(float(_pass) / total * 100, 2)
        failure = sum(int(head[head.index('Failure') + 2]) for head in head_list if 'Failure' in head)
        error = sum(int(head[head.index('Error') + 2]) for head in head_list if 'Error' in head)

        message = u"""
        <html>
            <head>
              <body>
                {0}
                <div>
                {1}
                </div>
              </body>
            </head>
        </html>"""

        head = u"""
                <div class='heading'>
                    <h1>{} API Automation Test Report</h1>
                    <p class='attribute'><strong>Start Time:</strong> {}</p>
                    <p class='attribute'><strong>Duration:</strong> {}min {}s</p>
                    <p class='attribute'><strong>Pass Rate:</strong> {} %</p>
                    <p class='attribute'><strong>Statistics:</strong> Total: {};  Pass: {};  Failure: {};   Error: {}; </p>
                    <p class='description'></p>
                </div>
                """.format(project_name.upper(), start_time, int(duration)/60, int(duration)%60, pass_rate, total, _pass, failure, error)

        insert = []
        for k, v in reports.items():
            if not local:
                v = v.split('/')[-1]
            insert.append('<iframe id={} class="contentView" '
                          'style="width: 100%;height: 400px;overflow: hidden;border: none;" '
                          'src="{}"></iframe>'.format(k,v))

        res = message.format(head, ''.join(insert))


        # # 生成合并后的文件名

        merge_full_path = os.path.join(ROOT_DIR, "report", merge_report_file_name)

        with open(merge_full_path, "w") as merge_file:
            merge_file.write(self.encode_utf8(res))

        return start_time, pass_rate, total, _pass, failure, error
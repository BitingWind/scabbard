# encoding: utf-8
from projects.project.ops.db_1_ops import DB1Ops
from projects.project.test_case.common_verify.base_verify import BaseVerify
from projects.project.test_data_prepare.test_data_prepare import TestDataPrepare
from utils.common.log_util import LogUtil


class CaseClass2(BaseVerify):

    def setUp(self):
        self.test_data_prepare = TestDataPrepare()
        self.db_cont_ops = DB1Ops()

    def test_2(self):
        """\
        说明\
        <br> 步骤与校验\
        <br> 1. 步骤 校验\
        <br> 2. 步骤 校验\
        <br> 3. 步骤 校验\
        """
        LogUtil.step(u"步骤1")
        param = self.db_cont_ops.get_first_info(1, 'name')

        LogUtil.verify(u"校验1")
        self.verify_1(param)

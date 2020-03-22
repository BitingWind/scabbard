# encoding: utf-8
from projects.project.env_config import DB_1_Session
from projects.project.model.table_model import TableModel


class DB1Ops(object):
    '''
    通过DB查询信息
    '''

    def get_one_info(self, param):
        """sql 查询单个"""
        sql_str = 'SELECT a, b, c from table WHERE param = {}'.format(param)
        cont = DB_1_Session().execute(sql_str).first()
        self._check_has_one_result(sql_str, cont)
        return cont

    def get_list_info(self, param):
        """sql 查询多个"""
        sql_str = 'SELECT a, b, c from table WHERE param = {}'.format(param)
        cont = DB_1_Session().execute(sql_str).fetchall()
        return [_['template_id'] for _ in cont]

    def get_first_info(self, id, name):
        """model 查询，过滤"""
        result = DB_1_Session.query(TableModel)\
            .filter(TableModel.id == id, TableModel.name == name)\
            .order_by(TableModel.id.asc()).limit(100).all()

        if len(result) == 0:
            raise Exception(u"查询不到 参数{}-{}".format(id, name))

        return int(result[0].id), result[0].name

    def _check_has_one_result(self, sql_str, first_result):
        if first_result:
            return
        msg = u"[ERROR] 没有找到符合条件的内容，查看sql ： \n{}".format(sql_str)
        raise Exception(msg)
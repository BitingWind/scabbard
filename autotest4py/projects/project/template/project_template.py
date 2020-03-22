from projects.project.ops.db_1_ops import DB1Ops


class ProjectTemplate(object):

    def get_post_api_payload(self, id, name):
        # db ops api ops combine
        data = {}
        data['param_1'] = 'param'
        data['param_2'] = DB1Ops().get_first_info(id, name)
        return data
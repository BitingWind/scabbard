# encoding: utf-8
import random
from projects.project.test_data_prepare.test_data_prepare import TestDataPrepare


class EntityX(object):
    """template ops combine to prepare by builder pattern"""

    def __init__(self, builder):
        # condition
        self.type2 = builder.type2
        self.type1 = builder.type1
        self.name = builder.name

        # result
        self.id = None
        self.type_no = None

    def __str__(self):
        return ''

    class Builder(object):
        """builder for entity x"""

        def __init__(self):
            self.type2 = 'type2'
            self.type1 = 123
            self.name = 'random_{}'.format(random.randint(10000, 99999))

        def with_type2(self, type2):
            self.type2 = type2
            return self

        def with_type1(self, type1):
            self.type1 = type1
            return self

        def with_name(self, name):
            self.name = name
            return self

        def build_up(self):
            x = EntityX(self)
            TestDataPrepare.construct_x_entity(x)
            return x


if __name__ == '__main__':
    x = EntityX.Builder()\
        .with_name('xx')\
        .with_type1(23)\
        .with_type2('sss')\
        .build_up()


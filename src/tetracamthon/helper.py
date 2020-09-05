import pickle

from sympy import symbols


class Variable(object):
    def __init__(self, name):
        self.name = name
        self.sym = symbols(name)
        self.val = None
        self.exp = None

    def set_value(self, value):
        self.val = value

    def set_expression(self, expression):
        self.exp = expression


class Memory(object):
    def __init__(self, name):
        self.dict = {}
        self.name = name
        self.save()  # init a data file

    def save(self):
        output = open(
            '/Users/johnqu/PycharmProjects/'
            'Tetracamthon/data/memo_{}.pkl'.format(self.name), 'wb')
        pickle.dump(self.dict, output)
        output.close()

    def load(self):
        pkl_file = open(
            '/Users/johnqu/PycharmProjects/'
            'Tetracamthon/data/memo_{}.pkl'.format(self.name), 'rb')
        self.dict = pickle.load(pkl_file)
        pkl_file.close()
        return self.dict

    def has_object(self, name):
        return name in self.dict

    def is_same_object(self, obj):
        return obj is self.dict[obj.name]

    def add_obj(self, key, value):
        self.dict[key] = value

    def get_obj(self, key):
        return self.dict[key]

    def update_memo(self, key, value):
        self.add_obj(key, value)
        self.save()


import pickle

from sympy import symbols
import matplotlib.pyplot as plt
import numpy as np


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


def save_attribute_to_pkl(name, data):
    output = open(
        '/Users/johnqu/PycharmProjects/'
        'Tetracamthon/data/memo_{}.pkl'.format(name), 'wb')
    pickle.dump(data, output)
    output.close()


def load_attribute_from_pkl(name):
    pkl_file = open(
        '/Users/johnqu/PycharmProjects/'
        'Tetracamthon/data/memo_{}.pkl'.format(name), 'rb')
    result = pickle.load(pkl_file)
    pkl_file.close()
    return result


def move_sympy_plot_to_plt_axes(p, ax):
    backend = p.backend(p)
    backend.ax = ax
    backend.process_series()
    backend.ax.spines['right'].set_color('none')
    backend.ax.spines['bottom'].set_position('zero')
    backend.ax.spines['top'].set_color('none')
    plt.close(backend.fig)


def trans_degree_to_time(degree, cycle_time=0.9):
    degree_to_time_ratio = cycle_time / 360.0
    return np.array(degree) * degree_to_time_ratio


def trans_time_to_degree(time, cycle_time=0.9):
    time_to_degree_ratio = 360.0 / cycle_time
    return np.array(time) * time_to_degree_ratio



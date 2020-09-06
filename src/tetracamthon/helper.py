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


def plot_subplots_on_one_figure(sp_curve_lis_of_diff_depth,
                                common_knots,
                                name='',
                                whether_save_png=False,
                                whether_show_figure=False,
                                whether_knots_ticks=True,
                                ):
    cur_lis = sp_curve_lis_of_diff_depth
    knots = common_knots
    fig, axs = plt.subplots(nrows=len(cur_lis),
                            figsize=(16, 10),
                            )
    fig.suptitle('PVAJ Curves \n {}'.format(name),
                 fontsize=14, fontweight='bold')
    y_labels = [
        "Position\n(mm)",
        "Velocity \n(mm/sec)",
        "Acceleration \n(mm/sec^2)",
        "Jerk \n(mm/sec^3)"
    ]
    for i in range(len(axs)):
        move_sympy_plot_to_plt_axes(cur_lis[i], axs[i])
        axs[i].set_ylabel(y_labels[i])
        axs[i].tick_params(labelcolor='tab:gray')
        axs[i].set_xlabel('machine degree')
        if whether_knots_ticks:
            axs[i].set_xticks([knots[i] for i in range(len(knots))])
            axs[i].set_xticklabels([(i % 2) * '\n' +
                                    str(round(
                                        trans_time_to_degree(knots[i]), 1))
                                    for i in range(len(knots))])
        else:
            axs[i].set_xticks(trans_degree_to_time(
                np.linspace(0, 360, 37, endpoint=True)))
            axs[i].set_xticklabels([(i % 2) * '\n' + str(
                int(np.linspace(0, 360, 37, endpoint=True)[i]))
                                    for i in range(37)])
        axs[i].grid(True)
    fig.align_ylabels(axs)
    if whether_save_png:
        plt.savefig('../plot/plot_of_{}.png'.format(name), dpi=720)
    if whether_show_figure:
        plt.show()
    return fig, axs

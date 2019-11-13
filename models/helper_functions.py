from sympy import pi
import numpy as np
import matplotlib.pyplot as plt


def degree_to_radial(degree):
    return np.array(degree) / 180 * pi


def radial_to_degree(radial):
    return np.array(radial) / pi * 180


def degree_to_time(degree, cycle_time=0.9):
    degree_to_time_ratio = cycle_time / 360.0
    return np.array(degree) * degree_to_time_ratio


def radial_to_time(radial, cycle_time=0.9):
    radial_to_time_ratio = cycle_time / (2 * pi)
    return np.array(radial) * radial_to_time_ratio


def time_to_degree(time, cycle_time=0.9):
    time_to_degree_ratio = 360.0 / cycle_time
    return np.array(time) * time_to_degree_ratio


def time_to_radial(time, cycle_time=0.9):
    time_to_radial_ratio = 2 * pi / cycle_time
    return np.array(time) * time_to_radial_ratio


def time_to_time(time, cycle_time=0.9):
    return np.array(time)


def move_sympyplot_to_axes(p, ax):
    backend = p.backend(p)
    backend.ax = ax
    backend.process_series()
    backend.ax.spines['right'].set_color('none')
    backend.ax.spines['bottom'].set_position('zero')
    backend.ax.spines['top'].set_color('none')
    plt.close(backend.fig)


def duplicate_start_end(a, num):
    b, c = [], []
    for i in range(num):
        b.append(a[0])
        c.append(a[-1])
    d = list(a[1:-1])
    return b + d + c


def print_list_items_in_row(li):
    """
    a = [1,2,3]
    b = ['a', 'b', 'c']
    print_list_items_in_row(a)
    print_list_items_in_row(b)
    :param li: list
    :return: None
    """
    for i in range(len(li)):
        print(str(i) + 'th: ' + str(li[i]))


def plot_pvaj(pvaj,
              knots,
              name='',
              whether_save_png=False,
              whether_show_figure=False,
              whether_knots_ticks=True,
              ):
    """
    s1 = SplineWithPiecewisePolynomial()
    s1.update_with_solution()
    s1.plot_svaj()
    """
    fig, axs = plt.subplots(nrows=4,
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
        move_sympyplot_to_axes(pvaj[i], axs[i])
        axs[i].set_ylabel(y_labels[i])
        axs[i].tick_params(labelcolor='tab:gray')
        axs[i].set_xlabel('machine degree')
        if whether_knots_ticks:
            axs[i].set_xticks([knots[i] for i in range(len(knots))])
            axs[i].set_xticklabels([(i % 2) * '\n' +
                                    str(round(time_to_degree(knots[i]), 1))
                                    for i in range(len(knots))])
        else:
            axs[i].set_xticks(degree_to_time(
                np.linspace(0, 360, 37, endpoint=True)))
            axs[i].set_xticklabels([(i % 2) * '\n' + str(
                int(np.linspace(0, 360, 37, endpoint=True)[i]))
                                    for i in range(37)])
        axs[i].grid(True)
    fig.align_ylabels(axs)
    if whether_save_png:
        plt.savefig('plot_of_{}.png'.format(name), dpi=720)
    if whether_show_figure:
        plt.show()
    return fig, axs


def find_index_in_ordered_list(value, li):
    for i in range(len(li) - 1):
        if li[i] <= value < li[i + 1]:
            return i

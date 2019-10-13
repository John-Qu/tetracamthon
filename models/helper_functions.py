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



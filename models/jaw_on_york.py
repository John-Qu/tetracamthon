from sympy import symbols, nan, diff, lambdify, Eq
from sympy.abc import x, y
import numpy as np
import matplotlib.pyplot as plt


def degree_to_time(degree, cycle_time=0.9):
    degree_to_time_ratio = cycle_time / 360.0
    return np.array(degree) * degree_to_time_ratio


def time_to_degree(time, cycle_time=0.9):
    time_to_degree_ratio = 360.0 / cycle_time
    return np.array(time) * time_to_degree_ratio


class Coefficients(object):
    def __init__(self, piece_id, order=6):
        self.c = []
        self.m = order
        for i in range(self.m, 0, -1):
            self.c.append(symbols('C_' + str(piece_id) + str(i)))

    def __str__(self):
        return str(self.c)


class ClassicalSplines(object):
    def __init__(self, knots, order, pva):
        self.pe, self.ve, self.ae, self.je, self.pie = [], [], [], [], []
        self.pf, self.vf, self.af, self.jf, self.pif = [], [], [], [], []
        self.co = []
        self.var = []
        self.knots = knots
        self.order = order
        self.degree = self.order - 1
        self.exprs = [self.pe, self.ve, self.ae, self.je, self.pie]
        self.funcs = [self.pf, self.vf, self.af, self.jf, self.pif]
        self.equations = []
        self.pva = pva

    def get_expr(self):
        for i in range(1, len(self.knots)):
            self.co.append(Coefficients(i))
            p_i = self.co[-1].c[-1]
            self.var.append(self.co[-1].c[0])
            for j in range(degree):
                p_i += self.co[-1].c[j] \
                       * (y - self.knots[i - 1]) ** (self.degree - j)
                self.var.append(self.co[-1].c[j + 1])
            v_i = diff(p_i, y)
            a_i = diff(v_i, y)
            jerk_i = diff(a_i, y)
            ping_i = diff(jerk_i, y)
            self.pe.append(p_i)
            self.ve.append(v_i)
            self.ae.append(a_i)
            self.je.append(jerk_i)
            self.pie.append(ping_i)
        return self.exprs

    def get_function(self):
        exprs = self.get_expr()
        for i in range(len(self.knots) - 1):
            for j in range(len(exprs)):
                self.funcs[j].append(lambdify(y, exprs[j][i]))
        return self.funcs

    def build_boundary_conditions(self):
        f = self.get_function()
        for i in range(3):
            self.equations.append(Eq(f[i][0](self.knots[0]).evalf(),
                                     self.pva[i][0]))
            self.equations.append(Eq(f[i][-1](self.knots[-1]).evalf(),
                                     self.pva[i][-1]))

    def build_interpolation_conditions(self, dict_inter_knots):
        """
        :param dict_inter_knots: {1:[0, 1], 2:[0]}
        :return:
        """
        f = self.get_function()
        for i in dict_inter_knots.keys():
            for j in dict_inter_knots[i]:
                self.equations.append(Eq(f[j][i](self.knots[i]).evalf(),
                                         self.pva[j][i]))

    def build_smoothness_conditions(self, loose_knots_ids):
        """
        :param loose_knots_ids: [1]
        :return:
        """
        f = self.get_function()
        for i in range(1, len(self.knots) - 1):
            for j in range(5 if i not in loose_knots_ids else 4):
                self.equations.append(
                    Eq(f[j][i - 1](self.knots[i]).evalf(),
                       f[j][i](self.knots[i]).evalf()))


if __name__ == "__main__":
    order = 6
    degree = order - 1
    knots = degree_to_time(np.array([0, 73, 120, 168]))
    positions = np.array([0, -131, -41.1, 0])
    velocities = np.array([0, 0, nan, 0])
    accelerations = np.array([0, nan, nan, 0])
    pva = [positions, velocities, accelerations]
    cp = ClassicalSplines(knots, order, pva)


# These codes were out-off date, replaced by
# "splines_building.py" and "curves_building.py".

from sympy import symbols, nan, diff, lambdify, Eq, solve, latex, \
    Piecewise, plot
from sympy.abc import x, y
import numpy as np
import matplotlib.pyplot as plt
from helper_functions import degree_to_time, time_to_degree, \
    move_sympyplot_to_axes


class Coefficients(object):
    def __init__(self, piece_id, order=6):
        self.c = []
        self.m = order
        for i in range(self.m, 0, -1):
            self.c.append(symbols('C_' + str(piece_id) + str(i)))

    def __str__(self):
        return str(self.c)


class ClassicalSplines(object):
    def __init__(self, knots, order, pvaj):
        self.pe, self.ve, self.ae, self.je, self.pie = [], [], [], [], []
        self.pf, self.vf, self.af, self.jf, self.pif = [], [], [], [], []
        self.p, self.v, self.a, self.j, self.pi = [], [], [], [], []
        self.co = []
        self.var = []
        self.knots = knots
        self.order = order
        self.degree = self.order - 1
        self.exprs = [self.pe, self.ve, self.ae, self.je, self.pie]
        # self.funcs = [self.pf, self.vf, self.af, self.jf, self.pif]
        self.funcs = [[] for i in range(self.order)]
        self.solved_expr = [self.p, self.v, self.a, self.j, self.pi]
        self.equations = []
        self.pvaj = pvaj
        self.exprs_of_x = [[] for i in range(self.degree)]
        self.piecewise_of_x = []
        for index_of_piece in range(0, len(self.knots)-1):
            self.co.append(Coefficients(index_of_piece, order=self.order))
            p_i = self.co[-1].c[-1]
            self.var.append(self.co[-1].c[0])
            for index_of_depth in range(self.degree):
                p_i += self.co[-1].c[index_of_depth] \
                       * (y - self.knots[index_of_piece - 1]) ** \
                       (self.degree - index_of_depth)
                self.var.append(self.co[-1].c[index_of_depth + 1])
            v_i = diff(p_i, y)
            a_i = diff(v_i, y)
            jerk_i = diff(a_i, y)
            ping_i = diff(jerk_i, y)
            self.pe.append(p_i)
            self.ve.append(v_i)
            self.ae.append(a_i)
            self.je.append(jerk_i)
            self.pie.append(ping_i)
        for index_of_piece in range(len(self.knots) - 1):
            for index_of_depth in range(len(self.exprs)):
                self.funcs[index_of_depth].append(
                    lambdify(y, self.exprs[index_of_depth][index_of_piece]))

    def build_boundary_conditions(self, bc_depth):
        f = self.funcs
        for i in range(bc_depth):
            self.equations.append(Eq(f[i][0](self.knots[0]).evalf(),
                                     self.pvaj[i][0]))
            self.equations.append(Eq(f[i][-1](self.knots[-1]).evalf(),
                                     self.pvaj[i][-1]))

    def build_interpolation_conditions(self, dict_inter_knots):
        """
        :param dict_inter_knots: {1:[0, 1], 2:[0]}
        :return:
        """
        f = self.funcs
        for i in dict_inter_knots.keys():
            for j in dict_inter_knots[i]:
                self.equations.append(Eq(f[j][i](self.knots[i]).evalf(),
                                         self.pvaj[j][i]))

    def build_smoothness_conditions(self, loose_knots):
        """
        :param loose_knots_ids: [1]
        :return:
        """
        f = self.funcs
        for i in range(1, len(self.knots) - 1):
            for j in range(self.degree if i not in loose_knots else self.degree - loose_knots[i]):
                self.equations.append(
                    Eq(f[j][i - 1](self.knots[i]).evalf(),
                       f[j][i](self.knots[i]).evalf()))

    def build_not_at_knot_conditions(self, index_of_piece,
                                     control_point, index_of_depth, value):
        f = self.funcs
        self.equations.append(Eq(f[index_of_depth][index_of_piece]
                                     (control_point).evalf(), value))

    def build_expressions(self, solutions, latex_print_out=False):
        for k in range(self.degree):
            for i in range(len(self.knots) - 1):
                self.solved_expr[k].append(self.exprs[k][i].subs(
                    [(self.co[i].c[j], solutions[self.co[i].c[j]]) for j in
                     range(self.order)]))
        if latex_print_out:
            for i in range(len(self.knots) - 1):
                print(latex(self.solved_expr[i]))

    def get_solved_expressions(self):
        return self.solved_expr

    def shift_curve(self, delta1, delta2):
        exprs_of_y = self.get_solved_expressions()
        for k in range(len(exprs_of_y)):
            self.exprs_of_x[k] += [exprs_of_y[k][i].subs(y, x + delta1)
                                   for i in range(len(self.knots) - 1)]
            self.exprs_of_x[k].append(exprs_of_y[k][0].subs(y, x - delta2))

    def get_exprs_of_x(self):
        return self.exprs_of_x

    def make_piecewise_curve(self):
        exprs_of_x = self.get_exprs_of_x()
        for k in range(5):
            self.piecewise_of_x.append(Piecewise(
                (0, x < 0),
                (exprs_of_x[k][0], x <= degree_to_time(43)),
                (exprs_of_x[k][1], x <= degree_to_time(82)),
                (exprs_of_x[k][2], x <= degree_to_time(138)),
                (0, x <= degree_to_time(330)),
                (exprs_of_x[k][3], x <= degree_to_time(360)),
                (0, True)))

    def make_piecewise_curve2(self):
        exprs_of_x = self.get_exprs_of_x()
        for k in range(5):
            self.piecewise_of_x.append(Piecewise(
                (0, x < 0),
                (exprs_of_x[k][0], x <= degree_to_time(43)),
                (exprs_of_x[k][1], x <= degree_to_time(138)),
                (0, x <= degree_to_time(330)),
                (exprs_of_x[k][2], x <= degree_to_time(360)),
                (0, True)))


    def get_piecewise_of_x(self):
        return self.piecewise_of_x

    def get_functional_position(self):
        return lambdify(x, self.get_piecewise_of_x()[0])

    def get_functional_velocity(self):
        return lambdify(x, self.get_piecewise_of_x()[1])

    def get_functional_acceleration(self):
        return lambdify(x, self.get_piecewise_of_x()[2])

    def get_functional_jerk(self):
        return lambdify(x, self.get_piecewise_of_x()[3])

    def plot_numerical(self, num=100):
        t = np.linspace(0, degree_to_time(360),
                        num, endpoint=True)
        degree = time_to_degree(t)
        position = self.get_functional_position()(t)
        velocity = self.get_functional_velocity()(t)
        acceleration = self.get_functional_acceleration()(t)
        jerk = self.get_functional_jerk()(t)
        fig = plt.figure(figsize=(15, 12), dpi=80)
        fig.suptitle('SVAJ curves of Jaw on York, with knots on \n' +
                     str(time_to_degree(self.knots) - 30),
                     fontsize='xx-large')
        plt.subplot(4, 1, 1)
        plt.grid()
        plt.ylabel("Position (mm)")
        plt.plot(degree, position,
                 color="blue", linewidth=3.0, linestyle="-")
        plt.xlim(0.0, 360.0)
        plt.xticks(np.linspace(0, 360, 37, endpoint=True))
        # plt.ylim(min(position)-10, max(position)+10)
        # plt.yticks(np.linspace(-2000, 2000, 9, endpoint=True))
        plt.subplot(4, 1, 2)
        plt.grid()
        plt.ylabel("Velocity (mm/s)")
        plt.plot(degree, velocity,
                 color="blue", linewidth=3.0, linestyle="-")
        plt.xlim(0.0, 360.0)
        plt.xticks(np.linspace(0, 360, 37, endpoint=True))
        # plt.ylim(min(position)-10, max(position)+10)
        # plt.yticks(np.linspace(-2000, 2000, 9, endpoint=True))
        plt.subplot(4, 1, 3)
        plt.grid()
        plt.ylabel("Acceleration (m/s^3)")
        plt.plot(degree, acceleration / 1000,
                 color="blue", linewidth=3.0, linestyle="-")
        plt.xlim(0.0, 360.0)
        plt.xticks(np.linspace(0, 360, 37, endpoint=True))
        # plt.ylim(min(position)-10, max(position)+10)
        # plt.yticks(np.linspace(-2000, 2000, 9, endpoint=True))
        plt.subplot(4, 1, 4)
        plt.grid()
        plt.ylabel("Jerk (m/s^4)")
        plt.plot(degree, jerk / 1000,
                 color="blue", linewidth=3.0, linestyle="-")
        plt.xlim(0.0, 360.0)
        plt.xticks(np.linspace(0, 360, 37, endpoint=True))
        # plt.ylim(min(position)-10, max(position)+10)
        # plt.yticks(np.linspace(-2000, 2000, 9, endpoint=True))
        plt.savefig("svaj_of_jaw_on_york.png", dpi=720)


def build_jaw_on_york_curves(if_print=False, if_plot=False):
    order = 6
    degree = order - 1
    knots = degree_to_time(np.array([0, 73, 112, 168]))
    positions = np.array([0, -131, -41.1, 0])
    velocities = np.array([0, 0, nan, 0])
    accelerations = np.array([0, nan, nan, 0])
    jerks = np.array([0, nan, nan, 0])
    pvaj = [positions, velocities, accelerations, jerks]
    cp = ClassicalSplines(knots, order, pvaj)
    cp.build_boundary_conditions(bc_depth=3)
    cp.build_interpolation_conditions({1: [0, 1], 2: [0]})
    # cp.build_smoothness_conditions({1:2, 2:1})
    cp.build_smoothness_conditions({1: 1})
    solutions = solve(cp.equations, cp.var)
    cp.build_expressions(solutions, latex_print_out=False)
    delta1 = degree_to_time(30)
    delta2 = degree_to_time(330)
    cp.shift_curve(delta1, delta2)
    cp.make_piecewise_curve()
    curves = cp.get_piecewise_of_x()
    if if_print:
        for i in range(len(curves)):
            print(latex(curves[i]))
    if if_plot:
        cp.plot_numerical(num=3600)
    return cp

def build_jaw_on_york_curves2(if_print=False, if_plot=False):
    order = 6
    degree = order - 1
    knots = degree_to_time(np.array([0, 73, 168]))
    positions = np.array([0, -131, 0])
    velocities = np.array([0, 0, 0])
    accelerations = np.array([0, nan, 0])
    jerks = np.array([0, 0, 0])
    pvaj = [positions, velocities, accelerations, jerks]
    cp = ClassicalSplines(knots, order, pvaj)
    cp.build_boundary_conditions(bc_depth=3)
    cp.build_interpolation_conditions({1: [0, 1]})
    cp.build_smoothness_conditions({1:1})
    # cp.build_smoothness_conditions({1:2})
    # cp.build_not_at_knot_conditions(index_of_piece=0,
    #                                 control_point=degree_to_time(50),
    #                                 index_of_depth=3, value=0)
    solutions = solve(cp.equations, cp.var)
    cp.build_expressions(solutions, latex_print_out=False)
    delta1 = degree_to_time(30)
    delta2 = degree_to_time(330)
    cp.shift_curve(delta1, delta2)
    cp.make_piecewise_curve2()
    if if_print:
        for i in range(len(curves)):
            print(latex(curves[i]))
    if if_plot:
        cp.plot_numerical(num=3600)
    return cp

if __name__ == "__main__":
    build_jaw_on_york_curves2(if_print=True, if_plot=True)

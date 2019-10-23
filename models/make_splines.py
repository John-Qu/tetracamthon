from sympy import symbols, nan, diff, lambdify, Eq, solve, latex, \
    Piecewise, integrate, cot, acos, sqrt
from sympy.abc import x, y
from sympy.plotting import plot
import numpy as np
import matplotlib.pyplot as plt
from helper_functions import degree_to_time, time_to_degree, \
    move_sympyplot_to_axes
from analysis import O4DriveA
from packages import Package


class Coefficients(object):
    def __init__(self, piece_id, order=6):
        self.c = []
        self.m = order
        for i in range(self.m, 0, -1):
            self.c.append(symbols('C_' + str(piece_id) + '_' + str(i)))

    def __str__(self):
        return str(self.c)


class ClassicalSplines(object):
    def __init__(self, knots, order, pvajp):
        self.knots = knots
        self.order = order
        self.pvajp = pvajp
        self.degree = self.order - 1
        self.num_of_pieces = len(self.knots) - 1
        self.co, self.var, self.equations = [], [], []
        self.interpolation_conditions = pvajp
        # list of difference depth of pieces
        self.expression_with_co = [[] for i in range(self.degree)]
        self.function_with_co = [[] for i in range(self.degree)]
        self.expression_solved = [[] for i in range(self.degree)]
        self.piecewise = [[] for i in range(self.degree)]

    def build_expression_with_co(self):
        for index_of_piece in range(self.num_of_pieces):
            self.co.append(Coefficients(index_of_piece, order=self.order))
            p_i = self.co[-1].c[-1]
            self.var.append(self.co[-1].c[0])
            for index_of_depth in range(self.degree):
                p_i += self.co[-1].c[index_of_depth] \
                       * (y - self.knots[index_of_piece]) ** \
                       (self.degree - index_of_depth)
                self.var.append(self.co[-1].c[index_of_depth + 1])
            for index_of_depth in range(self.degree):
                self.expression_with_co[index_of_depth].append(
                    diff(p_i, y, index_of_depth))

    def get_expression_with_co(self):
        if len(self.expression_with_co[0]) == 0:
            self.build_expression_with_co()
        return self.expression_with_co

    def build_function_with_co(self):
        for index_of_piece in range(self.num_of_pieces):
            for index_of_depth in range(self.degree):
                self.function_with_co[index_of_depth].append(
                    lambdify(y, self.get_expression_with_co()[index_of_depth][
                        index_of_piece]))

    def get_function_with_co(self):
        if len(self.function_with_co[0]) == 0:
            self.build_function_with_co()
        return self.function_with_co

    def build_boundary_conditions(self, conditions_of_knots):
        """
        Build interpolation equations on each knot, choose pvaj with depth
        :param conditions_of_knots: dict of knot-depth pair, e.g.,
        {0:[0, 1, 2], -1:[0, 1, 2], 1:[0, 1]}
        :return: None, append equations
        """
        print("Boundary Conditions of " + str(self.__str__()) + ':')
        f = self.get_function_with_co()
        for index_of_knots in conditions_of_knots.keys():
            print("at No." + str(index_of_knots) + " knot: " +
                  str(time_to_degree(self.knots[index_of_knots])) + 'degree')
            for index_of_depth in conditions_of_knots[index_of_knots]:
                self.equations.append(Eq(f[index_of_depth][index_of_knots](
                        self.knots[index_of_knots]).evalf(),
                       self.pvajp[index_of_depth][index_of_knots]))
                print(self.equations[-1])

    def build_smoothness_conditions(self, loose_at_knots):
        """
        :param loose_at_knots: dict of knot-lose_up_level pair, e.g.,
        {1:2, 2:1}
        :return: None, append equations
        """
        print("Smoothness Conditions:")
        f = self.get_function_with_co()
        for index_of_knots in range(1, self.num_of_pieces):
            if index_of_knots == 3:
                knot = self.knots[index_of_knots]-0.00001
            else:
                knot = self.knots[index_of_knots]
            for index_of_depth in range(
                    self.degree if index_of_knots not in loose_at_knots
                    else
                    self.degree - loose_at_knots[index_of_knots]):
                self.equations.append(
                    Eq(f[index_of_depth][index_of_knots - 1](knot).evalf(),
                       f[index_of_depth][index_of_knots](knot).evalf()))
                print('At No. ' + str(index_of_knots) + 'knot: ' +
                      str(time_to_degree(knot)))
                print(self.equations[-1])

    def build_not_at_knot_conditions(self, index_of_piece,
                                     control_point, index_of_depth, value):
        f = self.get_function_with_co()
        self.equations.append(Eq(f[index_of_depth][index_of_piece]
                                 (control_point).evalf(), value))

    def build_periodic_conditions(self):
        f = self.get_function_with_co()
        print("Period Conditions")
        for index_of_depth in range(self.degree):
            self.equations.append(
                Eq(f[index_of_depth][0](self.knots[0]).evalf(),
                   f[index_of_depth][-1](self.knots[-1]).evalf()))
            print(self.equations[-1])

    def solve_equations(self):
        if len(self.equations) == len(self.var):
            return solve(self.equations, self.var)
        else:
            raise ValueError

    def get_solutions(self):
        return self.solve_equations()

    def build_expression_solved(self, latex_print_out=False):
        solutions = self.get_solutions()
        for index_of_depth in range(self.degree):
            for index_of_piece in range(self.num_of_pieces):
                self.expression_solved[index_of_depth].append(
                    self.expression_with_co[index_of_depth][index_of_piece].
                        subs([(self.co[index_of_piece].c[index_of_co],
                               solutions[
                                   self.co[index_of_piece].c[index_of_co]])
                              for index_of_co in range(self.order)]))
        if latex_print_out:
            for index_of_piece in range(self.num_of_pieces):
                print(latex(self.expression_solved[index_of_piece]))

    def get_expression_solved(self):
        if len(self.expression_solved[0]) == 0:
            self.build_expression_solved()
        return self.expression_solved


class Jaw_on_York(ClassicalSplines):
    def __init__(self, knots=None, order=6, pvajp=None):
        if knots is None:
            knots = degree_to_time(np.array([0, 73, 168]))
        if pvajp is None:
            pvajp = np.array([[0, -131, 0], [0, 0, 0],
                              [0, 0, 0], [0, 0, 0], [0, 0, 0]])
        ClassicalSplines.__init__(self, knots, order, pvajp)
        self.expr_of_x = [[] for i in range(self.degree)]
        self.piecewise_of_x = []

    def __str__(self):
        return "Jaw on York object"

    def build_equations(self, conditions_of_knots=None, loose_at_knots=None):
        if loose_at_knots is None:
            loose_at_knots = {1: 1}
        if conditions_of_knots is None:
            conditions_of_knots = {0: [0, 1, 2], -1: [0, 1, 2], 1: [0, 1]}
        self.build_boundary_conditions(conditions_of_knots)
        self.build_smoothness_conditions(loose_at_knots)

    def shift_curve(self):
        if len(self.equations) == 0:
            self.build_equations()
        expr_of_y = self.get_expression_solved()
        delta1 = degree_to_time(30)
        delta2 = degree_to_time(330)
        for index_of_depth in range(self.degree):
            self.expr_of_x[index_of_depth] += \
                [expr_of_y[index_of_depth][i].subs(y, x + delta1)
                 for i in range(self.num_of_pieces)]
            self.expr_of_x[index_of_depth].append(
                expr_of_y[index_of_depth][0].subs(y, x - delta2))
        return None

    def get_expr_of_x(self):
        if len(self.expr_of_x[0]) == 0:
            self.shift_curve()
        return self.expr_of_x

    def build_piecewise_expr(self):
        if len(self.expr_of_x[0]) == 0:
            self.shift_curve()
        if len(self.piecewise_of_x) == 0:
            for k in range(self.degree):
                self.piecewise_of_x.append(Piecewise(
                    (0, x < 0),
                    (self.expr_of_x[k][0], x <= degree_to_time(43)),
                    (self.expr_of_x[k][1], x <= degree_to_time(138)),
                    (0, x <= degree_to_time(330)),
                    (self.expr_of_x[k][2], x <= degree_to_time(360)),
                    (0, True)))

    def get_piecewise_of_x(self):
        if len(self.piecewise_of_x) == 0:
            self.build_piecewise_expr()
        return self.piecewise_of_x

    def get_functional_position(self):
        return lambdify(x, self.get_piecewise_of_x()[0])

    def get_functional_velocity(self):
        return lambdify(x, self.get_piecewise_of_x()[1])

    def get_functional_acceleration(self):
        return lambdify(x, self.get_piecewise_of_x()[2])

    def get_functional_jerk(self):
        return lambdify(x, self.get_piecewise_of_x()[3])

    def plot_numerical(self, num=3600):
        t = np.linspace(0, degree_to_time(360),
                        num, endpoint=True)
        degree = time_to_degree(t)
        position = self.get_functional_position()(t)
        velocity = self.get_functional_velocity()(t)
        acceleration = self.get_functional_acceleration()(t)
        jerk = self.get_functional_jerk()(t)
        fig = plt.figure(figsize=(15, 12), dpi=80)
        fig.suptitle('Jaw on York, with knots on \n' +
                     str(time_to_degree(self.knots) - 30),
                     fontsize='xx-large')
        plt.subplot(4, 1, 1)
        plt.grid()
        plt.ylabel("Position (mm)")
        plt.plot(degree, position,
                 color="blue", linewidth=3.0, linestyle="-")
        plt.xlim(0.0, 360.0)
        plt.xticks(np.linspace(0, 360, 37, endpoint=True))
        plt.subplot(4, 1, 2)
        plt.grid()
        plt.ylabel("Velocity (mm/s)")
        plt.plot(degree, velocity,
                 color="blue", linewidth=3.0, linestyle="-")
        plt.xlim(0.0, 360.0)
        plt.xticks(np.linspace(0, 360, 37, endpoint=True))
        plt.subplot(4, 1, 3)
        plt.grid()
        plt.ylabel("Acceleration (m/s^3)")
        plt.plot(degree, acceleration / 1000,
                 color="blue", linewidth=3.0, linestyle="-")
        plt.xlim(0.0, 360.0)
        plt.xticks(np.linspace(0, 360, 37, endpoint=True))
        plt.subplot(4, 1, 4)
        plt.grid()
        plt.ylabel("Jerk (m/s^4)")
        plt.plot(degree, jerk / 1000,
                 color="blue", linewidth=3.0, linestyle="-")
        plt.xlim(0.0, 360.0)
        plt.xticks(np.linspace(0, 360, 37, endpoint=True))
        plt.savefig("svaj_of_jaw_on_york.png", dpi=720)


def test_jaw_on_york():
    joy = Jaw_on_York()
    joy.plot_numerical()
    # OK
    integrate(joy.expr_of_x[0][0], x)


class York(ClassicalSplines):
    def __init__(self, order=6, knots=None, pvajp=None,
                 constant_velocity=-422):
        self.cv = constant_velocity
        self.package = Package(330, "Square", 49.5, 48.5, 124.6, 6, 190)
        # 0
        start = [0, [
            0,
            0,
            symbols('acc_start'),
            symbols('jerk_start'),
            symbols('ping_start')]]
        # 1
        # highest = [symbols('theta_highest'), [
        highest = [degree_to_time(43), [
            372.2,
            0,
            symbols('acc_highest'),
            symbols('jerk_highest'),
            symbols('ping_highest')]]
        # 2
        touch = [degree_to_time(93), [
            # touch = [symbols('theta_touch'), [
            symbols('pos_touch'),
            symbols('vel_touch'),
            symbols('acc_touch'),
            symbols('jerk_touch'),
            symbols('ping_touch')]]
        # 3
        closed = [degree_to_time(138), [
            # closed = [symbols('theta_closed'), [
            symbols('pos_closed'),
            self.cv,
            0,
            symbols('jerk_closed'),
            symbols('ping_closed')]]
        # 4
        folding = [degree_to_time(145), [
            # folding = [symbols('theta_folding'), [
            symbols('pos_folding'),
            self.cv,
            0,
            symbols('jerk_folding'),
            symbols('ping_folding')]]
        # 5
        folded = [degree_to_time(192), [
            # folded = [symbols('theta_folded'), [
            symbols('pos_folded'),
            self.cv,
            0,
            symbols('jerk_folded'),
            symbols('ping_folded')]]
        # 6
        accepting = [degree_to_time(262), [
            # accepting = [symbols('theta_accepting'), [
            symbols('pos_accepting'),
            self.cv,
            0,
            symbols('jerk_accepting'),
            symbols('ping_accepting')]]
        # 7
        accepted = [degree_to_time(318), [
            # accepted = [symbols('theta_accepted'), [
            symbols('pos_accepted'),
            self.cv,
            0,
            symbols('jerk_accepted'),
            symbols('ping_accepted')]]
        # 8
        # leaving = [symbols('theta_leaving'), [
        leaving = [degree_to_time(330), [
            symbols('pos_leaving'),
            self.cv,
            0,
            symbols('jerk_leaving'),
            symbols('ping_leaving')]]
        # 9
        # left = [symbols('theta_left'), [
        left = [degree_to_time(335), [
            symbols('pos_left'),
            symbols('vel_left'),
            symbols('acc_left'),
            symbols('jerk_left'),
            symbols('ping_left')]]
        # 10
        end = [degree_to_time(360), [
            0,
            0,
            symbols('acc_end'),
            symbols('jerk_end'),
            symbols('ping_end')]]
        if knots == None:
            knots = np.array(
                [start[0], highest[0], touch[0], closed[0],
                 folding[0], folded[0], accepting[0], accepted[0],
                 leaving[0], left[0], end[0]])
        if pvajp == None:
            pvajp = np.array([
                [start[1][i], highest[1][i], touch[1][i], closed[1][i],
                 folding[1][i], folded[1][i], accepting[1][i], accepted[1][i],
                 leaving[1][i], left[1][i], end[1][i]] for i in range(5)])
        print(knots)
        ClassicalSplines.__init__(self, knots, order, pvajp)

    def __str__(self):
        return 'York object'

    def build_expression_with_co(self):
        for index_of_piece in range(self.num_of_pieces):
            self.co.append(Coefficients(index_of_piece, order=self.order))
            p_i = self.co[-1].c[-1]
            self.var.append(self.co[-1].c[0])
            for index_of_depth in range(self.degree):
                p_i += self.co[-1].c[index_of_depth] \
                       * (x - self.knots[index_of_piece]) ** \
                       (self.degree - index_of_depth)
                self.var.append(self.co[-1].c[index_of_depth + 1])
            for index_of_depth in range(self.degree):
                self.expression_with_co[index_of_depth].append(
                    diff(p_i, x, index_of_depth))
        return self.expression_with_co

    def build_touching_expr(self):
        jaw_to_york_curve = Jaw_on_York()
        jaw_on_york_mechanism = O4DriveA()
        touch_degree = 93
        close_degree = 138
        x_R_AO2_of_r_O4O2_expr = jaw_on_york_mechanism.get_x_R_AO2_of_r_O4O2_expr()
        y_R_AO2_of_r_O4O2_expr = jaw_on_york_mechanism.get_y_R_AO2_of_r_O4O2_expr()
        x_V_AO2_of_vr_O4O2 = jaw_on_york_mechanism.get_x_V_AO2_of_vr_O4O2()
        y_V_AO2_of_vr_O4O2 = jaw_on_york_mechanism.get_y_V_AO2_of_vr_O4O2()
        jaw_to_york_slider_position = jaw_to_york_curve.get_expr_of_x()[0][1]
        jaw_to_york_slider_velocity = jaw_to_york_curve.get_expr_of_x()[1][1]
        p1 = plot(jaw_to_york_slider_position, (x, degree_to_time(43), degree_to_time(138)), show=True)
        p2 = plot(jaw_to_york_slider_velocity, (x, degree_to_time(43), degree_to_time(138)), show=True)
        x_R_AO2 = x_R_AO2_of_r_O4O2_expr.subs(jaw_on_york_mechanism.r_O4O2, -(
                jaw_to_york_slider_position - 52.0476394259645))
        x_V_AO2 = x_V_AO2_of_vr_O4O2.subs(
            [(jaw_on_york_mechanism.r, -(jaw_to_york_slider_position - 52.0476394259645)),
             (jaw_on_york_mechanism.v, -jaw_to_york_slider_velocity)])
        y_R_AO2 = y_R_AO2_of_r_O4O2_expr.subs(jaw_on_york_mechanism.r_O4O2, -(
                jaw_to_york_slider_position - 52.0476394259645))
        y_V_AO2 = y_V_AO2_of_vr_O4O2.subs(
            [(jaw_on_york_mechanism.r, -(jaw_to_york_slider_position - 52.0476394259645)),
             (jaw_on_york_mechanism.v, -jaw_to_york_slider_velocity)])
        p3 = plot(x_R_AO2, (x, degree_to_time(43), degree_to_time(138)), show=True)
        p4 = plot(x_V_AO2, (x, degree_to_time(43), degree_to_time(138)), show=True)
        p5 = plot(y_R_AO2, (x, degree_to_time(43), degree_to_time(138)), show=True)
        p6 = plot(y_V_AO2, (x, degree_to_time(43), degree_to_time(138)), show=True)
        x_R_AO5 = x_R_AO2
        p330sq = Package(330, "Square", 49.5, 48.5, 124.6, 6, 190)
        r = p330sq.depth / 2
        y_R_AO5 = sqrt(r ** 2 - (r + x_R_AO5) ** 2)
        p7 = plot(x_R_AO5, (x, degree_to_time(43), degree_to_time(138)), show=True)
        p8 = plot(y_R_AO5, (x, degree_to_time(93), degree_to_time(138)), show=True)
        y_R_O5O2 = 164.44 + p330sq.get_hs_sealing_length() + p330sq.get_height()
        print(y_R_O5O2)
        expr_O2O1_180 = self.get_expression_with_co()[0][6]\
            .subs(x, x + degree_to_time(180))
        print(expr_O2O1_180)
        y_R_O2O1 = y_R_AO5 + y_R_O5O2 + expr_O2O1_180 - y_R_AO2
        return y_R_O2O1

    def replace_touching_expr(self):
        y_R_O2O1 = self.build_touching_expr()
        y_V_O2O1 = diff(y_R_O2O1, x)
        y_A_O2O1 = diff(y_R_O2O1, x, 2)
        y_J_O2O1 = diff(y_R_O2O1, x, 3)
        y_P_O2O1 = diff(y_R_O2O1, x, 4)
        self.expression_with_co[0][2] = y_R_O2O1
        self.expression_with_co[1][2] = y_V_O2O1
        self.expression_with_co[2][2] = y_A_O2O1
        self.expression_with_co[3][2] = y_J_O2O1
        self.expression_with_co[4][2] = y_P_O2O1

    def build_function_with_co(self):
        for index_of_piece in range(self.num_of_pieces):
            for index_of_depth in range(self.degree):
                self.function_with_co[index_of_depth].append(
                    lambdify(x, self.expression_with_co[index_of_depth][
                        index_of_piece]))

    def build_position_relationships(self):
        f = self.get_function_with_co()
        # 1 when near
        pr_near = f[0][0](degree_to_time(43)).evalf()
        pl_near = f[0][9](degree_to_time(43 + 180)).evalf()
        self.equations.append(Eq(pr_near, pl_near))
        # 2 when touch
        pr_touch = f[0][0](self.knots[2]).evalf()
        pl_touch = f[0][6](self.knots[2] + 0.45).evalf()
        y_ArO2r_touch = 171.354752195555
        y_ArO2l_touch = self.package.depth / 2 + \
                        self.package.height + \
                        self.package.hs_sealing_length + \
                        166.44
        self.equations.append(Eq(pr_touch - pl_touch,
                                 y_ArO2l_touch - y_ArO2r_touch))
        # 3 When right jaw over left jaw
        pr_jaw_over_jaw = f[0][2](self.knots[3]).evalf()
        pl_jaw_over_jaw = f[0][6](self.knots[3] + 0.45).evalf()
        y_ArO2r_jaw_over_jaw = 166.44
        y_ArO2l_jaw_over_jaw = self.package.height + \
                               self.package.hs_sealing_length + \
                               166.44
        self.equations.append(Eq(pr_jaw_over_jaw - pl_jaw_over_jaw,
                                 y_ArO2l_jaw_over_jaw - y_ArO2r_jaw_over_jaw))

    def build_velocity_conditions(self):
        f = self.get_function_with_co()
        # 1 When folding
        vr_folding = f[1][4]((self.knots[4] + self.knots[5])/2).evalf()
        self.equations.append(Eq(vr_folding, self.cv + 300))
        # 2 When accepting
        vr_accepting = f[1][6]((self.knots[6] + self.knots[7])/2).evalf()
        self.equations.append(Eq(vr_accepting, self.cv + 340))

    # def build_periodic_coditions(self):
    #     f = self.get_function_with_co()
    #     for index_of_depth in range(self.degree):


    def build_equations(self):
        # self.build_smoothness_conditions(loose_at_konts={1: [2], 2: [2], 3: [2], 4: [2], 5: [2], 6: [2], 7: [2], 8: [2], 9: [2]})  # 3x9=27
        # self.build_periodic_conditions()
        self.build_smoothness_conditions({1: 2, 2: 1, 3: 2, 4: 1, 5: 1, 6: 1, 7: 2, 8: 2, 9: 2})  # 3x9=27 -2-2 = 23 -
        self.build_boundary_conditions(conditions_of_knots={
            0: [0, 1],
            1: [0, 1],
            3: [1, 2],
            4: [1, 2],
            5: [1, 2],
            6: [1, 2],
            7: [1, 2],
            8: [1, 2],
            - 1: [0, 1]
        })  # 2x9=18
        self.build_position_relationships()  # 3
        self.build_velocity_conditions()  # 2


def test_york():
    york = York()
    york.build_expression_with_co()
    york.replace_touching_expr()
    york.build_function_with_co()
    york.build_equations()
    for i in range(6):
        york.var.pop(12)
    solutions = solve(york.equations, york.var)
    print(solutions)
    for i in range(len(york.equations)):
        print(i)
        print(latex(york.equations[i]))
    for i in range(len(york.equations)):
        print(york.equations[i])


# test_york()

import pickle

import matplotlib.pyplot as plt
import numpy as np
from analysis import O4DriveA, ANeedO4
from helper_functions import degree_to_time, time_to_degree, \
    move_sympyplot_to_axes, print_list_items_in_row
from packages import Package
from splines_building import Polynomial, SplineWithPiecewisePolynomial, \
    ShakeHand
from sympy import symbols, Symbol, diff, lambdify, Eq, solve, \
    Piecewise, linsolve, nan, piecewise_fold
from sympy.abc import x
from sympy.plotting import plot


class JawOnYorkCurve(SplineWithPiecewisePolynomial):
    """
    """

    def __init__(self, knots=None, orders=None, pvajp=None):
        # 0
        start = [degree_to_time(0), [
            symbols('pos_start'),
            symbols('vel_start'),
            symbols('acc_start'),
            symbols('jerk_start'),
            symbols('ping_start')]]
        # 1
        widest = [degree_to_time(43), [
            -131,
            0,
            symbols('acc_widest'),
            symbols('jerk_widest'),
            symbols('ping_widest')]]
        # 2
        closed = [degree_to_time(138), [
            0,
            symbols('vel_closed'),
            symbols('acc_closed'),
            symbols('jerk_closed'),
            symbols('ping_closed')]]
        # 3
        open = [degree_to_time(330), [
            0,
            symbols('vel_open'),
            symbols('acc_open'),
            symbols('jerk_open'),
            symbols('ping_open')]]
        # 4
        end = [degree_to_time(360), [
            symbols('pos_end'),
            symbols('vel_end'),
            symbols('acc_end'),
            symbols('jerk_end'),
            symbols('ping_end')]]
        if knots == None:
            knots = np.array([start[0], widest[0], closed[0],
                              open[0], end[0]])
        if pvajp == None:
            pvajp = np.array([[start[1][i], widest[1][i], closed[1][i],
                               open[1][i], end[1][i]] for i in range(5)])
        if orders == None:
            orders = [6, 6, 2, 6]
        SplineWithPiecewisePolynomial.__init__(self, knots, orders)
        self.pvajp = pvajp
        self.equations = []
        self.variables = []
        self.count_of_var = sum(self.orders)
        self.count_of_interpolation = 0
        self.count_of_boundary = 0
        self.count_of_not_at_knot = 0
        self.count_of_periodic = 0
        self.count_of_smoothness = 0
        self.piecewise = []

    def build_interpolating_condition(self):
        """
        j1 = JawOnYorkCurve()
        print(j1.build_interpolating_condition())
        """
        if self.count_of_interpolation != 0:
            return self.count_of_interpolation
        for d in range(5):
            for k in range(1, len(self.kp) - 1):
                if isinstance(self.pvajp[d][k], Symbol):
                    continue
                else:
                    p = self.get_pieces()[k]
                    f = p.get_functions()
                    knot = self.knots[k]
                    eq = Eq(f[d](knot), self.pvajp[d][k])
                    self.equations.append(eq)
                    self.count_of_interpolation += 1
        return self.count_of_interpolation

    def build_boundary_condition(self):
        """
        j1 = JawOnYorkCurve()
        print(j1.build_boundary_condition())
        """
        if self.count_of_boundary != 0:
            return self.count_of_boundary
        for d in range(5):
            for k in [0, -1]:
                if isinstance(self.pvajp[d][k], Symbol):
                    continue
                else:
                    p = self.get_pieces()[k]
                    f = p.get_functions()
                    knot = self.knots[k]
                    eq = Eq(f[d](knot), self.pvajp[d][k])
                    self.equations.append(eq)
                    self.count_of_boundary += 1
        return self.count_of_boundary

    def build_not_at_knot_condition(self, points, depths, values):
        """
        j1 = JawOnYorkCurve()
        points = [degree_to_time(23), degree_to_time(123)]
        depths = [3, 3]
        values = [0, 0]
        print(j1.build_not_at_knot_condition(points, depths, values))
        """
        if self.count_of_not_at_knot != 0:
            return self.count_of_not_at_knot
        for i in range(len(points)):
            for k in range(self.num_of_pieces, -1, -1):
                if points[i] >= self.knots[k]:
                    p = self.get_pieces()[k]
                    f = p.get_functions()
                    knot = self.knots[k]
                    eq = Eq(f[depths[i]](knot), values[i])
                    self.equations.append(eq)
                    self.count_of_not_at_knot += 1
                    break
        return self.count_of_not_at_knot

    def build_periodic_condition(self):
        """
        j1 = JawOnYorkCurve()
        print(j1.build_periodic_condition())
        """
        if self.count_of_periodic != 0:
            return self.count_of_period
        ps = self.get_pieces()[0]
        fs = ps.get_functions()
        s = self.knots[0]
        pe = self.get_pieces()[-1]
        fe = pe.get_functions()
        e = self.knots[-1]
        for d in range(min(ps.order, pe.order)):
            eq = Eq(fs[d](s), fe[d](e))
            self.equations.append(eq)
            self.count_of_periodic += 1
            # TODO: less than 6 order condition?
        return self.count_of_periodic

    def how_many_smoothness_equations_available(self):
        """
        j1 = JawOnYorkCurve()
        print(j1.how_many_smoothness_equations_available())
        """
        if self.count_of_interpolation == 0:
            self.build_interpolating_condition()
        if self.count_of_boundary == 0:
            self.build_boundary_condition()
        if self.count_of_periodic == 0:
            self.build_periodic_condition()
        result = (self.count_of_var - self.count_of_interpolation -
                  self.count_of_boundary - self.count_of_periodic)
        return result

    def build_smoothness_condition(self, depths=[0, 4, 3, 3, 0]):
        """
        j1 = JawOnYorkCurve()
        print(j1.build_smoothness_condition())
        """
        if self.count_of_smoothness != 0:
            return self.count_of_smoothness
        k1 = self.knots[1]
        p1b = self.get_pieces()[0]
        p1a = self.get_pieces()[1]
        f1b = p1b.get_functions()
        f1a = p1a.get_functions()
        for d in range(4):
            eq = Eq(f1b[d](k1), f1a[d](k1))
            self.equations.append(eq)
            self.count_of_smoothness += 1
        k2 = self.knots[2]
        p2b = self.get_pieces()[1]
        p2a = self.get_pieces()[2]
        f2b = p2b.get_functions()
        f2a = p2a.get_functions()
        for d in range(2):
            eq = Eq(f2b[d](k2), f2a[d](k2))
            self.equations.append(eq)
            self.count_of_smoothness += 1
        eq = Eq(f2b[2](k2), 0)
        self.equations.append(eq)
        self.count_of_smoothness += 1
        k3 = self.knots[3]
        p3b = self.get_pieces()[2]
        p3a = self.get_pieces()[3]
        f3b = p3b.get_functions()
        f3a = p3a.get_functions()
        for d in range(2):
            eq = Eq(f3b[d](k3), f3a[d](k3))
            self.equations.append(eq)
            self.count_of_smoothness += 1
        eq = Eq(0, f3a[2](k3))
        self.equations.append(eq)
        self.count_of_smoothness += 1
        return self.count_of_smoothness

    def build_equations(self):
        """
        j1 = JawOnYorkCurve()
        print(j1.build_equations())
        """
        if self.count_of_interpolation == 0:
            self.build_interpolating_condition()
        if self.count_of_boundary == 0:
            self.build_boundary_condition()
        if self.count_of_periodic == 0:
            self.build_periodic_condition()
        if self.count_of_smoothness == 0:
            self.build_smoothness_condition()
        return len(self.equations)

    def get_equations(self):
        if len(self.equations) == 0:
            self.build_equations()
        return self.equations

    def build_variables(self):
        """
        j1 = JawOnYorkCurve()
        print(j1.build_variables())
        """
        if len(self.variables) != 0:
            return len(self.variables)
        for i in range(self.num_of_pieces):
            polynomial_i = self.get_pieces()[i]
            coe_i = polynomial_i.coe
            for j in range(len(coe_i)):
                self.variables.append(coe_i[j])
        return len(self.variables)

    def get_variables(self):
        if len(self.variables) == 0:
            self.build_variables()
        return self.variables

    def solve_coefficients(self):
        """
        j1 = JawOnYorkCurve()
        print(j1.solve_coefficients())
        """
        equations = self.get_equations()
        variables = self.get_variables()
        solutions = solve(equations, variables)
        return solutions

    def update_with_solution(self):
        """
        j1 = JawOnYorkCurve()
        j1.update_with_solution()
        """
        solution = self.solve_coefficients()
        self.involve_solutions(solution)

    def get_kth_expr_of_ith_piece(self, k, i, without_symbol_coe=True):
        if without_symbol_coe:
            self.update_with_solution()
        try:
            return self.get_pieces()[i].get_expr()[k]
        except:
            return 0

    def build_spline(self):
        self.update_with_solution()
        if len(self.piecewise) == 0:
            for k in range(max(self.orders)):
                self.piecewise.append(Piecewise(
                    (0, x < self.knots[0]),
                    (self.get_kth_expr_of_ith_piece(k, 0), x <= self.knots[1]),
                    (self.get_kth_expr_of_ith_piece(k, 1), x <= self.knots[2]),
                    (self.get_kth_expr_of_ith_piece(k, 2), x <= self.knots[3]),
                    (self.get_kth_expr_of_ith_piece(k, 3), x <= self.knots[4]),
                    (0, True)))

    def get_piecewise(self):
        self.build_spline()
        return self.piecewise

    def plot_numerical(self, num=3600):
        """
        j1 = JawOnYorkCurve()
        j1.plot_numerical()
        """
        t = np.linspace(0, degree_to_time(360),
                        num, endpoint=True)
        degree = time_to_degree(t)
        position = lambdify(x, self.get_piecewise()[0])(t)
        velocity = lambdify(x, self.get_piecewise()[1])(t)
        acceleration = lambdify(x, self.get_piecewise()[2])(t)
        jerk = lambdify(x, self.get_piecewise()[3])(t)
        fig = plt.figure(figsize=(15, 12), dpi=80)
        fig.suptitle('Jaw on York curves, with knots on \n' +
                     str(time_to_degree(self.knots)),
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


class TraceOfA(object):
    def __init__(self, load_memo=True):
        self.joy_curve = JawOnYorkCurve()
        self.joy_mechanism_forward = O4DriveA()
        self.joy_mechanism_backward = ANeedO4()
        self.package = Package(330, "Square", 49.5, 48.5, 124.6, 6, 190)
        if load_memo:
            self.load_memo_from_file()
        else:
            self.memo = {}

    def write_memo_to_file(self):
        """
        t1 = TraceOfA()
        t1.write_memo_to_file()
        """
        output = open('trace_of_A_memo.pkl', 'wb')
        pickle.dump(self.memo, output)
        output.close()

    def load_memo_from_file(self):
        """
        t1 = TraceOfA()
        t1.load_memo_from_file()
        """
        pkl_file = open('trace_of_A_memo.pkl', 'rb')
        self.memo = pickle.load(pkl_file)
        pkl_file.close()
        return self.memo

    def get_close_rO4O2(self):
        """
        t1 = TraceOfA()
        print(t1.get_close_rO4O2())
        :return: 52.0476394259659
        """
        if 'r_O4O2_close' in self.memo:
            return self.memo['r_O4O2_close']
        expr = self.joy_mechanism_backward.get_r_O4O2_of_x_R_AO2_expr()
        x_R_AO2 = self.joy_mechanism_backward.x_R_AO2
        r_O4O2_close = expr.subs(x_R_AO2, 0)
        self.memo['r_O4O2_close'] = r_O4O2_close
        return r_O4O2_close

    def get_touch_rO4O2(self):
        """
        t1 = TraceOfA()
        print(t1.get_touch_rO4O2())
        :return: 93.1457274726962
        """
        if 'r_O4O2_touch' in self.memo:
            return self.memo['r_O4O2_touch']
        expr = self.joy_mechanism_backward.get_r_O4O2_of_x_R_AO2_expr()
        x_R_AO2_symbol = self.joy_mechanism_backward.x_R_AO2
        x_R_AO2_when_touch = - self.package.depth / 2
        r_O4O2_touch = expr.subs(x_R_AO2_symbol, x_R_AO2_when_touch)
        self.memo['r_O4O2_touch'] = r_O4O2_touch
        return r_O4O2_touch

    def get_touch_time(self):
        """
        t1 = TraceOfA()
        print(t1.get_touch_time())
            0.232561894257538
        """
        if 'touch_time' in self.memo:
            return self.memo['touch_time']
        r_O4O2_touch = self.get_touch_rO4O2()
        r_O4O2_close = self.get_close_rO4O2()
        position_touch = - (r_O4O2_touch - r_O4O2_close)
        curve = self.joy_curve.get_kth_expr_of_ith_piece(0, 1)
        equation = Eq(curve, position_touch)
        touch_time = solve(equation, x)[2]
        self.memo['touch_time'] = touch_time
        return touch_time

    def get_touch_degree(self):
        """
        t1 = TraceOfA()
        print(t1.get_touch_degree())
            93.0247577030154
        """
        return time_to_degree(self.get_touch_time())

    def get_y_R_AO2_when_touching_expr(self):
        """
        t1 = TraceOfA()
        print(t1.get_y_R_AO2_when_touching_expr())
        print(t1.get_y_R_AO2_when_touching_expr().subs(x, t1.get_touch_time()))
            171.354752195555
        print(t1.get_y_R_AO2_when_touching_expr().subs(x, degree_to_time(138)))
            164.440000000000
        :return:
        """
        if 'y_R_AO2_when_touching_expr' in self.memo:
            return self.memo['y_R_AO2_when_touching_expr']
        expr = self.joy_mechanism_forward.get_y_R_AO2_of_r_O4O2_expr()
        r_O4O2_symbol = self.joy_mechanism_forward.r_O4O2
        curve = self.joy_curve.get_kth_expr_of_ith_piece(0, 1)
        r_O4O2_close = self.get_close_rO4O2()
        r_O4O2_value = - (curve - r_O4O2_close)
        y_R_AO2_when_touching_expr = expr.subs(r_O4O2_symbol, r_O4O2_value)
        self.memo['y_R_AO2_when_touching_expr'] = y_R_AO2_when_touching_expr
        self.write_memo_to_file()
        return y_R_AO2_when_touching_expr

    def get_x_R_AO2_when_touching_expr(self):
        """
        t1 = TraceOfA()
        print(t1.get_x_R_AO2_when_touching_expr())
        print(t1.get_x_R_AO2_when_touching_expr().subs(x, t1.get_touch_time()))
            -24.2500000000004
        print(t1.get_x_R_AO2_when_touching_expr().subs(x, degree_to_time(138)))
            -7.81597009336110e-14
        print(t1.get_x_R_AO2_when_touching_expr().subs(x, degree_to_time(84)))
            -39.4824497428945
        :return:
        """
        if 'x_R_AO2_when_touching_expr' in self.memo:
            return self.memo['x_R_AO2_when_touching_expr']
        expr = self.joy_mechanism_forward.get_x_R_AO2_of_r_O4O2_expr()
        r_O4O2_symbol = self.joy_mechanism_forward.r_O4O2
        curve = self.joy_curve.get_kth_expr_of_ith_piece(0, 1)
        r_O4O2_close = self.get_close_rO4O2()
        r_O4O2_value = - (curve - r_O4O2_close)
        x_R_AO2_when_touching_expr = expr.subs(r_O4O2_symbol, r_O4O2_value)
        self.memo['x_R_AO2_when_touching_expr'] = x_R_AO2_when_touching_expr
        self.write_memo_to_file()
        return x_R_AO2_when_touching_expr

    def get_y_R_AO5_when_touching_expr(self):
        """
        t1 = TraceOfA()
        print(t1.get_y_R_AO5_when_touching_expr())
        print(t1.get_y_R_AO5_when_touching_expr().subs(x, t1.get_touch_time()))
            24.2500000000000
        print(t1.get_y_R_AO5_when_touching_expr().subs(x, degree_to_time(138)))
            1.93692169299983e-6
        print(t1.get_y_R_AO5_when_touching_expr().subs(x, degree_to_time(84)))
            18.8688890724969
        """
        if 'y_R_AO5_when_touching_expr' in self.memo:
            return self.memo['y_R_AO5_when_touching_expr']
        x_R_AO2_when_touching_expr = \
            self.get_x_R_AO2_when_touching_expr()
        x_R_AO5_when_touching_expr = x_R_AO2_when_touching_expr
        r_AG = self.package.depth / 2
        y_R_AO5_when_touching_expr = \
            (r_AG ** 2 - (r_AG + x_R_AO5_when_touching_expr) ** 2) ** 0.5
        self.memo['y_R_AO5_when_touching_expr'] = y_R_AO5_when_touching_expr
        self.write_memo_to_file()
        return y_R_AO5_when_touching_expr

    def get_y_R_AO5_when_touching_func(self):
        """
        t1 = TraceOfA()
        print(t1.get_y_R_AO5_when_touching_func()(t1.get_touch_time()))
            error
            File "/Users/johnqu/.conda/envs/Tetracamthon/lib/python3.7/site-packages/numpy/lib/scimath.py", line 226, in sqrt
    return nx.sqrt(x)
AttributeError: 'Float' object has no attribute 'sqrt'
        print(t1.get_y_R_AO5_when_touching_func()(degree_to_time(138)))
        """
        expr = self.get_y_R_AO5_when_touching_expr()
        return lambdify(x, expr)

    def plot_numerical(self, num=360):
        """
        t1 = TraceOfA()
        t1.plot_numerical()
        """
        start_time = float(self.get_touch_time())
        end_time = float(degree_to_time(138 - 1))
        t = np.linspace(start_time,
                        end_time,
                        num=360, endpoint=True)
        degree = time_to_degree(t)
        x_R_AO5_e = self.get_x_R_AO2_when_touching_expr()
        x_R_AO5_f = lambdify(x, x_R_AO5_e)
        y_R_AO5_e = self.get_y_R_AO5_when_touching_expr()
        y_R_AO5_f = lambdify(x, y_R_AO5_e)
        y_V_AO5_e = diff(y_R_AO5_e, x)
        y_V_AO5_f = lambdify(x, y_V_AO5_e)
        y_A_AO5_e = diff(y_V_AO5_e, x)
        y_A_AO5_f = lambdify(x, y_A_AO5_e)
        fig = plt.figure(figsize=(15, 12), dpi=80)
        fig.suptitle('R_AO5 SVA curves.', fontsize='x-large')
        plt.subplot(4, 1, 1)
        plt.grid()
        plt.ylabel("x position of AtoO5 (mm)")
        plt.plot(degree, x_R_AO5_f(t),
                 color="blue", linewidth=3.0, linestyle="-")
        plt.xlim(time_to_degree(start_time), time_to_degree(end_time))
        plt.subplot(4, 1, 2)
        plt.grid()
        plt.ylabel("y position of AtoO5 (mm)")
        plt.plot(degree, y_R_AO5_f(t),
                 color="blue", linewidth=3.0, linestyle="-")
        plt.xlim(time_to_degree(start_time), time_to_degree(end_time))
        plt.subplot(4, 1, 3)
        plt.grid()
        plt.ylabel("y velocity of AtoO5 (mm/s)")
        plt.plot(degree, y_V_AO5_f(t),
                 color="blue", linewidth=3.0, linestyle="-")
        plt.xlim(time_to_degree(start_time), time_to_degree(end_time))
        plt.subplot(4, 1, 4)
        plt.grid()
        plt.ylabel("y acceleration of AtoO5 (m/s^2)")
        plt.plot(degree, y_A_AO5_f(t) / 1000,
                 color="blue", linewidth=3.0, linestyle="-")
        plt.xlim(time_to_degree(start_time), time_to_degree(end_time))
        plt.savefig("Track of A to O5 curves.png", dpi=720)


def load_new_touch_piece():
    """
    j2 = YorkCurve()
    print(j2.new_touch_piece())
    """
    pkl_file = open('new_touch_piece.pkl', 'rb')
    new_touch_piece = pickle.load(pkl_file)
    pkl_file.close()
    return new_touch_piece


class YorkCurve(SplineWithPiecewisePolynomial):
    def __init__(self, knots=None, orders=None, pvajp=None):
        self.joy = JawOnYorkCurve()
        self.trace = TraceOfA(load_memo=True)
        self.package = Package(330, "Square", 49.5, 48.5, 124.6, 6, 190)
        self.cv = - self.package.get_pulling_velocity(cycle_time=0.9)
        self.start = [degree_to_time(0), [
            0,
            0,
            symbols('acc_start'),
            symbols('jerk_start'),
            symbols('ping_start')]]
        self.start_pair = [degree_to_time(20), [
            symbols('pos_start_pair'),
            symbols('vel_start_pair'),
            symbols('acc_start_pair'),
            symbols('jerk_start_pair'),
            symbols('ping_start_pair')]]
        self.cross = [degree_to_time(43), [
            200,
            symbols('vel_cross'),
            0,
            symbols('jerk_cross'),
            symbols('ping_cross')]]
        self.cross_pair = [degree_to_time(63), [
            symbols('pos_cross_pair'),
            symbols('vel_cross_pair'),
            symbols('acc_cross_pair'),
            symbols('jerk_cross_pair'),
            symbols('ping_cross_pair')]]
        self.highest = [degree_to_time(84), [
            372.2,
            0,
            symbols('acc_highest'),
            symbols('jerk_highest'),
            symbols('ping_highest')]]
        self.highest_pair = [degree_to_time(90), [
            symbols('pos_highest_pair'),
            symbols('vel_highest_pair'),
            symbols('acc_highest_pair'),
            symbols('jerk_highest_pair'),
            symbols('ping_highest_pair')]]
        self.touch = [self.trace.get_touch_time(), [
            symbols('pos_touch'),
            # 350,
            symbols('vel_touch'),
            symbols('acc_touch'),
            symbols('jerk_touch'),
            symbols('ping_touch')]]
        self.closed = [degree_to_time(138), [
            symbols('pos_closed'),
            self.cv,
            symbols('acc_closed'),
            symbols('jerk_closed'),
            symbols('ping_closed')]]
        self.fold = [degree_to_time(145), [
            symbols('pos_folding'),
            symbols('vel_folding'),
            symbols('acc_folding'),
            symbols('jerk_folding'),
            symbols('ping_folding')]]
        self.folding = [degree_to_time(168), [
            symbols('pos_folding'),
            self.cv + 300,
            0,
            symbols('jerk_folding'),
            symbols('ping_folding')]]
        self.folded = [degree_to_time(192), [
            symbols('pos_folded'),
            self.cv,
            symbols('acc_folded'),
            symbols('jerk_folded'),
            symbols('ping_folded')]]
        self.accept = [degree_to_time(264), [
            symbols('pos_accepting'),
            symbols('vel_accepting'),
            symbols('acc_accepting'),
            symbols('jerk_accepting'),
            symbols('ping_accepting')]]
        self.accepted = [degree_to_time(318), [
            # accepted = [symbols('theta_accepted'), [
            symbols('pos_accepted'),
            self.cv,
            symbols('acc_accepted'),
            symbols('jerk_accepted'),
            symbols('ping_accepted')]]
        self.leave = [degree_to_time(325), [
            symbols('pos_leaving'),
            symbols('vel_leaving'),
            symbols('acc_leaving'),
            symbols('jerk_leaving'),
            symbols('ping_leaving')]]
        self.left = [degree_to_time(330), [
            symbols('pos_left'),
            symbols('vel_left'),
            symbols('acc_left'),
            symbols('jerk_left'),
            symbols('ping_left')]]
        self.end = [degree_to_time(360), [
            symbols('pos_end'),
            symbols('vel_end'),
            symbols('acc_end'),
            symbols('jerk_end'),
            symbols('ping_end')]]
        self.kp = [
            self.start,
            # self.start_pair,
            self.cross,
            # self.cross_pair,
            # self.highest,
            # self.highest_pair,
            self.touch,
            self.closed,
            self.fold,
            # self.folding,
            self.folded,
            self.accept,
            self.accepted,
            self.leave,
            # self.left,
            self.end
        ]
        if knots == None:
            knots = np.array([self.kp[i][0] for i in range(len(self.kp))])
        if pvajp == None:
            pvajp = np.array([[self.kp[i][1][j] for i in range(len(self.kp))]
                              for j in range(5)])
        if orders == None:
            orders = [6, 6, 6, 2, 6, 2, 6, 2, 6]
            # orders = [6 for i in range(len(self.kp) - 1)]
        # SplineWithPiecewisePolynomial.__init__(self, knots, orders)
        knots_0 = np.linspace(self.start[0], self.cross[0], 4, endpoint=True)
        orders_0 = np.array([6 for i in range(len(knots_0) - 1)])
        piece_0 = SplineWithPiecewisePolynomial(knots_0, orders_0)
        knots_1 = np.linspace(self.cross[0], self.highest[0], 4, endpoint=True)
        orders_1 = np.array([6 for i in range(len(knots_1) - 1)])
        piece_1 = SplineWithPiecewisePolynomial(knots_1, orders_1)
        knots_2 = np.linspace(self.highest[0], self.touch[0], 4, endpoint=True)
        orders_2 = np.array([6 for i in range(len(knots_2) - 1)])
        piece_2 = SplineWithPiecewisePolynomial(knots_2, orders_2)
        knots_3 = np.linspace(self.accept[0], self.accepted[0], 4,
                              endpoint=True)
        orders_3 = np.array([6 for i in range(len(knots_3) - 1)])
        piece_3 = SplineWithPiecewisePolynomial(knots_3, orders_3)
        piece_4 = None

        self.pvajp = pvajp
        self.equations = []
        self.variables = []
        self.count_of_interpolation = 0
        self.count_of_boundary = 0
        self.count_of_not_at_knot = 0
        self.count_of_periodic = 0
        self.count_of_position = 0
        self.count_of_velocity = 0
        self.count_of_smoothness = 0
        self.piecewise = []
        self.solution = {}

    def save_new_touch_piece(self, new_touch_piece):
        """
        j2 = YorkCurve()
        j2.save_new_touch_piece()
        """
        output = open('new_touch_piece.pkl', 'wb')
        pickle.dump(new_touch_piece, output)
        output.close()

    def replace_touching_piece(self, reload=True):
        """
        j2 = YorkCurve()
        j2.replace_touching_piece(reload=False)
        print(j2.pieces[2].get_expr()[0])
        j3 = YorkCurve()
        j3.replace_touching_piece()
        print(j3.pieces[2].get_expr()[1])
        """
        index_t = self.kp.index(self.touch)
        if reload:
            np = load_new_touch_piece()  # New Piece
            self.pieces[index_t] = np
            return
        y_R_AO5_expr = self.trace.get_y_R_AO5_when_touching_expr()
        y_R_AO2_expr = self.trace.get_y_R_AO2_when_touching_expr()
        r_O5O2 = self.package.height + \
                 self.package.hs_sealing_length + \
                 self.trace.joy_mechanism_forward.r_DC_value
        index_a = self.kp.index(self.accept)
        accepting_curve_expr = \
            self.pieces[index_a].get_expr()[0].subs(x, x + degree_to_time(180))
        accepting_curve_coe = self.pieces[index_a].get_coefficients()
        new_touch_curve_expr = y_R_AO5_expr + r_O5O2 + accepting_curve_expr \
                               - y_R_AO2_expr
        op = self.pieces[index_t]  # Old Piece
        op_id = op.get_piece_id()
        op_order = op.get_order()
        op_piece = op.get_piece()
        np = Polynomial(op_id, op_order, op_piece)  # New Piece
        np.replace_expr(new_touch_curve_expr, accepting_curve_coe)
        self.save_new_touch_piece(np)
        self.pieces[index_t] = np

    def build_variables(self):
        """
        j2 = YorkCurve()
        print(j2.build_variables())
        print(j3.build_variables())
        """
        if len(self.variables) != 0:
            return len(self.variables)
        for i in range(self.num_of_pieces):
            if i == self.kp.index(self.touch):
                continue
            polynomial_i = self.get_pieces()[i]
            coe_i = polynomial_i.coe
            for j in range(len(coe_i)):
                self.variables.append(coe_i[j])
        return len(self.variables)

    def get_variables(self):
        """
        j2 = YorkCurve()
        print(j2.get_variables())
        """
        if len(self.variables) == 0:
            self.build_variables()
        return self.variables

    def build_interpolating_condition(self):
        """
        j2 = YorkCurve()
        print(j2.build_interpolating_condition())
        print(j3.build_interpolating_condition())
        """
        if self.count_of_interpolation != 0:
            return self.count_of_interpolation
        for k in range(len(self.knots)):
            knot = self.knots[k]
            if k == 0:
                p = self.get_pieces()[0]
            else:
                p = self.get_pieces()[k - 1]
            e = p.get_expr()
            for d in range(5):
                if isinstance(self.pvajp[d][k], Symbol):
                    continue
                else:
                    eq = Eq(e[d].subs(x, knot), self.pvajp[d][k])
                    self.equations.append(eq)
                    self.count_of_interpolation += 1
        return self.equations[-self.count_of_interpolation:]

    def build_periodic_condition(self):
        """
        j2 = YorkCurve()
        print(j2.build_periodic_condition())
        """
        if self.count_of_periodic != 0:
            return self.count_of_period
        ps = self.get_pieces()[0]  # Piece of Start
        es = ps.get_expr()  # Expression of Start
        ts = self.knots[0]  # Time of Start
        pe = self.get_pieces()[-1]  # Piece of End
        ee = pe.get_expr()  # Expression of End
        te = self.knots[-1]  # Time of End
        for d in range(min(ps.order, pe.order) - 2):  # Start IS a knot.
            eq = Eq(es[d].subs(x, ts), ee[d].subs(x, te))
            self.equations.append(eq)
            self.count_of_periodic += 1
            # TODO: less than 6 order condition?
        return self.equations[-self.count_of_periodic:]

    def build_position_relation(self):
        """
        j2 = YorkCurve()
        print(j2.build_position_relation())
        """
        if self.count_of_position != 0:
            return self.count_of_position
        pps = self.get_pieces()  # Polynomial PieceS
        # ======
        # when near
        # ------
        # rlnt = self.knot[1]  # Right Left Near Time
        # lrnt = rlnt + degree_to_time(180)  # Left Right Near Time
        # # pr_near_f = pps[0].get_functions()[0]
        # # pl_near_f = pps[5].get_functions()[0]
        # pr_near_e = pps[0].get_expr()[0]
        # pl_near_e = pps[5].get_expr()[0]
        # self.equations.append(Eq(pr_near_e.subs(x, rlnt),
        #                          pl_near_e.subs(x, lrnt)))
        # self.count_of_position += 1
        # ======
        # when highest
        # ------
        trh = self.highest[0]  # Time of Right york Highest
        pr_highest_e = pps[1].get_expr()[0]
        p_highest_v = self.highest[1][0]  # Position Highest Value
        self.equations.append(Eq(pr_highest_e.subs(x, trh), p_highest_v))
        self.count_of_position += 1
        # ======
        # when touch  # Duplicated?
        # ------
        # rjtt = self.knots[2]  # Right Jaw Touch Time
        # ljtt = self.knots[2] + degree_to_time(180)  # Left Jaw Touch Time
        # # pr_touch_f = pps[1].get_functions()[0]
        # # pl_touch_f = pps[6].get_functions()[0]
        # pr_touch_e = pps[1].get_expr()[0]
        # pl_touch_e = pps[6].get_expr()[0]
        # y_ArO2r = self.trace.get_y_R_AO2_when_touching_expr()
        # y_ArO2r_touch = y_ArO2r.subs(x, self.trace.get_touch_time())
        # y_ArO2l_touch = self.package.depth / 2 + \
        #                 self.package.height + \
        #                 self.package.hs_sealing_length + \
        #                 self.trace.joy_mechanism_forward.r_DC_value
        # O2r_over_O2l = pr_touch_e.subs(x, rjtt) \
        #                - pl_touch_e.subs(x, ljtt)
        # self.equations.append(Eq(O2r_over_O2l, y_ArO2l_touch - y_ArO2r_touch))
        # self.count_of_position += 1
        # ======
        # When closed, right jaw over left jaw
        # ------
        # trjc = self.knots[3]  # Time Right Jaw Closed
        # tlja = self.knots[7]  # Time Left Jaw Accepted
        # pr_touching_e = pps[2].get_expr()[0]  # Position Right york Expression
        # pl_accepting_e = pps[6].get_expr()[0] # Position Left york Expression
        y_ArAl_jaw_over_jaw = self.package.height + \
                              self.package.hs_sealing_length
        # self.equations.append(Eq(pr_touching_e.subs(x, trjc)
        #                          - pl_accepting_e.subs(x, tlja),
        #                          y_ArAl_jaw_over_jaw))
        # self.count_of_position += 1
        # return self.equations[-self.count_of_position:]
        # ======
        # When left
        # ------
        # index_left = self.kp.index(self.left)
        # trjl = self.knots[index_left]  # Time Right Jaw Left
        # tljl = trjl - degree_to_time(180)  # Time Left Jaw Left
        trjl = degree_to_time(330)
        tljl = degree_to_time(330 - 180)
        index_leave = self.kp.index(self.leave)
        pr_leave_e = pps[index_leave].get_expr()[0]
        index_fold = self.kp.index(self.fold)
        pl_fold_e = pps[index_fold].get_expr()[0]
        self.equations.append(Eq(pr_leave_e.subs(x, trjl)
                                 - pl_fold_e.subs(x, tljl),
                                 - y_ArAl_jaw_over_jaw - 20))
        self.count_of_position += 1
        return self.equations[-self.count_of_position:]

    def build_velocity_condition(self):
        """
        j2 = YorkCurve()
        print(j2.build_velocity_condition())
        """
        if self.count_of_velocity != 0:
            return self.count_of_velocity
        pps = self.get_pieces()  # Polynomial PieceS
        # ======
        # When folding
        # ------
        index_fold = self.kp.index(self.fold)
        # Folding Middle Time
        fmt = (self.knots[index_fold] + self.knots[index_fold + 1]) / 2
        vr_folding_e = pps[index_fold].get_expr()[1]
        self.equations.append(Eq(vr_folding_e.subs(x, fmt),
                                 self.cv + 300))
        self.count_of_velocity += 1
        ar_folding_e = pps[index_fold].get_expr()[2]
        self.equations.append(Eq(ar_folding_e.subs(x, fmt), 0))
        self.count_of_velocity += 1
        # ======
        # When accepting
        # ------
        # vr_accepting_f = pps[6].get_functions()[1]
        index_accept = self.kp.index(self.accept)
        # Accepting Middle Time
        amt = (self.knots[index_accept] + self.knots[index_accept + 1]) / 2
        vr_accepting_e = pps[index_accept].get_expr()[1]
        self.equations.append(Eq(vr_accepting_e.subs(x, amt),
                                 self.cv + 340))
        self.count_of_velocity += 1
        ar_accepting_e = pps[index_accept].get_expr()[2]
        self.equations.append(Eq(ar_accepting_e.subs(x, amt), 0))
        self.count_of_velocity += 1
        # ======
        # When heighest
        # ------
        trh = self.highest[0]  # Time of Right york Highest
        vr_highest_e = pps[1].get_expr()[1]
        v_highest_v = self.highest[1][1]  # Velocity Highest Value
        self.equations.append(Eq(vr_highest_e.subs(x, trh), v_highest_v))
        self.count_of_velocity += 1
        return self.equations[-self.count_of_velocity:]

    def how_many_smoothness_equations_available(self):
        """
        j2 = YorkCurve()
        print(j2.how_many_smoothness_equations_available())
            21
            25
            20
        """
        if self.count_of_interpolation == 0:
            self.build_interpolating_condition()
        if self.count_of_periodic == 0:
            self.build_periodic_condition()
        if self.count_of_position == 0:
            self.build_position_relation()
        if self.count_of_velocity == 0:
            self.build_velocity_condition()
        count_of_var = self.build_variables()
        result = (count_of_var -
                  self.count_of_interpolation -
                  self.count_of_periodic -
                  self.count_of_position -
                  self.count_of_velocity)
        return result

    def build_smoothness_condition(self, depths=None):
        """
        j2 = YorkCurve()
        print(j2.build_smoothness_condition())
        for i in range(len(j2.equations)):
            print(j2.equations[i])
        """
        if self.count_of_smoothness != 0:
            return self.count_of_smoothness
        if depths == None:
            depths = {
                1: 3,
                2: 3,
                3: 2,
                4: 2,
                5: 2,
                6: 2,
                7: 2,
                8: 2,
            }
        for i in depths.keys():
            ki = self.knots[i]  # Knot I
            pib = self.get_pieces()[i - 1]  # Piece Before knot I
            pia = self.get_pieces()[i]  # Piece After knot I
            # fib = pib.get_functions()
            # fia = pia.get_functions()
            eib = pib.get_expr()
            eia = pia.get_expr()
            for d in range(depths[i]):
                eq = Eq(eib[d].subs(x, ki), eia[d].subs(x, ki))
                self.equations.append(eq)
                self.count_of_smoothness += 1
        return self.equations[-self.count_of_smoothness:]

    def build_equations(self):
        """
        j2 = YorkCurve()
        print(j2.build_equations())
        for i in range(len(j2.equations)):
            print(j2.equations[i])
        """
        self.replace_touching_piece()
        if self.count_of_interpolation == 0:
            inter_equations = self.build_interpolating_condition()
            print('inter_equations:')
            print_list_items_in_row(inter_equations)
        # if self.count_of_boundary == 0:
        #     bound_equations = self.build_boundary_condition()
        #     print('bound_equations')
        #     print_list_items_in_row(bound_equations)
        if self.count_of_periodic == 0:
            period_equations = self.build_periodic_condition()
            print('period_equations')
            print_list_items_in_row(period_equations)
        if self.count_of_position == 0:
            position_equations = self.build_position_relation()
            print('position_equations')
            print_list_items_in_row(position_equations)
        if self.count_of_velocity == 0:
            velocity_equations = self.build_velocity_condition()
            print('velocity_equations')
            print_list_items_in_row(velocity_equations)
        if self.count_of_smoothness == 0:
            smoothness_equations = self.build_smoothness_condition()
            print('smoothness_equations')
            print_list_items_in_row(smoothness_equations)
        return len(self.equations)

    def get_equations(self):
        if len(self.equations) == 0:
            self.build_equations()
        return self.equations

    def solve_coefficients(self):
        """
        j2 = YorkCurve()
        print(j2.solve_coefficients())
        equations = j2.get_equations()
        variables = j2.get_variables()
        solutions = solve(equations, variables)
        """
        if self.solution != {}:
            return self.solution
        equations = self.get_equations()
        variables = self.get_variables()
        solution = linsolve(equations, variables)
        self.solution = solution
        return self.solution

    def save_solution(self):
        """
        j2 = YorkCurve()
        j2.save_solution()
        """
        output = open('york_curve_solution.pkl', 'wb')
        pickle.dump(self.solve_coefficients(), output)
        output.close()

    def load_solution(self):
        """
        j2 = YorkCurve()
        print(j2.load_solution())
        """
        pkl_file = open('york_curve_solution.pkl', 'rb')
        self.solution = pickle.load(pkl_file)
        pkl_file.close()
        return self.solution

    def update_with_solution(self):
        """
        j2 = YorkCurve()
        j2.replace_touching_piece()
        j2.update_with_solution()
        print(j2.get_pieces()[2].get_expr()[0])
        print(j2.get_pieces()[2].get_expr()[2])
        """
        self.build_variables()
        solution = self.load_solution()
        self.involve_solutions(solution)

    def save_solved_pieces(self):
        """
        j2 = YorkCurve()
        j2.save_solved_pieces()
        """
        output = open('york_curve_pieces.pkl', 'wb')
        pickle.dump(self.get_pieces(), output)
        output.close()

    def load_solved_pieces(self):
        """
        j3 = YorkCurve()
        j3.load_solved_pieces()
        print(j3.get_pieces()[2].get_expr()[0])
        """
        pkl_file = open('york_curve_pieces.pkl', 'rb')
        self.pieces = pickle.load(pkl_file)
        pkl_file.close()

    def get_kth_expr_of_ith_piece(self, k, i):
        try:
            return self.get_pieces()[i].get_expr()[k]
        except:
            return 0

    def build_spline(self):
        """
        j3 = YorkCurve()
        j3.load_solved_pieces()
        print(j3.get_pieces()[2].get_expr()[0])
        j3.build_spline()
        """
        # self.update_with_solution()
        for k in range(4):
            self.piecewise.append(Piecewise(
                (0, x < self.knots[0]),
                (self.get_kth_expr_of_ith_piece(k, 0), x <= self.knots[1]),
                (self.get_kth_expr_of_ith_piece(k, 1), x <= self.knots[2]),
                (self.get_kth_expr_of_ith_piece(k, 2), x <= self.knots[3]),
                (self.get_kth_expr_of_ith_piece(k, 3), x <= self.knots[4]),
                (self.get_kth_expr_of_ith_piece(k, 4), x <= self.knots[5]),
                (self.get_kth_expr_of_ith_piece(k, 5), x <= self.knots[6]),
                (self.get_kth_expr_of_ith_piece(k, 6), x <= self.knots[7]),
                (self.get_kth_expr_of_ith_piece(k, 7), x <= self.knots[8]),
                (self.get_kth_expr_of_ith_piece(k, 8), x <= self.knots[9]),
                (0, True)))

    def get_piecewise(self):
        """
        j2 = YorkCurve()
        j2.replace_touching_piece()
        print(j2.get_piecewise()[0])
        """
        if len(self.piecewise) == 0:
            self.build_spline()
        return self.piecewise

    def plot_svaj(self):
        """
        j3 = YorkCurve()
        j3.load_solved_pieces()
        j3.plot_svaj()
        """
        p0 = plot(0, (x, self.knots[0], self.knots[-1]),
                  title="Position",
                  ylabel="(mm)",
                  show=False)
        for i in range(self.num_of_pieces):
            expr_p_i = self.get_kth_expr_of_ith_piece(0, i)
            pi = plot(expr_p_i, (x, self.knots[i], self.knots[i + 1]),
                      show=False)
            p0.extend(pi)
        v0 = plot(0, (x, self.knots[0], self.knots[-1]),
                  title="Velocity",
                  ylabel="(mm/sec)",
                  show=False)
        for i in range(self.num_of_pieces):
            expr_v_i = self.get_kth_expr_of_ith_piece(1, i)
            vi = plot(expr_v_i, (x, self.knots[i], self.knots[i + 1]),
                      show=False)
            v0.extend(vi)
        a0 = plot(0, (x, self.knots[0], self.knots[-1]),
                  title="Acceleration",
                  ylabel="(mm/sec^2)",
                  show=False)
        for i in range(self.num_of_pieces):
            expr_a_i = self.get_kth_expr_of_ith_piece(2, i)
            ai = plot(expr_a_i, (x, self.knots[i], self.knots[i + 1]),
                      show=False)
            a0.extend(ai)
        j0 = plot(0, (x, self.knots[0], self.knots[-1]),
                  title="Jerk",
                  ylabel="(mm/sec^3)",
                  show=False)
        for i in range(self.num_of_pieces):
            expr_j_i = self.get_kth_expr_of_ith_piece(3, i)
            ji = plot(expr_j_i, (x, self.knots[i], self.knots[i + 1]),
                      show=False)
            j0.extend(ji)
        fig, (ax1, ax2, ax3, ax4) = plt.subplots(nrows=4)
        move_sympyplot_to_axes(p0, ax1)
        ax1.set_xticks([self.knots[i] for i in range(len(self.knots))])
        ax1.set_xticklabels([(i % 2) * '\n' +
                             str(time_to_degree(self.knots[i]))
                             for i in range(len(self.knots))])
        ax1.grid(True)
        move_sympyplot_to_axes(v0, ax2)
        ax2.set_xticks([self.knots[i] for i in range(len(self.knots))])
        ax2.set_xticklabels([(i % 2) * '\n' +
                             str(time_to_degree(self.knots[i]))
                             for i in range(len(self.knots))])
        ax2.grid(True)
        move_sympyplot_to_axes(a0, ax3)
        ax3.set_xticks([self.knots[i] for i in range(len(self.knots))])
        ax3.set_xticklabels([(i % 2) * '\n' +
                             str(time_to_degree(self.knots[i]))
                             for i in range(len(self.knots))])
        ax3.grid(True)
        move_sympyplot_to_axes(j0, ax4)
        ax4.set_xticks([self.knots[i] for i in range(len(self.knots))])
        ax4.set_xticklabels([(i % 2) * '\n' +
                             str(time_to_degree(self.knots[i]))
                             for i in range(len(self.knots))])
        ax4.grid(True)
        ax4.set_xlabel('machine degree')
        plt.show()

    def plt_svaj(self):
        """
        j3 = YorkCurve()
        j3.load_solved_pieces()
        j3.plt_svaj()
        """
        p0 = plot((0, (x, self.knots[0], self.knots[-1])), show=False)
        for i in range(self.num_of_pieces):
            expr_p_i = self.get_kth_expr_of_ith_piece(0, i)
            pi = plot(expr_p_i, (x, self.knots[i], self.knots[i + 1]),
                      show=False)
            p0.extend(pi)
        v0 = plot((0, (x, self.knots[0], self.knots[-1])), show=False)
        for i in range(self.num_of_pieces):
            expr_v_i = self.get_kth_expr_of_ith_piece(1, i)
            vi = plot(expr_v_i, (x, self.knots[i], self.knots[i + 1]),
                      show=False)
            v0.extend(vi)
        x1y1 = p0.get_points()
        x2y2 = v0.get_points()
        fig = plt.figure(figsize=(8, 5))
        ax1 = fig.add_subplot(121)
        ax2 = fig.add_subplot(122)

        # do subplot 1
        ax1.plot(x1y1[0], x1y1[1], 'g')  # plot x**2 in green
        ax1.set_xlim([-2, 2])
        ax1.set_xlabel('X1')
        ax1.set_ylabel('Y1')
        ax1.set_title('Line1')  # destroyed by another .title(); axis metho1

        # do subplot 2
        ax2.plot(x2y2[0], x2y2[1], 'r')  # plot x**3 in red
        ax2.set_xlim([-2, 2])
        ax2.set_xlabel('X2')
        ax2.set_ylabel('Y2')
        ax2.set_title('Line2')

        fig.subplots_adjust(wspace=0.4)  # set space between subplots

        plt.show()


def resolve_york(if_reload_touching_piece=True):
    j2 = YorkCurve()
    j2.replace_touching_piece(reload=False)
    j2.replace_touching_piece(reload=True)
    j2.solve_coefficients()
    j2.save_solution()
    j2.update_with_solution()
    j2.save_solved_pieces()
    j2.load_solved_pieces()
    j2.plot_svaj()


class Touch(ShakeHand):
    def __init__(self,
                 name='touch_curve_1',
                 start_knot=degree_to_time(82),
                 end_knot=degree_to_time(137),
                 if_rebuild_pieces=False
                 ):
        """
        t1 = Touch(if_rebuild_pieces=True)
        """
        ShakeHand.__init__(self,
                           name='shake_hand_curve_262_317',
                           start_knot=start_knot,
                           end_knot=end_knot,
                           start_position=0, end_position=nan,
                           cons_velocity=-422, mod_velocity=-122,
                           if_rebuild_pieces=False)
        self.name = name
        self.get_pieces()
        self.joy = JawOnYorkCurve()
        self.trace = TraceOfA(load_memo=True)
        self.package = Package(330, "Square", 49.5, 48.5, 124.6, 6, 190)
        if if_rebuild_pieces:
            self.modify_pieces_expr()
            self.save_solved_pieces()
        else:
            self.load_solved_pieces()

    def modify_pieces_expr(self):
        """
        t2 = Touch(if_rebuild_pieces=False)
        t2.narrow_start_and_end()
        t2.plot_svaj()
        """
        y_R_AO5_expr = self.trace.get_y_R_AO5_when_touching_expr()
        y_R_AO2_expr = self.trace.get_y_R_AO2_when_touching_expr()
        r_O5O2 = self.package.height + \
                 self.package.hs_sealing_length + \
                 self.trace.joy_mechanism_forward.r_DC_value
        expr_added = y_R_AO5_expr + r_O5O2 - y_R_AO2_expr
        value_add_to_x = degree_to_time(180)
        self.add_expr_to_pieces(expr_added, value_add_to_x)
        return self.get_pieces()

    def narrow_start_and_end(self):
        self.knots[0] += degree_to_time(6)
        self.knots[-1] -= degree_to_time(1)

    def get_touching_point_pvaj(self):
        """
        t2 = Touch(if_rebuild_pieces=False)
        print(t2.get_touching_point_pvaj())
        """
        touching_time = self.trace.get_touch_time()
        return tuple(
            [self.get_kth_expr_of_ith_piece(k, 1).subs(x, touching_time)
             for k in range(4)])

    def plot_s(self):
        """
        t1 = Touch()
        t1.modify_pieces_expr()
        """
        p0 = plot(0, (x, self.knots[0], self.knots[-1]),
                  title="Position",
                  ylabel="(mm)",
                  show=False)
        for i in range(self.num_of_pieces):
            expr_p_i = self.get_kth_expr_of_ith_piece(0, i)
            pi = plot(expr_p_i, (x, self.knots[i], self.knots[i + 1]),
                      show=False)
            p0.extend(pi)

        # v0 = plot(diff(expr, x), (x, self.knots[0], self.knots[-1]),
        #           title="Velocity",
        #           ylabel="(mm/sec)",
        #           show=False)
        # a0 = plot(diff(expr, x, 2), (x, self.knots[0], self.knots[-1]),
        #           title="Acceleration",
        #           ylabel="(mm/sec^2)",
        #           show=False)
        # j0 = plot(diff(expr, x, 3), (x, self.knots[0], self.knots[-1]),
        #           title="Jerk",
        #           ylabel="(mm/sec^3)",
        #           show=False)
        fig, (ax1, ax2, ax3, ax4) = plt.subplots(nrows=4)
        move_sympyplot_to_axes(p0, ax1)
        ax1.set_xticks([self.knots[i] for i in range(len(self.knots))])
        ax1.set_xticklabels([(i % 2) * '\n' +
                             str(time_to_degree(self.knots[i]))
                             for i in range(len(self.knots))])
        ax1.grid(True)
        # move_sympyplot_to_axes(v0, ax2)
        # ax2.set_xticks([self.knots[i] for i in range(len(self.knots))])
        # ax2.set_xticklabels([(i % 2) * '\n' +
        #                      str(time_to_degree(self.knots[i]))
        #                      for i in range(len(self.knots))])
        # ax2.grid(True)
        # move_sympyplot_to_axes(a0, ax3)
        # ax3.set_xticks([self.knots[i] for i in range(len(self.knots))])
        # ax3.set_xticklabels([(i % 2) * '\n' +
        #                      str(time_to_degree(self.knots[i]))
        #                      for i in range(len(self.knots))])
        # ax3.grid(True)
        # move_sympyplot_to_axes(j0, ax4)
        # ax4.set_xticks([self.knots[i] for i in range(len(self.knots))])
        # ax4.set_xticklabels([(i % 2) * '\n' +
        #                      str(time_to_degree(self.knots[i]))
        #                      for i in range(len(self.knots))])
        # ax4.grid(True)
        # ax4.set_xlabel('machine degree')
        plt.show()


if __name__ == '__main__':
    pass
    # resolve_york()

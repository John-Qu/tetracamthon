from sympy import nan, Eq, Piecewise, solve, lambdify, diff, symbols, \
    Symbol, plot
from sympy.abc import x
import numpy as np
from helper_functions import degree_to_time, time_to_degree, \
    move_sympyplot_to_axes
from polynomial_spline import SplineWithPiecewisePolynomial
from analysis import O4DriveA, ANeedO4
from packages import Package
import pickle
import matplotlib.pyplot as plt


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
        if knots is None:
            knots = np.array([start[0], widest[0], closed[0],
                              open[0], end[0]])
        if pvajp is None:
            pvajp = np.array([[start[1][i], widest[1][i], closed[1][i],
                               open[1][i], end[1][i]] for i in range(5)])
        if orders is None:
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

    def build_smoothness_condition(self):
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
        except IndexError:
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
            File "/Users/johnqu/.conda/envs/Tetracamthon/lib/python3.7/site
            -packages/numpy/lib/scimath.py", line 226, in sqrt
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
                        num=num, endpoint=True)
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


class ShakeHand(SplineWithPiecewisePolynomial):
    # def __init__(self, start_knot=0.3625, end_knot=0.4825,
    #              start_position=0, end_position=symbols('end_p'),
    #              cons_velocity=-422, mod_velocity=-122):
    def __init__(self, name='shake_hand_curve_1',
                 start_knot=degree_to_time(262),
                 end_knot=degree_to_time(317),
                 start_position=0, end_position=nan,
                 cons_velocity=-422, mod_velocity=-122,
                 if_rebuild_pieces=False):
        """
        s1 = ShakeHand(name='shake_hand_curve_262_317', if_rebuild_pieces=True)
        """
        self.start_knot = start_knot
        self.end_knot = end_knot
        self.start_p = start_position
        self.end_p = end_position
        self.cons_v = cons_velocity
        self.mod_v = mod_velocity
        delta = self.end_knot - self.start_knot
        knots = np.array([
            self.start_knot,
            self.start_knot + delta / 10 * 2,
            self.start_knot + delta / 10 * 3,
            self.start_knot + delta / 2,
            self.end_knot - delta / 10 * 3,
            self.end_knot - delta / 10 * 2,
            self.end_knot
        ])
        pvajp = [
            [self.start_p, nan, nan, nan, nan, nan, self.end_p],
            [self.cons_v, nan, nan, self.mod_v, nan, nan, self.cons_v],
            [0, nan, nan, 0, nan, nan, 0],
            [0, 0, nan, nan, nan, 0, 0],
            [nan, nan, 0, nan, 0, nan, nan]
        ]
        orders = [6 for i in range(len(knots) - 1)]
        SplineWithPiecewisePolynomial.__init__(self, knots, orders, pvajp,
                                               name=name)
        if if_rebuild_pieces:
            self.update_with_solution()
            self.save_solved_pieces()
        else:
            self.load_solved_pieces()

    def build_smoothness_condition(self, depths=None):
        """
        s1 = ShakeHand(if_save_pieces=False, if_load_pieces=False)
        print(len(s1.build_smoothness_condition()))
        print(len(s1.build_interpolating_condition()))
        for i in range(len(s1.equations)):
            print(s1.equations[i])
        """
        if self.count_of_smoothness != 0:
            return self.count_of_smoothness
        if depths is None:
            depths = {
                1: 5,
                2: 4,
                3: 5,
                4: 4,
                5: 5
            }
        for i in depths.keys():
            ki = self.knots[i]  # Knot I
            pib = self.get_pieces()[i - 1]  # Piece Before knot I
            pia = self.get_pieces()[i]  # Piece After knot I
            eib = pib.get_expr()
            eia = pia.get_expr()
            for d in range(depths[i]):
                eq = Eq(eib[d].subs(x, ki), eia[d].subs(x, ki))
                self.equations.append(eq)
                self.count_of_smoothness += 1
        return self.equations[-self.count_of_smoothness:]

    def build_spline(self):
        """
        s1 = ShakeHand(if_save_pieces=True, if_load_pieces=False)
        s1 = ShakeHand(if_save_pieces=False, if_load_pieces=True)
        s1.build_spline()
        s1.plot_svaj()
        """
        for k in range(4):
            self.piecewise.append(Piecewise(
                (0, x < self.knots[0]),
                (self.get_kth_expr_of_ith_piece(k, 0), x <= self.knots[1]),
                (self.get_kth_expr_of_ith_piece(k, 1), x <= self.knots[2]),
                (self.get_kth_expr_of_ith_piece(k, 2), x <= self.knots[3]),
                (self.get_kth_expr_of_ith_piece(k, 3), x <= self.knots[4]),
                (self.get_kth_expr_of_ith_piece(k, 4), x <= self.knots[5]),
                (self.get_kth_expr_of_ith_piece(k, 5), x <= self.knots[6]),
                (0, True)))

    def get_piecewise(self):
        """
        s1 = ShakeHand()
        print(s1.get_piecewise()[0])
        s1.plot_svaj()
        """
        if len(self.piecewise) == 0:
            self.build_spline()
        return self.piecewise


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
        r_O5O2 = (self.package.height +
                  self.package.hs_sealing_length +
                  self.trace.joy_mechanism_forward.r_DC_value)
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


class Pull(SplineWithPiecewisePolynomial):
    def __init__(self, name='constant_velocity_pull_1',
                 start_knot=0, end_knot=0.45,
                 start_position=0, end_position=nan,
                 cons_velocity=-422):
        """
        s2 = SmoothPulling()
        """
        self.start_knot = start_knot
        self.end_knot = end_knot
        self.start_p = start_position
        self.end_p = end_position
        self.cons_v = cons_velocity
        knots = np.array([
            self.start_knot,
            self.end_knot
        ])
        pvajp = [
            [self.start_p, self.end_p],
            [self.cons_v, nan],
            [nan, nan],
            [nan, nan],
            [nan, nan]
        ]
        orders = [2 for i in range(len(knots) - 1)]
        SplineWithPiecewisePolynomial.__init__(self, knots, orders, pvajp,
                                               name=name)

    def build_equations(self):
        """
        s1 = SplineWithPiecewisePolynomial()
        print(len(s1.build_equations()))
        """
        if self.count_of_interpolation == 0:
            self.build_interpolating_condition()
        return self.equations

    def build_spline(self):
        """
        s2 = SmoothPulling()
        s2.update_with_solution()
        s2.build_spline()
        """
        for k in range(4):
            self.piecewise.append(Piecewise(
                (0, x < self.knots[0]),
                (self.get_kth_expr_of_ith_piece(k, 0), x <= self.knots[1]),
                (0, True)))

    def get_piecewise(self):
        """
        s2 = SmoothPulling()
        print(s2.get_piecewise()[0])
        """
        if len(self.piecewise) == 0:
            self.build_spline()
        return self.piecewise


class Climb(SplineWithPiecewisePolynomial):
    def __init__(self, name='climb_up_curve_325_92',
                 start_knot=degree_to_time(-35),
                 cross_knot=degree_to_time(43),
                 high_knot=degree_to_time(84),
                 touch_knot=degree_to_time(92),
                 start_p=-50,
                 cross_p=200,
                 high_p=372.2,
                 touch_p=365,
                 start_v=-422,
                 touch_v=-200,
                 touch_a=-4444,
                 touch_j=500000):
        """
        s3 = ClimbUp()
        """
        self.name = name
        knots = np.array([
            start_knot,
            degree_to_time(-25),
            degree_to_time(-18),
            0,
            # cross_knot,
            # high_knot,
            touch_knot
        ])
        pvajp = [
            # [start_p, 0, cross_p, high_p, touch_p],
            # [start_v, 0, nan, 0, touch_v],
            # [0, nan, nan, nan, touch_a],
            # [nan, nan, nan, nan, touch_j],
            # [nan, nan, nan, nan, nan]
            [start_p, nan, nan, 0, touch_p],
            [start_v, nan, -430, 0, touch_v],
            [0, -5700, nan, nan, touch_a],
            [nan, 0, nan, nan, nan],
            [nan, nan, nan, nan, nan]
        ]
        orders = [6 for i in range(len(knots) - 1)]
        SplineWithPiecewisePolynomial.__init__(self, knots, orders, pvajp,
                                               name=name)

    def build_smoothness_condition(self, depths=None):
        """
        s3 = ClimbUp()
        print(len(s3.build_smoothness_condition()))
        for i in range(len(s3.equations)):
            print(s3.equations[i])
        s3 = ClimbUp()
        s3.update_with_solution()
        s3.plot_svaj()
        """
        if self.count_of_smoothness != 0:
            return self.count_of_smoothness
        if depths is None:
            depths = {
                1: 4,
                2: 4,
                3: 4,
            }
        for i in depths.keys():
            ki = self.knots[i]  # Knot I
            pib = self.get_pieces()[i - 1]  # Piece Before knot I
            pia = self.get_pieces()[i]  # Piece After knot I
            eib = pib.get_expr()
            eia = pia.get_expr()
            for d in range(depths[i]):
                eq = Eq(eib[d].subs(x, ki), eia[d].subs(x, ki))
                self.equations.append(eq)
                self.count_of_smoothness += 1
        return self.equations[-self.count_of_smoothness:]


class Throw(SplineWithPiecewisePolynomial):
    def __init__(self, name='climb_up_curve_325_92',
                 start_knot=degree_to_time(-35),
                 cross_knot=degree_to_time(43),
                 high_knot=degree_to_time(84),
                 touch_knot=degree_to_time(92),
                 start_p=-50,
                 cross_p=200,
                 high_p=372.2,
                 touch_p=365,
                 start_v=-422,
                 touch_v=-200,
                 touch_a=-4444,
                 touch_j=500000):
        """
        s3 = ClimbUp()
        """
        self.name = name
        knots = np.array([
            start_knot,
            degree_to_time(-25),
            degree_to_time(-18),
            0,
            # cross_knot,
            # high_knot,
            touch_knot
        ])
        pvajp = [
            # [start_p, 0, cross_p, high_p, touch_p],
            # [start_v, 0, nan, 0, touch_v],
            # [0, nan, nan, nan, touch_a],
            # [nan, nan, nan, nan, touch_j],
            # [nan, nan, nan, nan, nan]
            [start_p, nan, nan, 0, touch_p],
            [start_v, nan, -430, 0, touch_v],
            [0, -5700, nan, nan, touch_a],
            [nan, 0, nan, nan, nan],
            [nan, nan, nan, nan, nan]
        ]
        orders = [6 for i in range(len(knots) - 1)]
        SplineWithPiecewisePolynomial.__init__(self, knots, orders, pvajp,
                                               name=name)

    def build_smoothness_condition(self, depths=None):
        """
        s3 = ClimbUp()
        print(len(s3.build_smoothness_condition()))
        for i in range(len(s3.equations)):
            print(s3.equations[i])
        s3 = ClimbUp()
        s3.update_with_solution()
        s3.plot_svaj()
        """
        if self.count_of_smoothness != 0:
            return self.count_of_smoothness
        if depths is None:
            depths = {
                1: 4,
                2: 4,
                3: 4,
            }
        for i in depths.keys():
            ki = self.knots[i]  # Knot I
            pib = self.get_pieces()[i - 1]  # Piece Before knot I
            pia = self.get_pieces()[i]  # Piece After knot I
            eib = pib.get_expr()
            eia = pia.get_expr()
            for d in range(depths[i]):
                eq = Eq(eib[d].subs(x, ki), eia[d].subs(x, ki))
                self.equations.append(eq)
                self.count_of_smoothness += 1
        return self.equations[-self.count_of_smoothness:]


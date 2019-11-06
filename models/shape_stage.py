from sympy import nan, Eq, Piecewise, solve, lambdify, diff, symbols, \
    Symbol, plot
from sympy.abc import x
import numpy as np
from helper_functions import degree_to_time, time_to_degree, \
    move_sympyplot_to_axes
from polynomial_spline import SplineWithPiecewisePolynomial, Polynomial
from analysis import O4DriveA, ANeedO4
from packages import Package
import pickle
import matplotlib.pyplot as plt


class JawOnYorkCurve(SplineWithPiecewisePolynomial):
    """
    """
    def __init__(self, name="jaw_on_york_relative",
                 start=None, widest=None, closed=None,
                 release=None, end=None,
                 whether_rebuild_pieces=False):
        if start is None:
            start = (degree_to_time(0), (
                nan,
                nan,
                nan,
                nan,
                nan,
            ))
        knot1 = (degree_to_time(30), (
            nan,
            nan,
            nan,
            0,
            nan,
        ))
        if widest is None:
            widest = (degree_to_time(43), (
                -131,
                0,
                nan,
                nan,
                nan,
            ))
        knot4 = (degree_to_time(90), (
            nan,
            nan,
            0,
            nan,
            nan,
        ))
        knot2 = (degree_to_time(120), (
            nan,
            nan,
            nan,
            0,
            nan,
        ))
        if closed is None:
            closed = (degree_to_time(138), (
                0,
                0,
                0,
                nan,
                nan,
            ))
        if release is None:
            release = (degree_to_time(330), (
                0,
                0,
                0,
                nan,
                nan,
            ))
        knot3 = (degree_to_time(345), (
            nan,
            nan,
            nan,
            0,
            nan,
        ))
        if end is None:
            end = (degree_to_time(360), (
                nan,
                nan,
                nan,
                nan,
                nan,
            ))
        key_knots= [
            start, knot1, widest, knot4, knot2, closed, release, knot3, end
        ]
        smooth_depth = {
            # 1: 4,
            # 2: 6,
            # 3: 4,
            # 4: 4,
            # 5: 4,
            # 6: 4,
            # 7: 4,
            knot1: 4,
            widest: 6,
            knot4: 4,
            knot2: 4,
            closed: 4,
            release: 4,
            knot3: 4,
        }
        self.periodic_depth = 6
        orders = [6] * len(key_knots)
        SplineWithPiecewisePolynomial.__init__(self,
                                               key_knots=key_knots,
                                               orders=orders,
                                               smooth_depth=smooth_depth,
                                               name=name)
        # if whether_rebuild_pieces:
        #     self.update_with_solution()
        #     # self.save_solved_pieces()
        # else:
        #     self.load_solved_pieces()

    def build_equations(self):
        """
        j1 = JawOnYorkCurve(whether_rebuild_pieces=True)
        j1.update_with_solution()
        j1.plot_svaj()
        j2 = JawOnYorkCurve(whether_rebuild_pieces=False)
        j2.plot_svaj()
        """
        if self.count_of_interpolation == 0:
            self.build_interpolating_condition()
        if self.count_of_smoothness == 0:
            self.build_smoothness_condition(depths=self.smooth_depth)
        if self.count_of_periodic == 0:
            self.build_periodic_condition(depth=self.periodic_depth)
        return self.equations

    def build_spline(self):
        """
        j1 = JawOnYorkCurve(whether_rebuild_pieces=False)
        j1.get_piecewise()
        """
        if len(self.piecewise) != 0:
            return self.piecewise
        for k in range(max(self.orders)):
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
                (0, True)))
        return self.piecewise


class TraceOfA(object):
    def __init__(self, whether_load_memo=True):
        """
        t1 = TraceOfA(load_memo=False)
        """
        # Jaw on York spline Curve
        self.joy_curve = JawOnYorkCurve(whether_rebuild_pieces=False)
        # Jaw on York mechanism analysis driving forward
        self.joy_mechanism_forward = O4DriveA()
        # Jaw on York mechanism analysis driving backward
        self.joy_mechanism_backward = ANeedO4()
        self.package = Package(330, "Square", 49.5, 48.5, 124.6, 6, 190)
        if whether_load_memo:
            self.load_memo_from_file()
        else:
            self.memo = {}
            self.plot_svaj()
            self.save_memo_to_file()

    def save_memo_to_file(self):
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
         r_O4O2_touch = t1.get_touch_rO4O2()
        r_O4O2_close = t1.get_close_rO4O2()
        position_touch = - (r_O4O2_touch - r_O4O2_close)
        curve = t1.joy_curve.get_kth_expr_of_ith_piece(0, 3)
        equation = Eq(curve, position_touch)
        touch_time = solve(equation, x)
        print(touch_time)
            0.243849713905805
        """
        if 'touch_time' in self.memo:
            return self.memo['touch_time']
        r_O4O2_touch = self.get_touch_rO4O2()
        r_O4O2_close = self.get_close_rO4O2()
        position_touch = - (r_O4O2_touch - r_O4O2_close)
        curve = self.joy_curve.get_kth_expr_of_ith_piece(0, 3)
        equation = Eq(curve, position_touch)
        touch_time = solve(equation, x)[0]
        self.memo['touch_time'] = touch_time
        return touch_time

    def get_touch_degree(self):
        """
        t1 = TraceOfA()
        print(t1.get_touch_degree())
            93.0247577030154
            97.5398855623221
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
            164.603098392656
        :return:
        """
        if 'y_R_AO2_when_touching_expr' in self.memo:
            return self.memo['y_R_AO2_when_touching_expr']
        expr = self.joy_mechanism_forward.get_y_R_AO2_of_r_O4O2_expr()
        r_O4O2_symbol = self.joy_mechanism_forward.r_O4O2
        curve = self.joy_curve.get_kth_expr_of_ith_piece(0, 3)
        r_O4O2_close = self.get_close_rO4O2()
        r_O4O2_value = - (curve - r_O4O2_close)
        y_R_AO2_when_touching_expr = expr.subs(r_O4O2_symbol, r_O4O2_value)
        self.memo['y_R_AO2_when_touching_expr'] = y_R_AO2_when_touching_expr
        return y_R_AO2_when_touching_expr

    def get_y_R_AO2_when_closing_expr(self):
        """
        t1 = TraceOfA()
        print(t1.get_y_R_AO2_when_touching_expr())
        print(t1.get_y_R_AO2_when_touching_expr().subs(x, t1.get_touch_time()))
            171.354752195555
        print(t1.get_y_R_AO2_when_closing_expr().subs(x, degree_to_time(138)))
            164.440000000000
        :return:
        """
        if 'y_R_AO2_when_closing_expr' in self.memo:
            return self.memo['y_R_AO2_when_closing_expr']
        expr = self.joy_mechanism_forward.get_y_R_AO2_of_r_O4O2_expr()
        r_O4O2_symbol = self.joy_mechanism_forward.r_O4O2
        curve_closing = self.joy_curve.get_kth_expr_of_ith_piece(0, 4)
        r_O4O2_close = self.get_close_rO4O2()
        r_O4O2_value = - (curve_closing - r_O4O2_close)
        y_R_AO2_when_closing_expr = expr.subs(r_O4O2_symbol, r_O4O2_value)
        self.memo['y_R_AO2_when_closing_expr'] = y_R_AO2_when_closing_expr
        return y_R_AO2_when_closing_expr

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
        curve = self.joy_curve.get_kth_expr_of_ith_piece(0, 3)
        r_O4O2_close = self.get_close_rO4O2()
        r_O4O2_value = - (curve - r_O4O2_close)
        x_R_AO2_when_touching_expr = expr.subs(r_O4O2_symbol, r_O4O2_value)
        self.memo['x_R_AO2_when_touching_expr'] = x_R_AO2_when_touching_expr
        return x_R_AO2_when_touching_expr

    def get_x_R_AO2_when_closing_expr(self):
        """
        t1 = TraceOfA()
        print(t1.get_x_R_AO2_when_closing_expr().subs(x, degree_to_time(138)))
            -7.81597009336110e-14
        """
        if 'x_R_AO2_when_closing_expr' in self.memo:
            return self.memo['x_R_AO2_when_closing_expr']
        expr = self.joy_mechanism_forward.get_x_R_AO2_of_r_O4O2_expr()
        r_O4O2_symbol = self.joy_mechanism_forward.r_O4O2
        curve_closing = self.joy_curve.get_kth_expr_of_ith_piece(0, 4)
        r_O4O2_close = self.get_close_rO4O2()
        r_O4O2_value = - (curve_closing - r_O4O2_close)
        x_R_AO2_when_closing_expr = expr.subs(r_O4O2_symbol, r_O4O2_value)
        self.memo['x_R_AO2_when_closing_expr'] = x_R_AO2_when_closing_expr
        return x_R_AO2_when_closing_expr

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
        return y_R_AO5_when_touching_expr

    def get_y_R_AO5_when_closing_expr(self):
        """
        t1 = TraceOfA()
        print(t1.get_y_R_AO5_when_closing_expr())
        print(t1.get_y_R_AO5_when_closing_expr().subs(x, degree_to_time(138)))
            1.93692169299983e-6
        """
        if 'y_R_AO5_when_closing_expr' in self.memo:
            return self.memo['y_R_AO5_when_closing_expr']
        x_R_AO2_when_closing_expr = \
            self.get_x_R_AO2_when_closing_expr()
        x_R_AO5_when_closing_expr = x_R_AO2_when_closing_expr
        r_AG = self.package.depth / 2
        y_R_AO5_when_closing_expr = \
            (r_AG ** 2 - (r_AG + x_R_AO5_when_closing_expr) ** 2) ** 0.5
        self.memo['y_R_AO5_when_closing_expr'] = y_R_AO5_when_closing_expr
        return y_R_AO5_when_closing_expr

    def get_x_V_AO5_when_touching_expr(self):
        if 'x_V_AO5_when_touching' in self.memo:
            return self.memo['x_V_AO5_when_touching']
        x_V_AO5_when_touching = diff(self.get_x_R_AO2_when_touching_expr(), x)
        self.memo['x_V_AO5_when_touching'] = x_V_AO5_when_touching
        return self.memo['x_V_AO5_when_touching']

    def get_y_V_AO5_when_touching_expr(self):
        if 'y_V_AO5_when_touching' in self.memo:
            return self.memo['y_V_AO5_when_touching']
        y_V_AO5_when_touching = diff(self.get_y_R_AO5_when_touching_expr(), x)
        self.memo['y_V_AO5_when_touching'] = y_V_AO5_when_touching
        return self.memo['y_V_AO5_when_touching']

    def get_x_A_AO5_when_touching_expr(self):
        if 'x_A_AO5_when_touching' in self.memo:
            return self.memo['x_A_AO5_when_touching']
        x_A_AO5_when_touching = diff(self.get_x_V_AO5_when_touching_expr(), x)
        self.memo['x_A_AO5_when_touching'] = x_A_AO5_when_touching
        return self.memo['x_A_AO5_when_touching']

    def get_y_A_AO5_when_touching_expr(self):
        if 'y_A_AO5_when_touching' in self.memo:
            return self.memo['y_A_AO5_when_touching']
        y_A_AO5_when_touching = diff(self.get_y_V_AO5_when_touching_expr(), x)
        self.memo['y_A_AO5_when_touching'] = y_A_AO5_when_touching
        return self.memo['y_A_AO5_when_touching']

    def get_x_V_AO5_when_closing_expr(self):
        if 'x_V_AO5_when_closing' in self.memo:
            return self.memo['x_V_AO5_when_closing']
        x_V_AO5_when_closing = diff(self.get_x_R_AO2_when_closing_expr(), x)
        self.memo['x_V_AO5_when_closing'] = x_V_AO5_when_closing
        return self.memo['x_V_AO5_when_closing']

    def get_y_V_AO5_when_closing_expr(self):
        if 'y_V_AO5_when_closing' in self.memo:
            return self.memo['y_V_AO5_when_closing']
        y_V_AO5_when_closing = diff(self.get_y_R_AO5_when_closing_expr(), x)
        self.memo['y_V_AO5_when_closing'] = y_V_AO5_when_closing
        return self.memo['y_V_AO5_when_closing']

    def get_x_A_AO5_when_closing_expr(self):
        if 'x_A_AO5_when_closing' in self.memo:
            return self.memo['x_A_AO5_when_closing']
        x_A_AO5_when_closing = diff(self.get_x_V_AO5_when_closing_expr(), x)
        self.memo['x_A_AO5_when_closing'] = x_A_AO5_when_closing
        return self.memo['x_A_AO5_when_closing']

    def get_y_A_AO5_when_closing_expr(self):
        if 'y_A_AO5_when_closing' in self.memo:
            return self.memo['y_A_AO5_when_closing']
        y_A_AO5_when_closing = diff(self.get_y_V_AO5_when_closing_expr(), x)
        self.memo['y_A_AO5_when_closing'] = y_A_AO5_when_closing
        return self.memo['y_A_AO5_when_closing']

    def plot_svaj(self):
        """
        t1 = TraceOfA()
        t1.plot_svaj()
        """
        start_time = float(self.get_touch_time())
        knot120 = degree_to_time(120)
        end_time = float(degree_to_time(138))
        knots = [start_time, knot120, end_time]
        # Plot jaw on york curve on touching and closing stage
        # Position
        plot_joy_curve_p = plot(0, (x, knots[0], knots[-1]),
                                title="Position of jaw on york curve",
                                ylabel="(mm)",
                                show=False)
        for i in range(2):
            expr_joy_curve_p_i = \
                self.joy_curve.get_kth_expr_of_ith_piece(0, 3 + i)
            plot_joy_curve_p_i = plot(expr_joy_curve_p_i,
                                      (x, knots[i], knots[i + 1]),
                                      show=False)
            plot_joy_curve_p.extend(plot_joy_curve_p_i)
        # Plot jaw on york curve on touching and closing stage
        # Velocity
        plot_joy_curve_v = plot(0, (x, knots[0], knots[-1]),
                                title="Velocity of jaw on york curve",
                                ylabel="(mm/s)",
                                show=False)
        for i in range(2):
            joy_curve_v_expr_i = \
                self.joy_curve.get_kth_expr_of_ith_piece(1, 3 + i)
            plot_joy_curve_v_i = plot(joy_curve_v_expr_i,
                                      (x, knots[i], knots[i + 1]),
                                      show=False)
            plot_joy_curve_v.extend(plot_joy_curve_v_i)
        # Plot A to O5 curve on touching and closing stage
        # xy of A position
        plot_xy_R_AO5 = plot(0, (x, knots[0], knots[-1]),
                             title="xy of A to O5 position",
                             ylabel="(mm)",
                             show=False)
        x_R_AO5_expr = [self.get_x_R_AO2_when_touching_expr(),
                        self.get_x_R_AO2_when_closing_expr()]
        y_R_AO5_expr = [self.get_y_R_AO5_when_touching_expr(),
                        self.get_y_R_AO5_when_closing_expr()]
        for i in range(2):
            plot_x_R_AO5_i = plot(x_R_AO5_expr[i],
                                  (x, knots[i], knots[i + 1]),
                                  show=False)
            plot_y_R_AO5_i = plot(y_R_AO5_expr[i],
                                  (x, knots[i], knots[i + 1]),
                                  show=False)
            plot_xy_R_AO5.extend(plot_x_R_AO5_i)
            plot_xy_R_AO5.extend(plot_y_R_AO5_i)
        # Plot A to O5 curve on touching and closing stage
        # xy of A velocity
        plot_xy_V_AO5 = plot(0, (x, knots[0], knots[-1]),
                             title="xy of A to O5 velocity",
                             ylabel="(mm/s)",
                             show=False)
        x_V_AO5_expr = [self.get_x_V_AO5_when_touching_expr(),
                        self.get_x_V_AO5_when_closing_expr()]
        y_V_AO5_expr = [self.get_y_V_AO5_when_touching_expr(),
                        self.get_y_V_AO5_when_closing_expr()]
        for i in range(2):
            plot_x_V_AO5_i = plot(x_V_AO5_expr[i],
                                  (x, knots[i], knots[i + 1]),
                                  show=False)
            plot_y_V_AO5_i = plot(y_V_AO5_expr[i],
                                  (x, knots[i], knots[i + 1]),
                                  show=False)
            plot_xy_V_AO5.extend(plot_x_V_AO5_i)
            plot_xy_V_AO5.extend(plot_y_V_AO5_i)
        # Plot A to O5 curve on touching and closing stage
        # xy of A acceleration
        plot_xy_A_AO5 = plot(0, (x, knots[0], knots[-1]),
                             title="xy of A to O5 acceleration",
                             ylabel="(mm/s^2)",
                             show=False)
        x_A_AO5_expr = [self.get_x_A_AO5_when_touching_expr(),
                        self.get_x_A_AO5_when_closing_expr()]
        y_A_AO5_expr = [self.get_y_A_AO5_when_touching_expr(),
                        self.get_y_A_AO5_when_closing_expr()]
        for i in range(2):
            plot_x_A_AO5_i = plot(x_A_AO5_expr[i],
                                  (x, knots[i], knots[i + 1]),
                                  show=False)
            plot_y_A_AO5_i = plot(y_A_AO5_expr[i],
                                  (x, knots[i], knots[i + 1]),
                                  show=False)
            plot_xy_A_AO5.extend(plot_x_A_AO5_i)
            plot_xy_A_AO5.extend(plot_y_A_AO5_i)

        fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(nrows=5)
        move_sympyplot_to_axes(plot_joy_curve_p, ax1)
        ax1.set_xticks([knots[i] for i in range(len(knots))])
        ax1.set_xticklabels([(i % 2) * '\n' +
                             str(time_to_degree(knots[i]))
                             for i in range(len(knots))])
        ax1.grid(True)
        move_sympyplot_to_axes(plot_joy_curve_v, ax2)
        ax2.set_xticks([knots[i] for i in range(len(knots))])
        ax2.set_xticklabels([(i % 2) * '\n' +
                             str(time_to_degree(knots[i]))
                             for i in range(len(knots))])
        ax2.grid(True)
        move_sympyplot_to_axes(plot_xy_R_AO5, ax3)
        ax3.set_xticks([knots[i] for i in range(len(knots))])
        ax3.set_xticklabels([(i % 2) * '\n' +
                             str(time_to_degree(knots[i]))
                             for i in range(len(knots))])
        ax3.grid(True)
        move_sympyplot_to_axes(plot_xy_V_AO5, ax4)
        ax4.set_xticks([knots[i] for i in range(len(knots))])
        ax4.set_xticklabels([(i % 2) * '\n' +
                             str(time_to_degree(knots[i]))
                             for i in range(len(knots))])
        ax4.grid(True)
        move_sympyplot_to_axes(plot_xy_A_AO5, ax5)
        ax5.set_xticks([knots[i] for i in range(len(knots))])
        ax5.set_xticklabels([(i % 2) * '\n' +
                             str(time_to_degree(knots[i]))
                             for i in range(len(knots))])
        ax5.grid(True)
        ax5.set_xlabel('machine degree')
        plt.show()

    # def plot_numerical(self, num=360):
    #     """
    #     t1 = TraceOfA()
    #     t1.plot_numerical()
    #     """
    #     start_time = float(self.get_touch_time())
    #     end_time = float(degree_to_time(138 - 1))
    #     t = np.linspace(start_time,
    #                     end_time,
    #                     num=num, endpoint=True)
    #     degree = time_to_degree(t)
    #     x_R_AO5_e = self.get_x_R_AO2_when_touching_expr()
    #     x_R_AO5_f = lambdify(x, x_R_AO5_e)
    #     y_R_AO5_e = self.get_y_R_AO5_when_touching_expr()
    #     y_R_AO5_f = lambdify(x, y_R_AO5_e)
    #     y_V_AO5_e = diff(y_R_AO5_e, x)
    #     y_V_AO5_f = lambdify(x, y_V_AO5_e)
    #     y_A_AO5_e = diff(y_V_AO5_e, x)
    #     y_A_AO5_f = lambdify(x, y_A_AO5_e)
    #     fig = plt.figure(figsize=(15, 12), dpi=80)
    #     fig.suptitle('R_AO5 SVA curves.', fontsize='x-large')
    #     plt.subplot(4, 1, 1)
    #     plt.grid()
    #     plt.ylabel("x position of AtoO5 (mm)")
    #     plt.plot(degree, x_R_AO5_f(t),
    #              color="blue", linewidth=3.0, linestyle="-")
    #     plt.xlim(time_to_degree(start_time), time_to_degree(end_time))
    #     plt.subplot(4, 1, 2)
    #     plt.grid()
    #     plt.ylabel("y position of AtoO5 (mm)")
    #     plt.plot(degree, y_R_AO5_f(t),
    #              color="blue", linewidth=3.0, linestyle="-")
    #     plt.xlim(time_to_degree(start_time), time_to_degree(end_time))
    #     plt.subplot(4, 1, 3)
    #     plt.grid()
    #     plt.ylabel("y velocity of AtoO5 (mm/s)")
    #     plt.plot(degree, y_V_AO5_f(t),
    #              color="blue", linewidth=3.0, linestyle="-")
    #     plt.xlim(time_to_degree(start_time), time_to_degree(end_time))
    #     plt.subplot(4, 1, 4)
    #     plt.grid()
    #     plt.ylabel("y acceleration of AtoO5 (m/s^2)")
    #     plt.plot(degree, y_A_AO5_f(t) / 1000,
    #              color="blue", linewidth=3.0, linestyle="-")
    #     plt.xlim(time_to_degree(start_time), time_to_degree(end_time))
    #     plt.savefig("Track of A to O5 curves.png", dpi=720)


class ShakeHand(SplineWithPiecewisePolynomial):
    # def __init__(self, start_knot=0.3625, end_knot=0.4825,
    #              start_position=0, end_position=symbols('end_p'),
    #              cons_velocity=-422, mod_velocity=-122):
    def __init__(self, name='shake_hand_curve_1',
                 start=None, knot1=None, knot2=None, knot3=None, knot4=None,
                 knot5=None, end=None,
                 if_rebuild_pieces=False):
        """
        s1 = ShakeHand(name='shake_hand_curve_264_318', if_rebuild_pieces=True)
        s1 = ShakeHand(name='shake_hand_curve_264_318', if_rebuild_pieces=False)
        s1.plot_svaj(whether_save_png=True)
        """
        if start is None:
            start = (degree_to_time(264), (
                0,
                -422,
                0,
                nan,
                nan,
            ))
        if knot1 is None:
            knot1 = (degree_to_time(274.8), (
                nan,
                nan,
                nan,
                0,
                nan,
            ))
        if knot2 is None:
            knot2 = (degree_to_time(282), (
                nan,
                nan,
                nan,
                nan,
                0,
            ))
        if knot3 is None:
            knot3 = (degree_to_time(291), (
                nan,
                nan,
                0,
                nan,
                0,
            ))
        if knot4 is None:
            knot4 = (degree_to_time(300), (
                nan,
                nan,
                nan,
                nan,
                0,
            ))
        if knot5 is None:
            knot5 = (degree_to_time(307.2), (
                nan,
                nan,
                nan,
                0,
                nan,
            ))
        if end is None:
            end = (degree_to_time(318), (
                degree_to_time(318-264)*(-422) + 24.25,
                -422,
                0,
                nan,
                nan,
            ))
        self.took_knot_at = [start, knot1, knot2, knot3, knot4, knot5, end]
        smooth_depth = {
            knot1: 5,
            knot2: 5,
            knot3: 5,
            knot4: 4,
            knot5: 5,
        }
        knots = [self.took_knot_at[i][0]
                 for i in range(len(self.took_knot_at))]
        pvajp = [[self.took_knot_at[i][1][j]
                  for i in range(len(self.took_knot_at))]
                 for j in range(5)]
        orders = [6] * len(self.took_knot_at)
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
                2: 5,
                3: 5,
                4: 4,
                5: 5
            }
        for i in range(1, len(self.took_knot_at) - 1):
            kpi = self.took_knot_at[i]  # Knot Point I
            ki = kpi[0]
            pib = self.get_pieces()[i - 1]  # Piece Before knot I
            pia = self.get_pieces()[i]  # Piece After knot I
            eib = pib.get_expr()
            eia = pia.get_expr()
            for d in range(depths[kpi]):
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


class Touch(SplineWithPiecewisePolynomial):
    def __init__(self,
                 name='touch_curve_1',
                 touch=None, knot2=None, knot3=None,
                 knot4=None, knot5=None, end=None,
                 if_rebuild_pieces=False):
        """
        t1 = Touch(if_rebuild_pieces=True)
        """
        self.trace = TraceOfA(whether_load_memo=True)
        if touch is None:
            touch = (self.trace.get_touch_time(), (
                nan,
                nan,
                nan,
                nan,
                nan,
            ))
        if knot2 is None:
            knot2 = (degree_to_time(102), (
                nan,
                nan,
                nan,
                nan,
                nan,
            ))
        if knot3 is None:
            knot3 = (degree_to_time(111), (
                nan,
                nan,
                nan,
                nan,
                nan,
            ))
        if knot4 is None:
            knot4 = (degree_to_time(120), (
                nan,
                nan,
                nan,
                nan,
                nan,
            ))
        if knot5 is None:
            knot5 = (degree_to_time(127.2), (
                nan,
                nan,
                nan,
                nan,
                nan,
            ))
        if end is None:
            end = (degree_to_time(138), (
                nan,
                nan,
                nan,
                nan,
                nan,
            ))
        took_knot_at = [touch, knot2, knot3, knot4, knot5, end]
        knots = [took_knot_at[i][0] for i in range(len(took_knot_at))]
        pvajp = [[took_knot_at[i][1][j] for i in range(len(took_knot_at))]
                 for j in range(5)]
        orders = [6] * len(took_knot_at)
        SplineWithPiecewisePolynomial.__init__(self, knots, orders, pvajp,
                                               name=name)
        self.shake = ShakeHand(if_rebuild_pieces=False)
        self.joy = JawOnYorkCurve()
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
        self.build_pieces()
        r_O5O2 = (self.package.height +
                  self.package.hs_sealing_length +
                  self.trace.joy_mechanism_forward.r_DC_value)
        expr_y_R_AO2_touching = self.trace.get_y_R_AO2_when_touching_expr()
        expr_y_R_AO2_closing = self.trace.get_y_R_AO2_when_closing_expr()
        expr_y_R_AO2 = [expr_y_R_AO2_touching, expr_y_R_AO2_closing]
        expr_y_R_AO5_touching = self.trace.get_y_R_AO5_when_touching_expr()
        expr_y_R_AO5_closing = self.trace.get_y_R_AO5_when_closing_expr()
        expr_y_R_AO5 = [expr_y_R_AO5_touching, expr_y_R_AO5_closing]
        add_to_x = degree_to_time(180)
        for i in range(self.num_of_pieces):
            left_york_piece_i_plus = self.shake.get_pieces()[i + 1]
            left_york_now_position = \
                left_york_piece_i_plus.get_expr()[0].subs(x, x + add_to_x)
            new_expr = (expr_y_R_AO5[i // 3]
                        + r_O5O2
                        - expr_y_R_AO2[i // 3]
                        + left_york_now_position)
            self.update_piece_with_new_expr(i, new_expr)
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
    def __init__(self, name='climb_up_curve_0_92',
                 start=None,
                 cross=None,
                 high=None,
                 touch=None,
                 ):
        """
        c3 = Climb()
        """
        if start is None:
            start = (degree_to_time(0),
                     (0,
                      0,
                      nan,
                      nan,
                      nan))
        if cross is None:
            cross = (degree_to_time(43),
                     (200,
                      nan,
                      0,
                      nan,
                      nan))
        if high is None:
            high = (degree_to_time(84),
                    (372.2,
                     0,
                     nan,
                     nan,
                     nan))
        if touch is None:
            self.trace = TraceOfA(load_memo=True)
            touching_time = self.trace.get_touch_time()
            touch = (touching_time,
                     (320 + 147.490658039069,
                      -154.513293430448,
                      -3659.71088510222,
                      470384.967511957,
                      nan))
        took_knot_at = [start, cross, high, touch]
        knots = [took_knot_at[i][0] for i in range(len(took_knot_at))]
        pvajp = [[took_knot_at[i][1][j] for i in range(len(took_knot_at))]
                 for j in range(5)]
        orders = [6] * len(took_knot_at)
        SplineWithPiecewisePolynomial.__init__(self, knots, orders, pvajp,
                                               name=name)

    def build_smoothness_condition(self, depths=None):
        """
        c3 = Climb()
        c3.update_with_solution()
        c3.plot_svaj()
        """
        if self.count_of_smoothness != 0:
            return self.count_of_smoothness
        if depths is None:
            depths = {
                1: 4,
                2: 4,
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
    def __init__(self, start=None, release=None, end=None, name='throw_325_0'):
        """
        t3 = Throw()
        """
        if start is None:
            start = (degree_to_time(325),
                     (50,
                      -422,
                      0,
                      nan,
                      nan))
        if release is None:
            release = (degree_to_time(330),
                       (30,
                        nan,
                        nan,
                        nan,
                        nan))
        if end is None:
            end = (degree_to_time(360),
                   (0,
                    0,
                    30000,
                    nan,
                    nan))
        took_knot_at = [start, release, end]
        knots = [took_knot_at[i][0] for i in range(len(took_knot_at))]
        pvajp = [[took_knot_at[i][1][j] for i in range(len(took_knot_at))]
                 for j in range(5)]
        orders = [6] * len(took_knot_at)
        SplineWithPiecewisePolynomial.__init__(self, knots, orders, pvajp,
                                               name=name)

    def build_smoothness_condition(self, depths=None):
        """
        t3 = Throw()
        t3.update_with_solution()
        t3.plot_svaj()
        """
        if self.count_of_smoothness != 0:
            return self.count_of_smoothness
        if depths is None:
            depths = {
                1: 5,
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


class Combine(SplineWithPiecewisePolynomial):
    def __init__(self):
        self.joy = JawOnYorkCurve()
        self.trace = TraceOfA(load_memo=True)
        touching_time = self.trace.get_touch_time()
        self.climb = Climb(name="climb_to_touch",
                           start=(degree_to_time(0), (
                               0,
                               0,
                               nan,
                               nan,
                               nan,
                           )),
                           cross=(degree_to_time(43), (
                               symbols("climb_cross_p"),
                               nan,
                               nan,
                               nan,
                               nan,
                           )),
                           high=(degree_to_time(84), (
                               symbols("climb_high_p"),
                               0,
                               nan,
                               nan,
                               nan,
                           )),
                           touch=(touching_time, (
                               symbols("climb_touch_p"),
                               symbols("climb_touch_v"),
                               symbols("climb_touch_a"),
                               symbols("climb_touch_j"),
                               nan,
                           )),
                           )
        self.touch = Touch(name="touch_to_fold")
        self.pull1 = Pull(name="pull_1")
        self.shake1 = ShakeHand(name="shake_for_pulling_ear")
        self.pull2 = Pull(name="pull_2")
        self.shake2 = ShakeHand(name="shake_for_touching")
        self.pull3 = Pull(name="pull_3")
        self.throw = Throw(name="throw_to_bottom")

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
                 whether_rebuild=False):
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
        key_knots = [
            start, knot1, widest, knot4, knot2, closed, release, knot3, end
        ]
        smooth_depth = {
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
        if whether_rebuild:
            self.update_with_solution()
            self.save_solved_pieces()
        else:
            self.load_solved_pieces()

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
        t1 = TraceOfA(whether_load_memo=False)
        """
        # Jaw on York spline Curve
        self.joy_curve = JawOnYorkCurve(whether_rebuild=False)
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

    # xy of R_AO2 position expression
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

    # y of R_AO5 position expressionn
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
        return self.memo['y_R_AO5_when_closing_expr']

    #
    def get_x_V_AO5_when_touching_expr(self):
        """
        t1 = TraceOfA()
        print(t1.get_x_V_AO5_when_touching_expr().subs(x, t1.get_touch_time()))
            # 605.377269017069
        print(t1.get_x_V_AO5_when_touching_expr().subs(x, degree_to_time(120)))
            # 154.168911849550
        """
        if 'x_V_AO5_when_touching' in self.memo:
            return self.memo['x_V_AO5_when_touching']
        x_V_AO5_when_touching = diff(self.get_x_R_AO2_when_touching_expr(), x)
        self.memo['x_V_AO5_when_touching'] = x_V_AO5_when_touching
        return self.memo['x_V_AO5_when_touching']

    def get_x_V_AO5_when_closing_expr(self):
        if 'x_V_AO5_when_closing' in self.memo:
            return self.memo['x_V_AO5_when_closing']
        x_V_AO5_when_closing = diff(self.get_x_R_AO2_when_closing_expr(), x)
        self.memo['x_V_AO5_when_closing'] = x_V_AO5_when_closing
        return self.memo['x_V_AO5_when_closing']

    #
    def get_x_V_AO2_when_touching_expr(self):
        """
        t1 = TraceOfA()
        print(t1.get_x_V_AO2_when_touching_expr().subs(x, t1.get_touch_time()))
            # 605.377269017069
        print(t1.get_x_V_AO2_when_touching_expr().subs(x, degree_to_time(120)))
            # 154.168911849550
        """
        if 'x_V_AO2_when_touching' in self.memo:
            return self.memo['x_V_AO2_when_touching']
        x_V_AO2_of_vr_O4O2 = self.joy_mechanism_forward.get_x_V_AO2_of_vr_O4O2()
        x_V_AO2_when_touching = x_V_AO2_of_vr_O4O2.subs([
            (self.joy_mechanism_forward.r,
             (-self.joy_curve.get_kth_expr_of_ith_piece(0, 3)
              + self.get_close_rO4O2())),
            (self.joy_mechanism_forward.v,
             -self.joy_curve.get_kth_expr_of_ith_piece(1, 3))])
        self.memo['x_V_AO2_when_touching'] = x_V_AO2_when_touching
        return self.memo['x_V_AO2_when_touching']

    def get_x_V_AO2_when_closing_expr(self):
        """
        t1 = TraceOfA()
        print(t1.get_x_V_AO2_when_closing_expr().subs(x, degree_to_time(138)))
        # 4.36802480797050e-13
        print(t1.get_x_V_AO2_when_closing_expr().subs(x, degree_to_time(120)))
        # 154.168911849551
        """
        if 'x_V_AO2_when_closing' in self.memo:
            return self.memo['x_V_AO2_when_closing']
        x_V_AO2_of_vr_O4O2 = self.joy_mechanism_forward.get_x_V_AO2_of_vr_O4O2()
        x_V_AO2_when_closing = x_V_AO2_of_vr_O4O2.subs([
            (self.joy_mechanism_forward.r,
             (-self.joy_curve.get_kth_expr_of_ith_piece(0, 4)
              + self.get_close_rO4O2())),
            (self.joy_mechanism_forward.v,
             -self.joy_curve.get_kth_expr_of_ith_piece(1, 4))])
        self.memo['x_V_AO2_when_closing'] = x_V_AO2_when_closing
        return self.memo['x_V_AO2_when_closing']

    #
    def get_y_V_AO2_when_touching_expr(self):
        """
        t1 = TraceOfA()
        print(t1.get_y_V_AO2_when_touching_expr().subs(x, t1.get_touch_time()))
        # -126.300771294982
        print(t1.get_y_V_AO2_when_touching_expr().subs(x, degree_to_time(120)))
        # -54.1663345694120
        print(t1.get_y_V_AO2_when_touching_expr().subs(x, degree_to_time(84)))
        # -54.8571400797708
        """
        if 'y_V_AO2_when_touching' in self.memo:
            return self.memo['y_V_AO2_when_touching']
        y_V_AO2_of_vr_O4O2 = self.joy_mechanism_forward.get_y_V_AO2_of_vr_O4O2()
        y_V_AO2_when_touching = y_V_AO2_of_vr_O4O2.subs([
            (self.joy_mechanism_forward.r,
             (-self.joy_curve.get_kth_expr_of_ith_piece(0, 3)
              + self.get_close_rO4O2())),
            (self.joy_mechanism_forward.v,
             -self.joy_curve.get_kth_expr_of_ith_piece(1, 3))])
        self.memo['y_V_AO2_when_touching'] = y_V_AO2_when_touching
        return self.memo['y_V_AO2_when_touching']

    def get_y_V_AO2_when_closing_expr(self):
        """
        t1 = TraceOfA()
        print(t1.get_y_V_AO2_when_closing_expr().subs(x, degree_to_time(138)))
        # -1.59378185647184e-13
        print(t1.get_y_V_AO2_when_closing_expr().subs(x, degree_to_time(120)))
        -54.1663345694121
        """
        if 'y_V_AO2_when_closing' in self.memo:
            return self.memo['y_V_AO2_when_closing']
        y_V_AO2_of_vr_O4O2 = self.joy_mechanism_forward.get_y_V_AO2_of_vr_O4O2()
        y_V_AO2_when_closing = y_V_AO2_of_vr_O4O2.subs([
            (self.joy_mechanism_forward.r,
             (-self.joy_curve.get_kth_expr_of_ith_piece(0, 4)
              + self.get_close_rO4O2())),
            (self.joy_mechanism_forward.v,
             -self.joy_curve.get_kth_expr_of_ith_piece(1, 4))])
        self.memo['y_V_AO2_when_closing'] = y_V_AO2_when_closing
        return self.memo['y_V_AO2_when_closing']

    #
    def get_y_V_AO5_when_touching_expr(self):
        """
        t1 = TraceOfA()
        print(t1.get_y_V_AO5_when_touching_expr().subs(x, t1.get_touch_time()))
        # 4.39902319100218e-11
        print(t1.get_y_V_AO5_when_touching_expr().subs(x, degree_to_time(120)))
        # -358.114618459770
        """
        if 'y_V_AO5_when_touching' in self.memo:
            return self.memo['y_V_AO5_when_touching']
        y_V_AO5_when_touching = diff(self.get_y_R_AO5_when_touching_expr(), x)
        self.memo['y_V_AO5_when_touching'] = y_V_AO5_when_touching
        return self.memo['y_V_AO5_when_touching']

    def get_y_V_AO5_when_closing_expr(self):
        """
        t1 = TraceOfA()
        print(t1.get_y_V_AO5_when_closing_expr().subs(x, degree_to_time(138)))
        # -6.31220383387539e-6
        print(t1.get_y_V_AO5_when_closing_expr().subs(x, degree_to_time(120)))
        # -358.114618459771
        """
        if 'y_V_AO5_when_closing' in self.memo:
            return self.memo['y_V_AO5_when_closing']
        y_V_AO5_when_closing = diff(self.get_y_R_AO5_when_closing_expr(), x)
        self.memo['y_V_AO5_when_closing'] = y_V_AO5_when_closing
        return self.memo['y_V_AO5_when_closing']

    #
    def get_x_A_AO5_when_touching_expr(self):
        """
        t1 = TraceOfA()
        print(t1.get_x_A_AO5_when_touching_expr().subs(x, t1.get_touch_time()))
        # -4841.07447381837
        print(t1.get_x_A_AO5_when_touching_expr().subs(x, degree_to_time(120)))
        # -7942.86569052343
        """
        if 'x_A_AO5_when_touching' in self.memo:
            return self.memo['x_A_AO5_when_touching']
        x_A_AO5_when_touching = diff(self.get_x_V_AO5_when_touching_expr(), x)
        self.memo['x_A_AO5_when_touching'] = x_A_AO5_when_touching
        return self.memo['x_A_AO5_when_touching']

    def get_y_A_AO5_when_touching_expr(self):
        """
        t1 = TraceOfA()
        print(t1.get_y_A_AO5_when_touching_expr().subs(x, t1.get_touch_time()))
        # -15112.6448594876
        print(t1.get_y_A_AO5_when_touching_expr().subs(x, degree_to_time(120)))
        # 2597.04185357227
        """
        if 'y_A_AO5_when_touching' in self.memo:
            return self.memo['y_A_AO5_when_touching']
        y_A_AO5_when_touching = diff(self.get_y_V_AO5_when_touching_expr(), x)
        self.memo['y_A_AO5_when_touching'] = y_A_AO5_when_touching
        return self.memo['y_A_AO5_when_touching']

    def get_x_A_AO5_when_closing_expr(self):
        """
        t1 = TraceOfA()
        print(t1.get_x_A_AO5_when_closing_expr().subs(x, degree_to_time(138)))
        # -4.31184330462087e-12
        print(t1.get_x_A_AO5_when_closing_expr().subs(x, degree_to_time(120)))
        # -7942.86569052342
        """
        if 'x_A_AO5_when_closing' in self.memo:
            return self.memo['x_A_AO5_when_closing']
        x_A_AO5_when_closing = diff(self.get_x_V_AO5_when_closing_expr(), x)
        self.memo['x_A_AO5_when_closing'] = x_A_AO5_when_closing
        return self.memo['x_A_AO5_when_closing']

    def get_y_A_AO5_when_closing_expr(self):
        """
        t1 = TraceOfA()
        print(t1.get_y_A_AO5_when_closing_expr().subs(x, degree_to_time(138)))
        # 3.34129578550133e-5
        print(t1.get_y_A_AO5_when_closing_expr().subs(x, degree_to_time(120)))
        # 2597.04185357219
        print(t1.get_y_A_AO5_when_closing_expr().subs(x, degree_to_time(137)))
        # 11719.2517761919
        """
        if 'y_A_AO5_when_closing' in self.memo:
            return self.memo['y_A_AO5_when_closing']
        y_A_AO5_when_closing = diff(self.get_y_V_AO5_when_closing_expr(), x)
        self.memo['y_A_AO5_when_closing'] = y_A_AO5_when_closing
        return self.memo['y_A_AO5_when_closing']

    def get_y_A_AO2_when_touching_expr(self):
        """
        t1 = TraceOfA()
        print(t1.get_y_A_AO2_when_touching_expr().subs(x, t1.get_touch_time()))
        # -1221.82260807299
        print(t1.get_y_A_AO2_when_touching_expr().subs(x, degree_to_time(120)))
        # 2628.99301159539
        """
        if 'y_A_AO2_when_touching' in self.memo:
            return self.memo['y_A_AO2_when_touching']
        y_A_AO2_when_touching = diff(self.get_y_V_AO2_when_touching_expr(), x)
        self.memo['y_A_AO2_when_touching'] = y_A_AO2_when_touching
        return self.memo['y_A_AO2_when_touching']

    def get_y_A_AO2_when_closing_expr(self):
        """
        t1 = TraceOfA()
        print(t1.get_y_A_AO2_when_closing_expr().subs(x, degree_to_time(138)))
        # 1.57328264581155e-12
        print(t1.get_y_A_AO2_when_closing_expr().subs(x, degree_to_time(120)))
        # 2628.99301159538
        print(t1.get_y_A_AO2_when_closing_expr().subs(x, degree_to_time(137)))
        # 19.9800822443496
        """
        if 'y_A_AO2_when_closing' in self.memo:
            return self.memo['y_A_AO2_when_closing']
        y_A_AO2_when_closing = diff(self.get_y_V_AO2_when_closing_expr(), x)
        self.memo['y_A_AO2_when_closing'] = y_A_AO2_when_closing
        return self.memo['y_A_AO2_when_closing']

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
        # Plot A to O2 curve on touching and closing stage
        # xy of A velocity
        plot_xy_V_AO2 = plot(0, (x, knots[0], knots[-1]),
                             title="xy of A to O2 velocity",
                             ylabel="(mm/s)",
                             show=False)
        x_V_AO2_expr = [self.get_x_V_AO2_when_touching_expr(),
                        self.get_x_V_AO2_when_closing_expr()]
        y_V_AO2_expr = [self.get_y_V_AO2_when_touching_expr(),
                        self.get_y_V_AO2_when_closing_expr()]
        for i in range(2):
            plot_x_V_AO2_i = plot(x_V_AO2_expr[i],
                                  (x, knots[i], knots[i + 1]),
                                  show=False)
            plot_y_V_AO2_i = plot(y_V_AO2_expr[i],
                                  (x, knots[i], knots[i + 1]),
                                  show=False)
            plot_xy_V_AO2.extend(plot_x_V_AO2_i)
            plot_xy_V_AO2.extend(plot_y_V_AO2_i)
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

        fig, (ax1, ax2, ax3, ax4, ax5, ax6) = plt.subplots(nrows=6)
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
        move_sympyplot_to_axes(plot_xy_V_AO2, ax5)
        ax5.set_xticks([knots[i] for i in range(len(knots))])
        ax5.set_xticklabels([(i % 2) * '\n' +
                             str(time_to_degree(knots[i]))
                             for i in range(len(knots))])
        ax5.grid(True)
        move_sympyplot_to_axes(plot_xy_A_AO5, ax6)
        ax6.set_xticks([knots[i] for i in range(len(knots))])
        ax6.set_xticklabels([(i % 2) * '\n' +
                             str(time_to_degree(knots[i]))
                             for i in range(len(knots))])
        ax6.grid(True)
        ax6.set_xlabel('machine degree')
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
    def __init__(self,
                 name='shake_hand_curve_264_318',
                 start=None,
                 knot1=None,
                 knot2=None,
                 knot3=None,
                 knot4=None,
                 knot5=None,
                 end=None,
                 whether_rebuild=False):
        """
        s1 = ShakeHand(name='shake_hand_curve_264_318', whether_rebuild=True)
        s1 = ShakeHand(name='shake_hand_curve_264_318', whether_rebuild=False)
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
                degree_to_time(318 - 264) * (-422) + 24.25 * 1.3,
                -422,
                0,
                nan,
                nan,
            ))
        key_knots = [start, knot1, knot2, knot3, knot4, knot5, end]
        smooth_depth = {
            knot1: 5,
            knot2: 5,
            knot3: 5,
            knot4: 4,
            knot5: 5,
        }
        SplineWithPiecewisePolynomial.__init__(self,
                                               key_knots=key_knots,
                                               smooth_depth=smooth_depth,
                                               name=name)
        if whether_rebuild:
            self.update_with_solution()
            self.save_solved_pieces()
        else:
            self.load_solved_pieces()

    # def build_smoothness_condition(self, depths=None):
    #     """
    #     s1 = ShakeHand(whether_rebuild=False)
    #     print(len(s1.build_smoothness_condition()))
    #     print(len(s1.build_interpolating_condition()))
    #     for i in range(len(s1.equations)):
    #         print(s1.equations[i])
    #     """
    #     if self.count_of_smoothness != 0:
    #         return self.count_of_smoothness
    #     if depths is None:
    #         depths = {
    #             1: 5,
    #             2: 5,
    #             3: 5,
    #             4: 4,
    #             5: 5
    #         }
    #     for i in range(1, len(self.took_knot_at) - 1):
    #         kpi = self.took_knot_at[i]  # Knot Point I
    #         ki = kpi[0]
    #         pib = self.get_pieces()[i - 1]  # Piece Before knot I
    #         pia = self.get_pieces()[i]  # Piece After knot I
    #         eib = pib.get_expr()
    #         eia = pia.get_expr()
    #         for d in range(depths[kpi]):
    #             eq = Eq(eib[d].subs(x, ki), eia[d].subs(x, ki))
    #             self.equations.append(eq)
    #             self.count_of_smoothness += 1
    #     return self.equations[-self.count_of_smoothness:]

    def build_spline(self):
        """
        s1 = ShakeHand(whether_rebuild=True)
        s1 = ShakeHand(whether_rebuild=False)
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
                 shake=None, joy=None, package=None,
                 whether_rebuild=False):
        """
        t1 = Touch(whether_rebuild=True)
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
        smooth_depth = {
            knot2: 5,
            knot3: 5,
            knot4: 4,
            knot5: 5,
        }
        key_knots = [touch, knot2, knot3, knot4, knot5, end]
        SplineWithPiecewisePolynomial.__init__(self,
                                               key_knots=key_knots,
                                               smooth_depth=smooth_depth,
                                               name=name)
        if shake is None:
            self.shake = ShakeHand(whether_rebuild=False)
        else:
            self.shake = shake
        if joy is None:
            self.joy = JawOnYorkCurve(whether_rebuild=False)
        else:
            self.joy = joy
        if package is None:
            self.package = Package(330, "Square", 49.5, 48.5, 124.6, 6, 190)
        else:
            self.package = package
        if whether_rebuild:
            self.modify_pieces_expr()
            self.save_solved_pieces()
        else:
            self.load_solved_pieces()

    def modify_pieces_expr(self):
        """
        t2 = Touch(whether_rebuild=False)
        t2 = Touch(whether_rebuild=True)
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
        """
        t2 = Touch(whether_rebuild_pieces=False)
        t2.narrow_start_and_end()
        """
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
    def __init__(self,
                 name='constant_velocity_pull_1',
                 start=None,
                 end=None,
                 whether_rebuild=False):
        """
        s2 = Pull(whether_rebuild=True)
        s2.plot_svaj()
        """
        self.package = Package(330, "Square", 49.5, 48.5, 124.6, 6, 190)
        self.cons_v = self.package.get_pulling_velocity()
        if start is None:
            start = (degree_to_time(0), (
                0,
                self.cons_v,
                nan,
                nan,
                nan,
            ))
        if end is None:
            end = (degree_to_time(180), (
                nan,
                nan,
                nan,
                nan,
                nan,
            ))
        key_knots = [start, end]
        smooth_depth = {
        }
        orders = [2] * (len(key_knots))
        SplineWithPiecewisePolynomial.__init__(self,
                                               key_knots=key_knots,
                                               orders=orders,
                                               smooth_depth=smooth_depth,
                                               name=name)
        if whether_rebuild:
            self.update_with_solution()
            self.save_solved_pieces()
        else:
            self.load_solved_pieces()

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
    def __init__(self, name='climb_up_0_touching',
                 start=None,
                 cross=None,
                 high=None,
                 touch=None,
                 whether_rebuild=False):
        """
        c3 = Climb(whether_rebuild=False)
        c3 = Climb(whether_rebuild=True)
        c3.update_with_solution()
        c3.plot_svaj()
        """
        self.trace = TraceOfA(whether_load_memo=True)
        self.package = Package(330, "Square", 49.5, 48.5, 124.6, 6, 190)
        if start is None:
            start = (degree_to_time(0), (
                0,
                0,
                38000,
                567486.791390715,
                nan,
            ))
        knot1 = (degree_to_time(13), (
            nan,
            nan,
            nan,
            0,
            nan,
        ))
        if cross is None:
            cross = (degree_to_time(43), (
                200,
                nan,
                nan,
                nan,
                nan,
            ))
        knot2 = (degree_to_time(69), (
            nan,
            nan,
            nan,
            0,
            nan,
        ))
        if high is None:
            high = (degree_to_time(84), (
                372.2,
                0,
                nan,
                nan,
                nan,
            ))
        if touch is None:
            touching_time = self.trace.get_touch_time()
            touch = (touching_time, (
                nan,
                -40.6661440887556,
                -4088.93068846931,
                93189.8259805306,
                nan,
            ))
        # key_knots = [start, knot1, cross, knot2, high, touch]
        key_knots = [start, cross, high, touch]
        smooth_depth = {
            knot1: 5,
            cross: 4,
            knot2: 5,
            high: 4,
        }
        SplineWithPiecewisePolynomial.__init__(self,
                                               key_knots=key_knots,
                                               smooth_depth=smooth_depth,
                                               name=name)
        if whether_rebuild:
            self.update_with_solution()
            self.save_solved_pieces()
        else:
            self.load_solved_pieces()


class Throw(SplineWithPiecewisePolynomial):
    def __init__(self,
                 start=None,
                 release=None,
                 end=None,
                 name='throw_325_0',
                 whether_rebuild=False
                 ):
        """
        t3 = Throw(whether_rebuild=True)
        t3.plot_svaj()
        """
        if start is None:
            start = (degree_to_time(325), (
                50,
                -422,
                0,
                nan,
                nan,
            ))
        if release is None:
            release = (degree_to_time(330), (
                44.5,
                nan,
                nan,
                nan,
                nan,
            ))
        knot1 = (degree_to_time(335), (
            nan,
            nan,
            nan,
            0,
            nan,
        ))
        if end is None:
            end = (degree_to_time(360), (
                0,
                0,
                38000,
                nan,
                nan,
            ))
        key_knots = [start, release, knot1, end]
        smooth_depth = {
            release: 5,
            knot1: 5,
        }
        SplineWithPiecewisePolynomial.__init__(self,
                                               key_knots=key_knots,
                                               smooth_depth=smooth_depth,
                                               name=name)
        if whether_rebuild:
            self.update_with_solution()
            self.save_solved_pieces()
        else:
            self.load_solved_pieces()


class Combine(SplineWithPiecewisePolynomial):
    def __init__(self):
        self.package = Package(330, "Square", 49.5, 48.5, 124.6, 6, 190)
        self.cons_v = self.package.get_pulling_velocity()
        self.joy = JawOnYorkCurve(whether_rebuild=False)
        self.trace = TraceOfA(whether_load_memo=True)
        self.touching_time = self.trace.get_touch_time()
        self.climb = []
        self.touch = []
        self.pull1 = []
        self.shake1 = []
        self.pull2 = []
        self.shake2 = []
        self.pull3 = []
        self.throw = []
        self.key_knots = []

    def build_shake2(self, whether_rebuild=False):
        """
        com = Combine()
        com.build_shake2(whether_rebuild=False)
        com.build_shake2(whether_rebuild=True)
        com.build_shake2().plot_svaj()
        """
        try:
            return self.shake2[0]
        except IndexError:
            self.shake2.append(
                ShakeHand(name="shake2_for_accepting",
                          start=(degree_to_time(264), (
                              # symbols('shake2_start_p'),
                              0,
                              self.cons_v,
                              0,
                              nan,
                              nan,
                          )),
                          knot1=(degree_to_time(274.8), (
                              nan,
                              nan,
                              nan,
                              0,
                              nan,
                          )),
                          knot2=(degree_to_time(282), (
                              nan,
                              nan,
                              nan,
                              nan,
                              0,
                          )),
                          knot3=(degree_to_time(291), (
                              nan,
                              nan,
                              0,
                              nan,
                              0,
                          )),
                          knot4=(degree_to_time(300), (
                              nan,
                              nan,
                              nan,
                              nan,
                              0,
                          )),
                          knot5=(degree_to_time(307.2), (
                              nan,
                              nan,
                              nan,
                              0,
                              nan,
                          )),
                          end=(degree_to_time(318), (
                              (degree_to_time(318 - 264) * self.cons_v
                               + self.package.depth / 2 * 1.3),
                               # (symbols('shake2_start_p')
                               # + degree_to_time(318 - 264) * self.cons_v
                               # + self.package.depth / 2 * 1.3),
                              self.cons_v,
                              0,
                              nan,
                              nan,
                          )),
                          whether_rebuild=whether_rebuild,
                          )
            )
            return self.shake2[0]

    def build_touch(self, whether_rebuild=False):
        """
        com = Combine()
        com.build_touch(whether_rebuild=False)
        com.build_touch(whether_rebuild=True)
        com.build_touch().plot_svaj()
        """
        try:
            return self.touch[0]
        except IndexError:
            self.touch.append(
                Touch(name="touch_to_fold",
                      touch=(self.trace.get_touch_time(), (
                          nan,
                          nan,
                          nan,
                          nan,
                          nan,
                      )),
                      knot2=(degree_to_time(102), (
                          nan,
                          nan,
                          nan,
                          nan,
                          nan,
                      )),
                      knot3=(degree_to_time(111), (
                          nan,
                          nan,
                          nan,
                          nan,
                          nan,
                      )),
                      knot4=(degree_to_time(120), (
                          nan,
                          nan,
                          nan,
                          nan,
                          nan,
                      )),
                      knot5=(degree_to_time(127.2), (
                          nan,
                          nan,
                          nan,
                          nan,
                          nan,
                      )),
                      end=(degree_to_time(138), (
                          nan,
                          nan,
                          nan,
                          nan,
                          nan,
                      )),
                      package=self.package,
                      shake=self.build_shake2(whether_rebuild=False),
                      joy=self.joy,
                      whether_rebuild=whether_rebuild,
                      )
            )
            return self.touch[0]

    def build_climb(self, whether_rebuild=False):
        """
        com = Combine()
        com.build_climb(whether_rebuild=False)
        com.build_climb(whether_rebuild=True)
        com.build_climb().plot_svaj()
        """
        try:
            return self.climb[0]
        except IndexError:
            self.climb.append(
                Climb(name="climb_to_touch",
                      start=(degree_to_time(0), (
                          0,
                          0,
                          # symbols('climb_start_a'),
                          # symbols('climb_start_j'),
                          # self.build_throw()[1][2],
                          # self.build_throw()[1][3],
                          38000,
                          567486.791390715,
                          nan,
                      )),
                      cross=(degree_to_time(43), (
                          200,
                          nan,
                          nan,
                          nan,
                          nan,
                      )),
                      high=(degree_to_time(84), (
                          372.2,
                          0,
                          nan,
                          nan,
                          nan,
                      )),
                      touch=(self.touching_time, (
                          nan,
                          # symbols('climb_touch_v'),
                          # symbols('climb_touch_a'),
                          # symbols('climb_touch_j'),
                          # self.build_touch()[0][1],
                          # self.build_touch()[0][2],
                          # self.build_touch()[0][3],
                          -40.6661440887556,
                          -4088.93068846931,
                          93189.8259805306,
                          nan,
                      )),
                      whether_rebuild=whether_rebuild,
                      )
            )
            return self.climb[0]

    def build_pull1(self, whether_rebuild=False):
        """
        com = Combine()
        com.build_pull1(whether_rebuild=False)
        com.build_pull1(whether_rebuild=True)
        com.build_pull1().plot_svaj()
        """
        try:
            return self.pull1[0]
        except IndexError:
            self.pull1.append(
                Pull(name="pull_1",
                     start=(degree_to_time(138), (
                         # symbols('pull1_start_p'),
                         0,
                         self.cons_v,
                         nan,
                         nan,
                         nan,
                     )),
                     end=(degree_to_time(145), (
                         nan,
                         nan,
                         nan,
                         nan,
                         nan,
                     )),
                     whether_rebuild=whether_rebuild,
                     )
            )
            return self.pull1[0]

    def build_shake1(self, whether_rebuild=False):
        """
        com = Combine()
        com.build_shake1(whether_rebuild=False)
        com.build_shake1(whether_rebuild=True)
        com.build_shake1().plot_svaj()
        """
        try:
            return self.shake1[0]
        except IndexError:
            self.shake1.append(
                ShakeHand(
                    name="shake1_for_ear",
                    start=(degree_to_time(145), (
                        0,
                        -422,
                        0,
                        nan,
                        nan,
                    )),
                    knot1=(degree_to_time(155), (
                        nan,
                        nan,
                        nan,
                        0,
                        nan,
                    )),
                    knot2=(degree_to_time(162), (
                        nan,
                        nan,
                        nan,
                        nan,
                        0,
                    )),
                    knot3=(degree_to_time(170), (
                        nan,
                        nan,
                        0,
                        nan,
                        0,
                    )),
                    knot4=(degree_to_time(178), (
                        nan,
                        nan,
                        nan,
                        nan,
                        0,
                    )),
                    knot5=(degree_to_time(185), (
                        nan,
                        nan,
                        nan,
                        0,
                        nan,
                    )),
                    end=(degree_to_time(195), (
                        (degree_to_time(318 - 264) * self.cons_v
                         + self.package.depth / 2 * 1.0),
                        -422,
                        0,
                        nan,
                        nan,
                    )),
                    whether_rebuild=whether_rebuild,
                )
            )
            return self.shake1[0]

    def build_pull2(self, whether_rebuild=False):
        """
        com = Combine()
        com.build_pull2(whether_rebuild=False)
        com.build_pull2(whether_rebuild=True)
        com.build_pull2().plot_svaj()
        """
        try:
            return self.pull2[0]
        except IndexError:
            self.pull2.append(
                Pull(name="pull_2",
                     start=(degree_to_time(195), (
                         # symbols('pull2_start_p'),
                         0,
                         self.cons_v,
                         nan,
                         nan,
                         nan,
                     )),
                     end=(degree_to_time(264), (
                         nan,
                         nan,
                         nan,
                         nan,
                         nan,
                     )),
                     whether_rebuild=whether_rebuild,
                     )
            )
            return self.pull2[0]

    def build_pull3(self, whether_rebuild=False):
        """
        com = Combine()
        com.build_pull3(whether_rebuild=False)
        com.build_pull3(whether_rebuild=True)
        com.build_pull3().plot_svaj()
        """
        try:
            return self.pull3[0]
        except IndexError:
            self.pull3.append(
                Pull(
                    name="pull_3",
                    start=(degree_to_time(318), (
                        # symbols('pull3_start_p'),
                        0,
                        self.cons_v,
                        nan,
                        nan,
                        nan,
                    )),
                    end=(degree_to_time(325), (
                        nan,
                        nan,
                        nan,
                        nan,
                        nan,
                    )),
                    whether_rebuild=whether_rebuild,
                )
            )
            return self.pull3[0]

    def build_throw(self, whether_rebuild=False):
        """
        com = Combine()
        com.build_throw(whether_rebuild=False)
        com.build_throw(whether_rebuild=True)
        com.build_throw().plot_svaj()
        """
        try:
            return self.throw[0]
        except IndexError:
            self.throw.append(
                Throw(
                    name="throw_to_bottom",
                    start=(degree_to_time(325), (
                        50,
                        -422,
                        0,
                        nan,
                        nan,
                    )),
                    release=(degree_to_time(330), (
                        44.5,
                        nan,
                        nan,
                        nan,
                        nan,
                    )),
                    end=(degree_to_time(360), (
                        0,
                        0,
                        38000,
                        nan,
                        nan,
                    )),
                    whether_rebuild=whether_rebuild,
                )
            )
            return self.throw[0]

    def collect_key_knots(self):
        """
        com = Combine()
        key_knots = com.collect_key_knots()
        for i in range(len(key_knots)):
            print(time_to_degree(key_knots[i][0]))
        print(len(com.collect_key_knots()))
        """
        if len(self.key_knots) != 0:
            return self.key_knots
        self.key_knots.extend(
            self.build_climb().key_knots
        )
        self.key_knots.extend(
            self.build_touch().key_knots[1:]
        )
        self.key_knots.extend(
            self.build_pull1().key_knots[1:]
        )
        self.key_knots.extend(
            self.build_shake1().key_knots[1:]
        )
        self.key_knots.extend(
            self.build_pull2().key_knots[1:]
        )
        self.key_knots.extend(
            self.build_shake2().key_knots[1:]
        )
        self.key_knots.extend(
            self.build_pull3().key_knots[1:]
        )
        self.key_knots.extend(
            self.build_throw().key_knots[1:]
        )
        return self.key_knots

    def construct_spline_of_empty_pieces(self):
        """
        com = Combine()
        num_of_pieces = com.construct_spline_of_empty_pieces()
        print('num_of_pieces: ', num_of_pieces)
        """
        try:
            return self.num_of_pieces
        except AttributeError:
            name = "combined_curve"
            key_knots = self.collect_key_knots()
            SplineWithPiecewisePolynomial.__init__(self,
                                                   key_knots=key_knots,
                                                   name=name)
            return self.num_of_pieces

    def collect_stage_pieces(self):
        """
        com = Combine()
        actual_pieces = com.collect_stage_pieces()
        print('actual num of pieces: ', len(actual_pieces))
        print('First one of these pieces: ', actual_pieces[0])
        print('Last one of these pieces: ', actual_pieces[-1])
        """
        try:
            return self.pieces
        except AttributeError:
            self.construct_spline_of_empty_pieces()
        self.pieces.extend(
            self.build_climb().get_pieces()
        )
        self.pieces.extend(
            self.build_touch().get_pieces()
        )
        self.pieces.extend(
            self.build_pull1().get_pieces()
        )
        self.pieces.extend(
            self.build_shake1().get_pieces()
        )
        self.pieces.extend(
            self.build_pull2().get_pieces()
        )
        self.pieces.extend(
            self.build_shake2().get_pieces()
        )
        self.pieces.extend(
            self.build_pull3().get_pieces()
        )
        self.pieces.extend(
            self.build_throw().get_pieces()
        )
        return self.pieces

    def plot_pvaj(self):
        """
        com = Combine()
        actual_pieces = com.collect_stage_pieces()
        print('actual num of pieces: ', len(actual_pieces))
        com.plot_pvaj()
        """
        fig = self.plot_svaj()
        fig.savefig("General Curves of not continuous position.png", dpi=720)


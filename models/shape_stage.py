from sympy import nan, Eq, Piecewise, solve, lambdify, diff, symbols, \
    Symbol, plot, linsolve
from sympy.abc import x
import numpy as np
from helper_functions import degree_to_time, time_to_degree, \
    move_sympyplot_to_axes, plot_pvaj, print_list_items_in_row, \
    find_index_in_ordered_list
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
                -136.33,
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
            closed = (degree_to_time(136), (
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
        j1 = JawOnYorkCurve(whether_rebuild=True)
        j1.update_with_solution()
        j1.plot_svaj()
        j2 = JawOnYorkCurve(whether_rebuild=False)
        p, v, a, j = j1.combine_pieces_for_plot(
                  whether_save_png=False,
                  line_color='blue',
                  whether_show_figure=True,
                  whether_knots_ticks=False,
                  # whether_knots_ticks=True,
        )
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

    def plot_curves(self,
                    name='Jaw_on_York',
                    whether_rebuild_for_plot=False,
                    ):
        """
        j2 = JawOnYorkCurve(whether_rebuild=False)
        j2.plot_curves(whether_rebuild_for_plot=True)
        j2.plot_curves(whether_rebuild_for_plot=False)
        """
        if whether_rebuild_for_plot:
            p0, v0, a0, j0 = self.combine_pieces_for_plot(
                whether_save_png=False,
                line_color='blue',
                whether_show_figure=False,
                whether_knots_ticks=True,
            )
            output = open('../data/{}_plots.pkl'.format(self.name), 'wb')
            pickle.dump((p0, v0, a0, j0), output)
            output.close()
        else:
            pkl_file = open('../data/{}_plots.pkl'.format(self.name), 'rb')
            (p0, v0, a0, j0) = pickle.load(pkl_file)
            pkl_file.close()
        plot_pvaj((p0, v0, a0, j0),
                  self.knots,
                  name=name,
                  whether_save_png=False,
                  whether_show_figure=True,
                  whether_knots_ticks=True,
                  )


class TraceOfA(object):
    def __init__(self, whether_load_memo=True, package=None):
        """
        t1 = TraceOfA(whether_load_memo=False)
        """
        # Jaw on York spline Curve
        self.joy_curve = JawOnYorkCurve(whether_rebuild=False)
        # Jaw on York mechanism analysis driving forward
        self.joy_mechanism_forward = O4DriveA()
        # Jaw on York mechanism analysis driving backward
        self.joy_mechanism_backward = ANeedO4()
        if package is None:
            self.package = Package(1000, 'Square', 72, 71, 198, 5, 285.00)
            # self.package = Package(1000, 'Baseline', 94, 63, 166, 5, 245.00)
            # self.package = Package(100, 'Base', 47, 32, 86, 4, 130.00)
            # self.package = Package(330, "Square", 49.5, 48.5, 124.6, 6, 190)
        else:
            self.package = package
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
        output = open('../data/trace_of_A_memo_{}_{}.pkl'.format(
            self.package.volumn, self.package.shape), 'wb')
        pickle.dump(self.memo, output)
        output.close()

    def load_memo_from_file(self):
        """
        t1 = TraceOfA()
        t1.load_memo_from_file()
        """
        pkl_file = open('../data/trace_of_A_memo_{}_{}.pkl'.format(
            self.package.volumn, self.package.shape), 'rb')
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
        r_O4O2_close = expr.subs(x_R_AO2, (-1.5/2))
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
        t2 = TraceOfA(whether_load_memo=False)
        print(t1.get_x_R_AO2_when_touching_expr())
        print(t1.get_x_R_AO2_when_touching_expr().subs(x, t1.get_touch_time()))
            -24.2500000000004
        print(t2.get_x_R_AO2_when_touching_expr().subs(x, t2.get_touch_time()))
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
        t2 = TraceOfA(whether_load_memo=False)
        print(t1.get_x_R_AO2_when_closing_expr().subs(x, degree_to_time(138)))
            ## -7.81597009336110e-14
            # -0.999999999999915
        print(t2.get_x_R_AO2_when_closing_expr().subs(x, degree_to_time(138)))
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
        t2 = TraceOfA(whether_load_memo=False)
        print(t1.get_y_R_AO5_when_touching_expr())
        print(t1.get_y_R_AO5_when_touching_expr().subs(x, t1.get_touch_time()))
            # 24.2500000000000
            # 25.1500000000000
        """
        if 'y_R_AO5_when_touching_expr' in self.memo:
            return self.memo['y_R_AO5_when_touching_expr']
        x_R_AO2_when_touching_expr = \
            self.get_x_R_AO2_when_touching_expr()
        x_R_AO5_when_touching_expr = x_R_AO2_when_touching_expr
        r_GO5 = self.package.depth / 2
        r_AG = r_GO5 - 1.5/2
        y_R_AO5_when_touching_expr = \
            (r_AG ** 2 - (r_GO5 + x_R_AO5_when_touching_expr) ** 2) ** 0.5
        self.memo['y_R_AO5_when_touching_expr'] = y_R_AO5_when_touching_expr
        return y_R_AO5_when_touching_expr

    def get_y_R_AO5_when_closing_expr(self):
        """
        t1 = TraceOfA()
        t1 = TraceOfA(whether_load_memo=False)
        print(t1.get_y_R_AO5_when_closing_expr())
        print(t1.get_y_R_AO5_when_closing_expr().subs(x, degree_to_time(138)))
            1.93692169299983e-6
            # 6.89202437604482
        """
        if 'y_R_AO5_when_closing_expr' in self.memo:
            return self.memo['y_R_AO5_when_closing_expr']
        x_R_AO2_when_closing_expr = \
            self.get_x_R_AO2_when_closing_expr()
        x_R_AO5_when_closing_expr = x_R_AO2_when_closing_expr
        r_GO5 = self.package.depth / 2
        r_AG = r_GO5 - 1.5/2
        y_R_AO5_when_closing_expr = \
            (r_AG ** 2 - (r_GO5 + x_R_AO5_when_closing_expr) ** 2) ** 0.5
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
        end_time = float(degree_to_time(136))
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
        s1 = ShakeHand(name='shake_hand_curve_262_318', whether_rebuild=True)
        s1 = ShakeHand(name='shake_hand_curve_264_318', whether_rebuild=False)
        s1.combine_pieces_for_plot(whether_show_figure=True)
        """
        if start is None:
            start = (degree_to_time(262), (
                0,
                # -422,  # for 330sq
                # -288,  # for 125s
                -633,
                0,
                0,
                nan,
            ))
        if knot1 is None:
            knot1 = (degree_to_time(277), (
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
            knot3 = (degree_to_time(292), (
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
            knot5 = (degree_to_time(310), (
                nan,
                nan,
                nan,
                0,
                nan,
            ))
        if end is None:
            end = (degree_to_time(316), (
                # degree_to_time(318 - 264) * (-422) + 24.25 * 1.3, # for 330sq
                degree_to_time(318 - 262) * (-633) + 30.5 * 1.3,  # for 125s
                # -422,  # for 330sq
                # -288,  # for 125s
                -633,
                0,
                0,
                nan,
            ))
        key_knots = [start, knot1, knot2, knot3, knot4, knot5, end]
        smooth_depth = {
            knot1: 4,
            knot2: 5,
            knot3: 5,
            knot4: 4,
            knot5: 4,
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
                 knot1=None,
                 knot2=None,
                 end=None,
                 name='throw_325_0',
                 whether_rebuild=False
                 ):
        """
        t3 = Throw(whether_rebuild=True)
        t3.combine_pieces_for_plot(whether_show_figure=True)
        """
        if start is None:
            start = (degree_to_time(325), (
                37,
                -438,
                0,
                0,
                nan,
            ))
        if knot1 is None:
            knot1 = (degree_to_time(335), (
                nan,
                nan,
                nan,
                0,
                nan,
            ))
        if knot2 is None:
            knot2 = (degree_to_time(342), (
                nan,
                nan,
                0,
                nan,
                nan,
            ))
        if end is None:
            end = (degree_to_time(360), (
                0,
                0,
                22000,
                nan,
                nan,
            ))
        # key_knots = [start, release, knot1, end]
        key_knots = [start, knot1, knot2, end]
        smooth_depth = {
            knot1: 4,
            knot2: 5,
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


class York(SplineWithPiecewisePolynomial):
    def __init__(self, package=None, whether_rebuild_with_symbol=False):
        """
        com = York(whether_rebuild_with_symbol=True)
        """
        if package is None:
            self.package = Package(1000, 'Square', 72, 71, 198, 5, 285.00)
            # self.package = Package(1000, 'Baseline', 94, 63, 166, 5, 245.00)
            # self.package = Package(100, 'Base', 47, 32, 86, 4, 130.00)
            # self.package = Package(330, "Square", 49.5, 48.5, 124.6, 6, 190)
        else:
            self.package = package
        self.joy = JawOnYorkCurve(whether_rebuild=False)
        self.trace = TraceOfA(whether_load_memo=True)
        self.cons_v = self.package.get_pulling_velocity()
        self.shake2_less_p = 0.4 * (self.package.depth / 2)
        self.touch_less_p = self.trace.get_y_R_AO5_when_closing_expr().subs(
            x, degree_to_time(136))
        self.cons_v_faster = (
                - (self.package.web_repeated_length
                   + self.shake2_less_p
                   + self.touch_less_p) /
                degree_to_time(180)
        )
        self.touching_time = self.trace.get_touch_time()
        self.stages = {}
        self.connection = {}
        self.climb_se = []
        self.touch_se = []
        self.pull1_se = []
        self.shake1_se = []
        self.pull2_se = []
        self.shake2_se = []
        self.pull3_se = []
        self.throw_se = []
        self.key_knots = []
        self.pva_symbols = []
        self.equations = []
        self.solution = {}
        self.accumulate_distances(
            whether_with_symbol=True,
            whether_rebuild=whether_rebuild_with_symbol)
        self.pieces = self.collect_stage_pieces()

    def accumulate_distances(self,
                             whether_with_symbol=True,
                             whether_rebuild=False
                             ):
        throw = self.build_throw(
            whether_with_symbol=whether_with_symbol,
            whether_rebuild=whether_rebuild
        )
        throw_d = throw.get_start_pvaj()[0] - throw.get_end_pvaj()[0]
        throw_end_p = 0
        throw_start_p = throw_end_p + throw_d
        self.connection['throw'] = (throw_start_p, throw_end_p)
        pull3 = self.build_pull3(
            whether_with_symbol=whether_with_symbol,
            whether_rebuild=whether_rebuild
        )
        pull3_d = pull3.get_start_pvaj()[0] - pull3.get_end_pvaj()[0]
        pull3_end_p = throw_start_p
        pull3_start_p = pull3_end_p + pull3_d
        self.connection['pull3'] = (pull3_start_p, pull3_end_p)
        # shake2 = self.build_shake2(
        #     whether_with_symbol=whether_with_symbol,
        #     # whether_with_symbol=True,
        #     whether_rebuild=whether_rebuild
        # )
        shake2_d = -(
                degree_to_time(316 - 262) * self.cons_v_faster
                + self.package.depth / 2
                + self.shake2_less_p
        )
        shake2_end_p = pull3_start_p
        shake2_start_p = shake2_end_p + shake2_d
        self.connection['shake2'] = (shake2_start_p, shake2_end_p)
        pull2 = self.build_pull2(
            whether_with_symbol=whether_with_symbol,
            whether_rebuild=whether_rebuild
        )
        pull2_d = pull2.get_start_pvaj()[0] - pull2.get_end_pvaj()[0]
        pull2_end_p = shake2_start_p
        pull2_start_p = pull2_end_p + pull2_d
        self.connection['pull2'] = (pull2_start_p, pull2_end_p)
        # shake1 = self.build_shake1(
        #     whether_with_symbol=whether_with_symbol,
        #     whether_rebuild=whether_rebuild
        # )
        shake1_d = -(
                degree_to_time(195 - 145) * self.cons_v_faster
                + self.package.depth / 2
        )
        shake1_end_p = pull2_start_p
        shake1_start_p = shake1_end_p + shake1_d
        self.connection['shake1'] = (shake1_start_p, shake1_end_p)
        pull1 = self.build_pull1(
            whether_with_symbol=whether_with_symbol,
            whether_rebuild=whether_rebuild
        )
        pull1_d = pull1.get_start_pvaj()[0] - pull1.get_end_pvaj()[0]
        pull1_end_p = shake1_start_p
        pull1_start_p = pull1_end_p + pull1_d
        self.connection['pull1'] = (pull1_start_p, pull1_end_p)
        touch = self.build_touch(
            whether_with_symbol=whether_with_symbol,
            whether_rebuild=whether_rebuild
        )
        touch_d = touch.get_start_pvaj()[0] - touch.get_end_pvaj()[0]
        print('touch.get_start_pvaj()[0]', touch.get_start_pvaj()[0])
        print('touch.get_end_pvaj()[0]', touch.get_end_pvaj()[0])
        print('touch_d:', touch_d)
        touch_end_p = pull1_start_p
        touch_start_p = touch_end_p + touch_d
        self.connection['touch'] = (touch_start_p, touch_end_p)
        climb = self.build_climb(
            # whether_with_symbol=True,
            whether_with_symbol=whether_with_symbol,
            whether_rebuild=whether_rebuild
        )
        climb_d = climb.get_start_pvaj()[0] - climb.get_end_pvaj()[0]
        climb_end_p = touch_start_p
        climb_start_p = climb_end_p + climb_d
        self.connection['climb'] = (climb_start_p, climb_end_p)

    def build_shake2(self,
                     whether_rebuild=False,
                     whether_with_symbol=False):
        """
        com = York()
        com.build_shake2(whether_rebuild=False)
        com.build_shake2(whether_rebuild=True)
        com.build_shake2().combine_pieces_for_plot(whether_show_figure=True)
        com.build_shake2().get_start_pvaj()
        com.build_shake2().get_end_pvaj()
        37 + 7.67180555555552 + 25.959999999999994 + 75.6220833333334 + 30.548611111111114 + 7.671805555556006 + 31.873260131671003
        = 218.04506568722704
        _ - 146.998262068592
        = 84.001737931408
        37 + 7.67180555555552 + 27.657500000000002
         + 75.6220833333334 + 30.548611111111114 + 7.671805555556006 + 31.873260131671003
        """
        shake2_d = -(
                degree_to_time(316 - 262) * self.cons_v_faster
                + self.package.depth / 2
                + self.shake2_less_p
        )
        if whether_with_symbol:
            name = "shake2_for_accepting_with_symbol"
            shake2_start_p = symbols('shake2_start_p')
            shake2_end_p = shake2_start_p - shake2_d
        else:
            name = "shake2_for_accepting"
            shake2_start_p = self.connection['shake2'][0]
            shake2_end_p = self.connection['shake2'][1]
        try:
            return self.stages[name]
        except KeyError:
            self.stages[name] = ShakeHand(
                name=name,
                start=(degree_to_time(262), (
                    shake2_start_p,
                    self.cons_v_faster,
                    0,
                    0,
                    nan,
                )),
                knot1=(degree_to_time(277), (
                    nan,
                    nan,
                    nan,
                    0,
                    nan,
                )),
                knot2=(degree_to_time(284.5), (
                    nan,
                    nan,
                    nan,
                    nan,
                    0,
                )),
                knot3=(degree_to_time(292), (
                    nan,
                    nan,
                    0,
                    nan,
                    0,
                )),
                knot4=(degree_to_time(301), (
                    nan,
                    nan,
                    nan,
                    nan,
                    0,
                )),
                knot5=(degree_to_time(310), (
                    nan,
                    nan,
                    nan,
                    0,
                    nan,
                )),
                end=(degree_to_time(316), (
                    shake2_end_p,
                    self.cons_v_faster,
                    0,
                    0,
                    nan,
                )),
                whether_rebuild=whether_rebuild,
            )
            return self.stages[name]

    def build_touch(self,
                    whether_rebuild=False,
                    whether_with_symbol=False
                    ):
        """
        com = York()
        com.build_touch(whether_rebuild=False)
        com.build_touch(whether_rebuild=True)
        com.build_touch(whether_rebuild=True, whether_with_symbol=True)
        com.build_touch().combine_pieces_for_plot(whether_show_figure=True)
        com.build_touch().get_start_pvaj()
        com.build_touch().get_end_pvaj()
        146.998262068592 - 115.125001936921
        = 31.873260131671003
        com.build_touch().get_start_pvaj()
(270.604950513073, 106.531117736901, -7442.01723178674, 147802.196471411)
com.build_touch().get_end_pvaj()
(247.802066310273, -584.817254139623, 1.51040812753454e-11, -1.30332113606732e
-9)
        """
        if whether_with_symbol:
            name = "touch_to_fold_with_symbol"
        else:
            name = "touch_to_fold"
        try:
            return self.stages[name]
        except KeyError:
            self.stages[name] = Touch(
                name=name,
                touch=(self.trace.get_touch_time(), (
                    nan,
                    nan,
                    nan,
                    nan,
                    nan,
                )),
                knot2=(degree_to_time(104.5), (
                    nan,
                    nan,
                    nan,
                    nan,
                    nan,
                )),
                knot3=(degree_to_time(112), (
                    nan,
                    nan,
                    nan,
                    nan,
                    nan,
                )),
                knot4=(degree_to_time(121), (
                    nan,
                    nan,
                    nan,
                    nan,
                    nan,
                )),
                knot5=(degree_to_time(130), (
                    nan,
                    nan,
                    nan,
                    nan,
                    nan,
                )),
                end=(degree_to_time(136), (
                    nan,
                    nan,
                    nan,
                    nan,
                    nan,
                )),
                package=self.package,
                shake=self.build_shake2(
                    whether_with_symbol=whether_with_symbol,
                    whether_rebuild=False),
                joy=self.joy,
                whether_rebuild=whether_rebuild,
            )
            return self.stages[name]

    def build_climb(self,
                    whether_rebuild=False,
                    whether_with_symbol=False
                    ):
        """
        com = York()
        com.build_climb(whether_rebuild=True)
        com.build_climb().combine_pieces_for_plot(whether_show_figure=True)
        com.build_climb().get_end_pvaj()
        37 + 7.3888888888 + 25.475 + 72.83 + 28.5277777777 + 7.38 + 31.873260131671003
        210.47492679817103
        """
        if whether_with_symbol:
            name = "climb_to_touch_with_symbol"
            climb_end_p = symbols('climb_end_p')
        else:
            name = "climb_to_touch"
            climb_end_p = self.connection['climb'][1]
        try:
            return self.stages[name]
        except KeyError:
            self.stages[name] = Climb(
                name=name,
                start=(degree_to_time(0), (
                    0,
                    0,
                    # 22000,  # for 330sq
                    # 14000,  # for 125s
                    35000,  # for TBA1000sq
                    # 147784.235076798,  # for 330sq
                    # 372166.82180039,  # for 125s
                    177112.788893618,  # for TBA1000sq
                    nan,
                )),
                cross=(degree_to_time(40), (
                    # 122,  # for 330sq
                    170,  # for TBA1000sq
                    nan,
                    nan,
                    nan,
                    nan,
                )),
                high=(degree_to_time(80), (
                    nan,
                    0,
                    nan,
                    nan,
                    nan,
                )),
                touch=(self.touching_time, (
                    # climb_end_p,
                    # 219.419594153918,
                    # -44.0031089879033,
                    # -1508.50518522546,
                    # 10950.5981182494,
                    # 152.083898260352,
                    # 99.935766976934,
                    # -11712.5721657465,
                    # 373048.366333169,
                    338.2887729644,
                    -382.545496050749,
                    1096.08981377025,
                    853439.642075869,
                    nan,
                )),
                whether_rebuild=whether_rebuild,
            )
            return self.stages[name]

    def build_pull1(self,
                    whether_rebuild=False,
                    whether_with_symbol=False
                    ):
        """
        com = York()
        com.build_pull1(whether_rebuild=False)
        com.build_pull1(whether_rebuild=True)
        com.build_pull1().plot_svaj()
        com.build_pull1().get_start_pvaj()
        com.build_pull1().get_end_pvaj()
        """
        if whether_with_symbol:
            name = "pull_1_with_symbol"
            pull1_start_p = symbols('pull1_start_p')
        else:
            name = "pull_1"
            pull1_start_p = self.connection['pull1'][0]
        try:
            return self.stages[name]
        except KeyError:
            self.stages[name] = Pull(
                name=name,
                start=(degree_to_time(136), (
                    pull1_start_p,
                    self.cons_v_faster,
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
            return self.stages[name]

    def build_shake1(self,
                     whether_rebuild=False,
                     whether_with_symbol=False
                     ):
        """
        com = York()
        com.build_shake1(whether_rebuild=False)
        com.build_shake1(whether_rebuild=True)
        com.build_shake1().plot_svaj()
        com.build_shake1().get_start_pvaj()
        com.build_shake1().get_end_pvaj()
        37 + 7.67180555555552 + 27.657500000000002 + 75.6220833333334 + 30.548611111111114 + 7.671805555556006 + 31.873260131671003
        """
        if whether_with_symbol:
            name = "shake1_for_ear_with_symbols"
            shake1_start_p = symbols('shake1_start_p')
            shake1_end_p = (shake1_start_p
                            + degree_to_time(195 - 145) * self.cons_v_faster
                            + self.package.depth / 2 * 1.0),
        else:
            name = "shake1_for_ear"
            shake1_start_p = self.connection['shake1'][0]
            shake1_end_p = self.connection['shake1'][1]
        try:
            return self.stages[name]
        except KeyError:
            self.stages[name] = ShakeHand(
                name=name,
                start=(degree_to_time(145), (
                    shake1_start_p,
                    self.cons_v_faster,
                    0,
                    0,
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
                    shake1_end_p,
                    self.cons_v_faster,
                    0,
                    0,
                    nan,
                )),
                whether_rebuild=whether_rebuild,
            )
            return self.stages[name]

    def build_pull2(self,
                    whether_rebuild=False,
                    whether_with_symbol=False
                    ):
        """
        com = York()
        com.build_pull2(whether_rebuild=False)
        com.build_pull2(whether_rebuild=True)
        com.build_pull2().plot_svaj()
        com.build_pull2().get_start_pvaj()
        com.build_pull2().get_end_pvaj()
        """
        if whether_with_symbol:
            name = "pull_2_with_symbol"
            pull2_start_p = symbols('pull2_start_p')
        else:
            name = "pull_2"
            pull2_start_p = self.connection['pull2'][0]
        try:
            return self.stages[name]
        except KeyError:
            self.stages[name] = Pull(
                name=name,
                start=(degree_to_time(195), (
                    pull2_start_p,
                    self.cons_v_faster,
                    nan,
                    nan,
                    nan,
                )),
                end=(degree_to_time(262), (
                    nan,
                    nan,
                    nan,
                    nan,
                    nan,
                )),
                whether_rebuild=whether_rebuild,
            )
            return self.stages[name]

    def build_pull3(self,
                    whether_rebuild=False,
                    whether_with_symbol=False):
        """
        com = York()
        com.build_pull3(whether_rebuild=False)
        com.build_pull3(whether_rebuild=True)
        com.build_pull3().plot_svaj()
        com.build_pull3().get_start_pvaj()
        com.build_pull3().get_end_pvaj()
        """
        if whether_with_symbol:
            name = "pull_3_with_symbol"
            pull3_start_p = symbols('pull3_start_p')
        else:
            name = "pull_3"
            pull3_start_p = self.connection['pull3'][0]
        try:
            return self.stages[name]
        except KeyError:
            self.stages[name] = Pull(
                name=name,
                start=(degree_to_time(316), (
                    pull3_start_p,
                    self.cons_v_faster,
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
            return self.stages[name]

    def build_throw(self,
                    whether_rebuild=False,
                    whether_with_symbol=False):
        """
        com = York()
        com.build_throw(whether_rebuild=True)
        com.build_throw().combine_pieces_for_plot(whether_show_figure=True)
        com.build_throw().get_start_pvaj()
        com.build_throw().get_end_pvaj()
        """
        if whether_with_symbol:
            name = "throw_to_bottom_with_symbol"
            # throw_start_p = symbols('throw_start_p')
        else:
            name = "throw_to_bottom"
            # throw_start_p = self.connection['throw'][0]
        try:
            return self.stages[name]
        except KeyError:
            self.stages[name] = Throw(
                name=name,
                start=(degree_to_time(325), (
                    # 37,  # for 330sq
                    # 27,  # for 125s
                    # 50,  # for 1000b
                    60,
                    self.cons_v_faster,
                    0,
                    0,
                    nan,
                )),
                knot1=(degree_to_time(335), (
                    # 44.5,
                    nan,
                    nan,
                    nan,
                    0,
                    nan,
                )),
                knot2=(degree_to_time(342), (
                    nan,
                    nan,
                    0,
                    nan,
                    nan,
                )),
                end=(degree_to_time(360), (
                    0,
                    0,
                    # 22000,  # for 330sq
                    # 18000,  # for 125s
                    # 32000,  # for 1000b
                    35000,  # for 1000sq
                    nan,
                    nan,
                )),
                whether_rebuild=whether_rebuild,
            )
            return self.stages[name]

    def collect_key_knots(self):
        """
        com = York()
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
        com = York()
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
        com = York()
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

    def plot_curves(self, name='General_Curves', whether_save_png=False):
        """
        com = York()
        actual_pieces = com.collect_stage_pieces()
        print('actual num of pieces: ', len(actual_pieces))
        com.plot_curves(whether_save_png=True)
        """
        p0, v0, a0, j0 = self.combine_pieces_for_plot(
            line_color='blue',
            whether_show_figure=False,
        )
        # p0_joy, v0_joy, a0_joy, j0_ = self.joy.combine_pieces_for_plot(
        #     line_color='red',
        #     whether_show_figure=False,
        # )
        # p0.extend(p0_joy)
        # v0.extend(v0_joy)
        # a0.extend(a0_joy)
        # j0.extend(j0_joy)
        plot_pvaj((p0, v0, a0, j0),
                  self.knots,
                  name="for TPA330sq",
                  whether_save_png=whether_save_png,
                  whether_show_figure=True,
                  whether_knots_ticks=True,
                  )

    #
    # def identify_variables(self):
    #     """
    #     com = York()
    #     pva_symbols = com.identify_variables()
    #     num_of_variables = len(pva_symbols)
    #     print(num_of_variables)
    #     for i in range(num_of_variables):
    #         print(pva_symbols[i])
    #     """
    #     pva_symbols = [
    #         symbols('shake2_start_p'),
    #         symbols('climb_start_a'),
    #         symbols('climb_start_j'),
    #         symbols('climb_high_p'),
    #         symbols('climb_touch_v'),
    #         symbols('climb_touch_a'),
    #         symbols('climb_touch_j'),
    #         symbols('pull1_start_p'),
    #         symbols('shake1_start_p'),
    #         symbols('pull2_start_p'),
    #         symbols('pull3_start_p'),
    #         symbols('throw_start_p'),
    #         symbols('throw_end_a'),
    #     ]
    #     self.pva_symbols.extend(pva_symbols)
    #     return self.pva_symbols
    #
    # def build_equations(self):
    #     """
    #     com = York()
    #     equations = com.build_equations()
    #     solution = solve(equations, pva_symbols)
    #     print(solution)
    #     num_of_variables = len(pva_symbols)
    #     print(num_of_variables)
    #     for i in range(num_of_variables):
    #         print(pva_symbols[i])
    #     """
    #     equations = [
    #         Eq(self.build_climb().get_start_pvaj()[2],
    #            self.build_throw().get_end_pvaj()[2]),
    #         Eq(self.build_climb().get_start_pvaj()[3],
    #            self.build_throw().get_end_pvaj()[3]),
    #         Eq(self.build_climb().get_end_pvaj()[0],
    #            self.build_touch().get_start_pvaj()[0]),
    #         Eq(self.build_climb().get_end_pvaj()[1],
    #            self.build_touch().get_start_pvaj()[1]),
    #         Eq(self.build_climb().get_end_pvaj()[2],
    #            self.build_touch().get_start_pvaj()[2]),
    #         Eq(self.build_climb().get_end_pvaj()[3],
    #            self.build_touch().get_start_pvaj()[3]),
    #         Eq(self.build_touch().get_end_pvaj()[0],
    #            self.build_pull1().get_start_pvaj()[0]),
    #         Eq(self.build_pull1().get_end_pvaj()[0],
    #            self.build_shake1().get_start_pvaj()[0]),
    #         Eq(self.build_shake1().get_end_pvaj()[0],
    #            self.build_pull2().get_start_pvaj()[0]),
    #         Eq(self.build_pull2().get_end_pvaj()[0],
    #            self.build_shake2().get_start_pvaj()[0]),
    #         Eq(self.build_shake2().get_end_pvaj()[0],
    #            self.build_pull3().get_start_pvaj()[0]),
    #         Eq(self.build_pull3().get_end_pvaj()[0],
    #            self.build_throw().get_start_pvaj()[0]),
    #         # Eq(self.build_climb().get_kth_expr_of_ith_piece(4, 2).subs(
    #         #     x, self.touching_time),
    #         #    self.build_touch().get_kth_expr_of_ith_piece(4, 0).subs(
    #         #        x, self.touching_time)),
    #         Eq(self.build_climb().get_kth_expr_of_ith_piece(4, 0).subs(
    #             x, 0),
    #             self.build_throw().get_kth_expr_of_ith_piece(4, 2).subs(
    #                 x, degree_to_time(360))),
    #     ]
    #     self.equations.extend(equations)
    #     return self.equations
    #
    # def solve_equations(self):
    #     """
    #     com = York()
    #     com.solve_equations()
    #     """
    #     pva_symbols = self.identify_variables()
    #     num_of_variables = len(pva_symbols)
    #     for i in range(num_of_variables):
    #         print(pva_symbols[i])
    #     equations = self.build_equations()
    #     for i in range(len(equations)):
    #         print(equations[i])
    #     solution = solve(equations, pva_symbols)
    #     for key in solution.keys():
    #         print(str(key), ':', solution[key])
    #     self.solution = solution
    #     return self.solution
    #
    # def update_pieces_with_solution(self):
    #     """
    #     com = York()
    #     com.update_pieces_with_solution()
    #     """
    #     actual_pieces = self.collect_stage_pieces()
    #     solution = self.solve_equations()
    #     self.involve_solutions(solution)
    #     self.plot_pvaj(name='General Curve of Wired Solution.png')
    #


class Jaw(SplineWithPiecewisePolynomial):
    def __init__(self,
                 name="jaw_driver",
                 whether_rebuild=False):
        """
        jaw = Jaw(whether_rebuild=True)
        p, v, a, j = jaw.combine_pieces_for_plot()

        """
        self.name = name
        self.york = York(whether_rebuild_with_symbol=False)
        self.joy = JawOnYorkCurve(whether_rebuild=False)
        york_pieces = self.york.collect_stage_pieces()
        self.temp_knots = []
        self.combine_knots()
        key_knots = [
            (self.temp_knots[i], (nan, nan, nan, nan, nan))
            for i in range(len(self.temp_knots))
        ]
        SplineWithPiecewisePolynomial.__init__(self, key_knots=key_knots)
        if whether_rebuild:
            self.refresh_pieces()
            self.save_solved_pieces()
        else:
            self.load_solved_pieces()

    def combine_knots(self):
        """
        jaw = Jaw()
        temp_knots = time_to_degree(jaw.combine_knots())
        print_list_items_in_row(temp_knots)
        """
        york_knots = self.york.get_knots().copy()
        joy_knots = self.joy.get_knots().copy()
        try:
            while True:
                if york_knots[0] < joy_knots[0]:
                    self.temp_knots.append(york_knots.pop(0))
                elif york_knots[0] == joy_knots[0]:
                    self.temp_knots.append(york_knots.pop(0))
                    joy_knots.pop(0)
                else:
                    self.temp_knots.append(joy_knots.pop(0))
        except IndexError:
            if len(york_knots) < len(joy_knots):
                self.temp_knots.extend(joy_knots)
            else:
                self.temp_knots.extend(york_knots)
        return self.temp_knots

    def refresh_pieces(self):
        """
        jaw = Jaw()
        york_knots = jaw.york.get_knots()
        joy_knots = jaw.joy.get_knots()
        for i in range(len(jaw.pieces)):
            start_knot = jaw.pieces[3].get_piece()[0]
            york_index = find_index_in_ordered_list(start_knot, york_knots)
            joy_index = find_index_in_ordered_list(start_knot, joy_knots)
            new_expressions = []
                new_expressions.append(
                    jaw.york.get_kth_expr_of_ith_piece(0, york_index)
                    + jaw.joy.get_kth_expr_of_ith_piece(0, joy_index)
                )
            jaw.update_piece_with_new_expressions(i, new_expressions)
            jaw.update_piece_with_new_expressions(0, new_expressions)
        return self.pieces
        jaw = Jaw()
        jaw.refresh_pieces()
        temp_knots = time_to_degree(jaw.combine_knots())
        print_list_items_in_row(temp_knots)
        """
        york_knots = self.york.get_knots()
        joy_knots = self.joy.get_knots()
        for i in range(len(self.get_pieces())):
            start_knot = self.pieces[i].get_piece()[0]
            york_index = find_index_in_ordered_list(start_knot, york_knots)
            joy_index = find_index_in_ordered_list(start_knot, joy_knots)
            new_expressions = []
            for j in range(4):
                new_expressions.append(
                    self.york.get_kth_expr_of_ith_piece(j, york_index)
                    + self.joy.get_kth_expr_of_ith_piece(j, joy_index)
                )
            self.update_piece_with_new_expressions(i, new_expressions)
        return self.pieces

    def plot_curves(self, name='Jaw absolutely', whether_save_png=False):
        """
        jaw = Jaw()
        jaw.plot_curves()
        """
        p0, v0, a0, j0 = self.combine_pieces_for_plot(
            line_color='blue',
            whether_show_figure=False,
        )
        plot_pvaj((p0, v0, a0, j0),
                  self.knots,
                  name=name,
                  whether_save_png=whether_save_png,
                  whether_show_figure=True,
                  whether_knots_ticks=False,
                  )


class Combine(SplineWithPiecewisePolynomial):
    def __init__(self,
                 name="york_and_jaw",
                 whether_rebuild=False,
                 ):
        """
        com = Combine(whether_rebuild=True)
        """
        self.name = name
        self.york = York(whether_rebuild_with_symbol=False)
        self.joy = JawOnYorkCurve(whether_rebuild=False)
        self.jaw = Jaw(whether_rebuild=False)
        # if whether_rebuild:
        #     self.jaw.refresh_pieces()
        # else:
        #     self.load_solved_pieces()

    def plot_curves(self,
                    name='Cam Curves for TPA 330sq',
                    whether_rebuild_for_plot=False,
                    ):
        """
        com = Combine()
        com.plot_curves(whether_rebuild_for_plot=False)
        com.plot_curves(whether_rebuild_for_plot=True)
        """
        if whether_rebuild_for_plot:
            p0_york, v0_york, a0_york, j0_york = \
                self.york.combine_pieces_for_plot(
                    line_color='blue',
                    whether_show_figure=False,
                )
            p0_joy, v0_joy, a0_joy, j0_joy = \
                self.joy.combine_pieces_for_plot(
                    line_color='red',
                    whether_show_figure=False,
                )
            p0_jaw, v0_jaw, a0_jaw, j0_jaw = \
                self.jaw.combine_pieces_for_plot(
                    line_color='green',
                    whether_show_figure=False,
                )
            p0_york.extend(p0_joy)
            v0_york.extend(v0_joy)
            a0_york.extend(a0_joy)
            j0_york.extend(j0_joy)
            p0_york.extend(p0_jaw)
            v0_york.extend(v0_jaw)
            a0_york.extend(a0_jaw)
            j0_york.extend(j0_jaw)
            output = open('../data/{}_plots.pkl'.format(self.name), 'wb')
            pickle.dump((p0_york, v0_york, a0_york, j0_york), output)
            output.close()
        else:
            pkl_file = open('../data/{}_plots.pkl'.format(self.name), 'rb')
            (p0_york, v0_york, a0_york, j0_york) = pickle.load(pkl_file)
            pkl_file.close()
        plot_pvaj((p0_york, v0_york, a0_york, j0_york),
                  self.jaw.knots,
                  name=name,
                  whether_save_png=True,
                  whether_show_figure=True,
                  whether_knots_ticks=True,
                  )

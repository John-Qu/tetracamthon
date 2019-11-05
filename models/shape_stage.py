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
        took_knot_at = [
            start, knot1, widest, knot4, knot2, closed, release, knot3, end
        ]
        self.smooth_depth = {
            1: 4,
            2: 6,
            3: 4,
            4: 4,
            5: 4,
            6: 4,
            7: 4,
        }
        self.periodic_depth = 6
        knots = [took_knot_at[i][0] for i in range(len(took_knot_at))]
        pvajp = [
            [took_knot_at[i][1][j] for i in range(len(took_knot_at))]
            for j in range(5)
        ]
        orders = [6] * len(took_knot_at)
        SplineWithPiecewisePolynomial.__init__(self, knots, orders,
                                               pvajp, name=name)
        if whether_rebuild_pieces:
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
                 start=None, end=None,
                 if_rebuild_pieces=False):
        """
        s1 = ShakeHand(name='shake_hand_curve_262_317', if_rebuild_pieces=True)
        """
        if start is None:
            start = (degree_to_time(262), (
                0,
                -422,
                0,
                0,
                nan,
            ))
        if end is None:
            end = (degree_to_time(317), (
                nan,
                -422,
                0,
                0,
                nan,
            ))
        delta = end[0] - start[0]
        knot1 = (start[0] + delta / 10 * 2, (
            nan,
            nan,
            nan,
            0,
            nan,
        ))
        knot2 = (start[0] + delta / 10 * 3, (
            nan,
            nan,
            nan,
            nan,
            0,
        ))
        knot3 = (start[0] + delta / 10 * 5, (
            nan,
            -122,
            0,
            nan,
            nan,
        ))
        knot4 = (start[0] + delta / 10 * 7, (
            nan,
            nan,
            nan,
            nan,
            0,
        ))
        knot5 = (start[0] + delta / 10 * 8, (
            nan,
            nan,
            nan,
            0,
            nan,
        ))
        # pvajp = [
        #     [self.start_p, nan, nan, nan, nan, nan, self.end_p],
        #     [self.cons_v, nan, nan, self.mod_v, nan, nan, self.cons_v],
        #     [0, nan, nan, 0, nan, nan, 0],
        #     [0, 0, nan, nan, nan, 0, 0],
        #     [nan, nan, 0, nan, 0, nan, nan]
        # ]
        # orders = [6 for i in range(len(knots) - 1)]
        took_knot_at = [start, knot1, knot2, knot3, knot4, knot5, end]
        knots = [took_knot_at[i][0] for i in range(len(took_knot_at))]
        pvajp = [[took_knot_at[i][1][j] for i in range(len(took_knot_at))]
                 for j in range(5)]
        orders = [6] * len(took_knot_at)
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

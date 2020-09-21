from math import sqrt

from sympy import plot
from tetracamthon.helper import trans_degree_to_time, trans_time_to_degree, \
    move_sympy_plot_to_plt_axes
from tetracamthon.polynomial import Spline, KnotsInSpline
from tetracamthon.package import Package, Productivity, Production
from tetracamthon.mechanism import TracingOfPointA
from sympy.abc import t
import matplotlib.pyplot as plt


class JawOnYork(Spline):
    def __init__(self,
                 name="spline_of_jaw_on_york",
                 informed_knots=KnotsInSpline(
                     knots_info_csv="/Users/johnqu/PycharmProjects/"
                                    "tetracamthon/src/tetracamthon/knot_info/"
                                    "jaw_on_york_with_eight_knots.csv"
                 ),
                 whether_reload=False,
                 ):
        Spline.__init__(self,
                        name=name,
                        a_set_of_informed_knots=informed_knots,
                        whether_reload=whether_reload,
                        )

    def plot_symbolically(self, whether_save_png=False):
        self.plot_spline_on_subplots(
            whether_save_png=whether_save_png,
            whether_show_figure=True,
            whether_knots_ticks=True,
            whether_annotate=True,
        )


class ShakingHandWithClampingBottom(Spline):
    def __init__(self,
                 name="spline_of_shaking_hand_with_clamping_bottom",
                 a_set_of_informed_knots=KnotsInSpline(
                     knots_info_csv="/Users/johnqu/PycharmProjects/"
                                    "tetracamthon/src/tetracamthon/knot_info/"
                                    "shaking_hand_with_clamping_bottom.csv"
                 ),
                 a_production=Production(Package('1000SQ'), Productivity(
                     8000)),
                 whether_reload=False,
                 ):
        self.production = a_production
        self.informed_knots = a_set_of_informed_knots
        self.modify_knot_value(
            'start',
            0,
            (self.informed_knots.knots_with_info[-1].pvajp[0] +
             sqrt((-self.production.get_average_velocity() *
                   self.production.get_time_of_clamping() -
                   self.production.get_extra_length_of_clamping()) ** 2 -
                  (self.production.get_extra_length_of_clamping()) ** 2)
             )
        )
        self.modify_knot_value(
            'start',
            1,
            self.production.get_average_velocity()
        )
        self.modify_knot_value(
            'end',
            1,
            self.production.get_average_velocity()
        )
        Spline.__init__(self,
                        name=name,
                        a_set_of_informed_knots=self.informed_knots,
                        whether_reload=whether_reload,
                        )
        if whether_reload:
            self.load_solved_pieces_of_polynomial()
        else:
            self.save_solved_pieces_of_polynomial()

    def plot_symbolically(self, whether_save_png=False):
        self.plot_spline_on_subplots(
            whether_save_png=whether_save_png,
            whether_show_figure=True,
            whether_knots_ticks=True,
            whether_annotate=True,
        )


class ShakingHandWithFoldingEar(Spline):
    def __init__(self,
                 name="spline_of_shaking_hand_with_folding_ear",
                 a_set_of_informed_knots=KnotsInSpline(
                     knots_info_csv="/Users/johnqu/PycharmProjects/"
                                    "tetracamthon/src/tetracamthon/knot_info/"
                                    "shaking_hand_with_folding_ear.csv"
                 ),
                 a_production=Production(Package('1000SQ'), Productivity(
                     8000)),
                 whether_reload=False,
                 ):
        self.production = a_production
        self.informed_knots = a_set_of_informed_knots
        self.modify_knot_value(
            'start',
            0,
            (self.informed_knots.knots_with_info[-1].pvajp[0] -
             (self.production.get_average_velocity() *
              self.production.get_time_of_folding() +
              self.production.get_extra_length_of_folding())
             )
        )
        self.modify_knot_value(
            'start',
            1,
            self.production.get_average_velocity()
        )
        self.modify_knot_value(
            'end',
            1,
            self.production.get_average_velocity()
        )
        Spline.__init__(self,
                        name=name,
                        a_set_of_informed_knots=self.informed_knots,
                        whether_reload=whether_reload,
                        )

    def plot_symbolically(self, whether_save_png=False):
        self.plot_spline_on_subplots(
            whether_save_png=whether_save_png,
            whether_show_figure=True,
            whether_knots_ticks=True,
            whether_annotate=True,
        )


class PullingTube(Spline):
    def __init__(self,
                 name="spline_of_pulling_tube",
                 a_set_of_informed_knots=KnotsInSpline(
                     knots_info_csv=(
                             "/Users/johnqu/PycharmProjects/" +
                             "tetracamthon/src/tetracamthon/knot_info/" +
                             "pulling_tube.csv"
                     ),
                 ),
                 a_production=Production(Package('1000SQ'),
                                         Productivity(8000)),
                 whether_reload=False,
                 ):
        self.production = a_production
        self.informed_knots = a_set_of_informed_knots
        self.modify_knot_value(
            'start',
            1,
            self.production.get_average_velocity()
        )
        Spline.__init__(self,
                        name=name,
                        a_set_of_informed_knots=self.informed_knots,
                        whether_reload=whether_reload,
                        )


class WaitingLock(Spline):
    def __init__(self,
                 name="spline_of_waiting_lock",
                 a_set_of_informed_knots=KnotsInSpline(
                     knots_info_csv=(
                             "/Users/johnqu/PycharmProjects/" +
                             "tetracamthon/src/tetracamthon/knot_info/" +
                             "waiting_lock.csv"
                     ),
                 ),
                 a_production=Production(Package('1000SQ'),
                                         Productivity(8000)),
                 whether_reload=False,
                 ):
        self.production = a_production
        self.informed_knots = a_set_of_informed_knots
        self.modify_knot_value(
            'start',
            1,
            self.production.get_average_velocity()
        )
        Spline.__init__(self,
                        name=name,
                        a_set_of_informed_knots=self.informed_knots,
                        whether_reload=whether_reload,
                        )


class WaitingKnife(Spline):
    def __init__(self,
                 name="spline_of_waiting_knife",
                 a_set_of_informed_knots=KnotsInSpline(
                     knots_info_csv=(
                             "/Users/johnqu/PycharmProjects/" +
                             "tetracamthon/src/tetracamthon/knot_info/" +
                             "waiting_knife.csv"
                     ),
                 ),
                 a_production=Production(Package('1000SQ'),
                                         Productivity(8000)),
                 whether_reload=False,
                 ):
        self.production = a_production
        self.informed_knots = a_set_of_informed_knots
        self.modify_knot_value(
            'start',
            1,
            self.production.get_average_velocity()
        )
        Spline.__init__(self,
                        name=name,
                        a_set_of_informed_knots=self.informed_knots,
                        whether_reload=whether_reload,
                        )


class ClampingBottom(Spline):
    def __init__(self,
                 name="spline_of_clamping_bottom",
                 a_set_of_informed_knots=KnotsInSpline(
                     knots_info_csv=(
                             "/Users/johnqu/PycharmProjects/"
                             "tetracamthon/src/tetracamthon/knot_info/"
                             "clamping_bottom.csv"
                     ),
                 ),
                 a_production=Production(Package('1000SQ'),
                                         Productivity(8000)),
                 a_spline_of_shake_hand_with_clamping_bottom=(
                         ShakingHandWithClampingBottom(
                             whether_reload=True,
                         )
                 ),
                 a_tracing_of_point_a=TracingOfPointA(
                     a_jaw_on_york_spline=JawOnYork(
                         whether_reload=True,
                     ),
                     whether_reload=True,
                 ),
                 whether_reload=False,
                 ):
        self.production = a_production
        self.informed_knots = a_set_of_informed_knots
        self.shaking = a_spline_of_shake_hand_with_clamping_bottom
        self.tracing = a_tracing_of_point_a
        self.modify_knot('touch', trans_time_to_degree(
            self.tracing.get_t_touched()))
        self.modify_knot('knot3', self.shaking.get_knot_with_info_by_knot_id(
            'knot3').knot - 180)
        self.modify_knot('knot2',
                         self.tracing.joy_spline.get_knot_with_info_by_knot_id(
                             'knot2').knot)
        self.modify_knot('closed',
                         self.tracing.joy_spline.get_knot_with_info_by_knot_id(
                             'closed').knot)
        Spline.__init__(self,
                        name=name,
                        a_set_of_informed_knots=self.informed_knots,
                        whether_reload=False,
                        whether_solve=False
                        )
        if whether_reload:
            self.load_solved_pieces_of_polynomial()
        else:
            self.construct_pieces()
            self.save_solved_pieces_of_polynomial()

    def construct_pieces(self):
        """Construct pieces with mechanism dimension, shaking hand spline, and
        tracing of point A functions.
        r_o5o2: constant float
        left_york_pos_of_t: shaking hand spline of left york by right york's
            time, also has two pieces:
            84d______ps[0]___________111.5d_________ps[1]______________140d
        y_ao2_of_t, y_ao5_of_t: tracing of point A, whose function expressions
            has two element:
                91d__________pt[0]__________________121d______pt[1]____137d
        So for the knots of ClampingBottom:
                91d_____pc[0]________111.5d__pc[1]__121d_____pc[2]_____137d
            the index of shaking and tracing are:
                     ps[0] pt[0]           ps[1]pt[0]      ps[1]pt[1]
        """
        r_o5o2 = self.get_distance_o5o2()
        y_ao2_of_t = self.tracing.get_y_AO2_of_t_while_clamping()
        y_ao5_of_t = self.tracing.get_y_AO5_of_t_while_clamping()
        left_york_pos_of_t = (
            (self.shaking.get_pieces_of_polynomial()[0]
             .get_expr_with_co_val()[0].subs(t, self.get_t_left_york())),
            (self.shaking.get_pieces_of_polynomial()[1]
             .get_expr_with_co_val()[0].subs(t, self.get_t_left_york()))
        )
        for i_of_piece in range(self.num_of_pieces):
            if i_of_piece == 0:
                i_of_shaking = 0
                i_of_tracing = 0
            elif i_of_piece == 1:
                i_of_shaking = 1
                i_of_tracing = 0
            else:
                i_of_shaking = 1
                i_of_tracing = 1
            expr_i = (
                    left_york_pos_of_t[i_of_shaking]
                    + y_ao5_of_t[i_of_tracing]
                    - y_ao2_of_t[i_of_tracing]
                    + r_o5o2
            )
            self.pieces_of_polynomial[i_of_piece].fill_expr_lis_with_diff(
                expr_i
            )
        return self

    def get_t_left_york(self):
        time_half_cycle = trans_degree_to_time(
            180,
            cycle_time=self.production.productivity.get_cycle_time()
        )
        t_left_york = t + time_half_cycle
        return t_left_york

    def get_distance_o5o2(self):
        result = (
                self.production.package.height +
                self.production.package.horizontal_sealing_length +
                self.tracing.forward.lDC.r.val -
                self.production.package.top_gap +
                3.99189865564460
        )
        return result

    def plot_one_polynomial_at_one_depth(self, i_of_piece, i_of_depth):
        p = plot(
            (self.get_pieces_of_polynomial()[i_of_piece].
                get_expr_with_co_val()[i_of_depth]),
            (t, self.knots[i_of_piece], self.knots[i_of_piece + 1]),
            title='Piece ' + str(i_of_piece) + ' at depth ' + str(i_of_depth),
            show=False
        )
        fig, axs = plt.subplots(nrows=2)
        move_sympy_plot_to_plt_axes(p, axs[0])
        move_sympy_plot_to_plt_axes(p, axs[1])
        axs[0].grid(True)
        axs[0].set_xticks(self.knots)
        axs[0].set_xticklabels(str(trans_time_to_degree(self.knots)))
        plt.show()

    def plot_to_depth_of_acceleration(self):
        self.plot_spline_on_subplots(axs_num=3)


class ClimbingBack(Spline):
    def __init__(self,
                 name="spline_of_climbing_back",
                 a_set_of_informed_knots=KnotsInSpline(
                     knots_info_csv=(
                             "/Users/johnqu/PycharmProjects/" +
                             "tetracamthon/src/tetracamthon/knot_info/" +
                             "climbing_back.csv"
                     ),
                 ),
                 a_production=Production(Package('1000SQ'),
                                         Productivity(8000)),
                 a_tracing_of_point_a=TracingOfPointA(
                     a_jaw_on_york_spline=JawOnYork(
                         whether_reload=True,
                     ),
                     whether_reload=True,
                 ),
                 whether_reload=False,
                 ):
        self.production = a_production
        self.informed_knots = a_set_of_informed_knots
        self.tracing = a_tracing_of_point_a
        self.modify_knot('touch', trans_time_to_degree(
            self.tracing.get_t_touched()))
        Spline.__init__(self,
                        name=name,
                        a_set_of_informed_knots=self.informed_knots,
                        whether_reload=whether_reload,
                        )


class ThrowingPack(Spline):
    def __init__(self,
                 name="spline_of_throwing_pack",
                 informed_knots=KnotsInSpline(
                     knots_info_csv=(
                             "/Users/johnqu/PycharmProjects/" +
                             "tetracamthon/src/tetracamthon/knot_info/" +
                             "throwing_pack.csv"
                     ),
                 ),
                 a_production=Production(Package('1000SQ'),
                                         Productivity(8000)),
                 whether_reload=False,
                 ):
        self.production = a_production
        self.informed_knots = informed_knots
        Spline.__init__(self,
                        name=name,
                        a_set_of_informed_knots=self.informed_knots,
                        whether_reload=whether_reload,
                        )


class StagesConnector(object):
    def __init__(
            self,
            machine_production=Production(
                Package('1000SQ'),
                Productivity(8000)
            ),
            whether_reload=False):
        self.production = machine_production
        self.jaw_on_york = JawOnYork(
            whether_reload=whether_reload
        )
        self.tracing_of_point_a = TracingOfPointA(
            self.jaw_on_york,
            a_spec_id=self.production.package.spec_id,
            a_package_id=self.production.package.package_id,
            whether_reload=whether_reload
        )
        self.throwing_pack = ThrowingPack(
            a_production=self.production,
            whether_reload=whether_reload
        )
        self.climbing_back = ClimbingBack(
            a_production=self.production,
            whether_reload=whether_reload
        )
        self.pulling_tube = PullingTube(
            a_production=self.production,
            whether_reload=whether_reload
        )
        self.waiting_lock = WaitingLock(
            a_production=self.production,
            whether_reload=whether_reload
        )
        self.waiting_knife = WaitingKnife(
            a_production=self.production,
            whether_reload=whether_reload
        )
        self.shaking_hand_with_clamping_bottom = ShakingHandWithClampingBottom(
            a_production=self.production,
            whether_reload=whether_reload
        )
        self.shaking_hand_with_folding_ear = ShakingHandWithFoldingEar(
            a_production=self.production,
            whether_reload=whether_reload
        )
        self.clamping_bottom = ClampingBottom(
            a_production=self.production,
            a_spline_of_shake_hand_with_clamping_bottom=(
                self.shaking_hand_with_clamping_bottom
            ),
            a_tracing_of_point_a=self.tracing_of_point_a,
            whether_reload=whether_reload,
        )
        self.connector = {}
        self.collect_connectors()

    def collect_connectors(self):
        if len(self.connector):
            return self.connector
        self.connector['throwing_pack_end_acc'] = (
            self.throwing_pack.get_a_dyn_at_boundary('end', 2)
        )
        self.connector['throwing_pack_end_jer'] = (
            self.throwing_pack.get_a_dyn_at_boundary('end', 3)
        )
        self.connector['throwing_pack_start_pos'] = (
            self.throwing_pack.get_a_dyn_at_boundary('start', 0)
        )
        self.connector['waiting_knife_end_pos'] = (
            self.connector['throwing_pack_start_pos']
        )
        self.connector['waiting_knife_start_pos'] = (
                self.connector['waiting_knife_end_pos'] +
                self.waiting_knife.get_a_dyn_at_boundary('start', 0) -
                self.waiting_knife.get_a_dyn_at_boundary('end', 0)
        )
        self.connector['shaking_hand_with_clamping_bottom_end_pos'] = (
            self.connector['waiting_knife_start_pos']
        )
        self.connector['shaking_hand_with_clamping_bottom_start_pos'] = (
                self.connector['shaking_hand_with_clamping_bottom_end_pos'] +
                self.shaking_hand_with_clamping_bottom.get_a_dyn_at_boundary(
                    'start', 0) -
                self.shaking_hand_with_clamping_bottom.get_a_dyn_at_boundary(
                    'end', 0)
        )
        self.connector['pulling_tube_end_pos'] = (
            self.connector['shaking_hand_with_clamping_bottom_start_pos']
        )
        self.connector['pulling_tube_start_pos'] = (
                self.connector['pulling_tube_end_pos'] +
                self.pulling_tube.get_a_dyn_at_boundary('start', 0) -
                self.pulling_tube.get_a_dyn_at_boundary('end', 0)
        )
        self.connector['shaking_hand_with_folding_ear_end_pos'] = (
            self.connector['pulling_tube_start_pos']
        )
        self.connector['shaking_hand_with_folding_ear_start_pos'] = (
                self.connector['shaking_hand_with_folding_ear_end_pos'] +
                self.shaking_hand_with_folding_ear.get_a_dyn_at_boundary(
                    'start', 0) -
                self.shaking_hand_with_folding_ear.get_a_dyn_at_boundary(
                    'end', 0)
        )
        self.connector['waiting_lock_end_pos'] = (
            self.connector['shaking_hand_with_folding_ear_start_pos']
        )
        self.connector['waiting_lock_start_pos'] = (
                self.connector['waiting_lock_end_pos'] +
                self.waiting_lock.get_a_dyn_at_boundary('start', 0) -
                self.waiting_lock.get_a_dyn_at_boundary('end', 0)
        )
        self.connector['clamping_bottom_end_pos'] = (
            self.connector['waiting_lock_start_pos']
        )
        self.connector['clamping_bottom_start_pos'] = (
                self.connector['clamping_bottom_end_pos'] +
                self.clamping_bottom.get_a_dyn_at_boundary('start', 0) -
                self.clamping_bottom.get_a_dyn_at_boundary('end', 0)
        )
        self.connector['clamping_bottom_start_vel'] = (
            self.clamping_bottom.get_a_dyn_at_boundary('start', 1)
        )
        self.connector['clamping_bottom_start_acc'] = (
            self.clamping_bottom.get_a_dyn_at_boundary('start', 2)
        )
        self.connector['clamping_bottom_start_jer'] = (
            self.clamping_bottom.get_a_dyn_at_boundary('start', 3)
        )
        self.connector['climbing_back_end_pos'] = (
            self.connector['clamping_bottom_start_pos']
        )
        self.connector['climbing_back_end_vel'] = (
            self.connector['clamping_bottom_start_vel']
        )
        self.connector['climbing_back_end_acc'] = (
            self.connector['clamping_bottom_start_acc']
        )
        self.connector['climbing_back_end_jer'] = (
            self.connector['clamping_bottom_start_jer']
        )
        self.connector['climbing_back_start_acc'] = (
            self.connector['throwing_pack_end_acc']
        )
        self.connector['climbing_back_start_jer'] = (
            self.connector['throwing_pack_end_jer']
        )
        return self.connector


if __name__ == "__main__":
    # joy = JawOnYork(whether_reload=False)
    # joy.plot_symbolically()
    # shake_hand = ShakingHandWithClampingBottom(whether_reload=False)
    # shake_hand.plot_symbolically()
    # print(shake_hand.get_pvajp_at_point(shake_hand.knots[-1]))
    # clamp_bottom = ClampingBottom(whether_reload=True)
    # clamp.plot_one_polynomial_at_one_depth(0,1)
    # clamp.plot_to_depth_of_acceleration()
    # pvajp_touched = clamp_bottom.get_pvajp_at_point(
    #     clamp_bottom.tracing.get_t_touched()
    # )
    # print('pvajp_touched: ', pvajp_touched )
    # climbing_back = ClimbingBack(whether_reload=False)
    # climbing_back.plot_spline_on_subplots()
    # print(climbing_back.get_pvajp_at_point(
    #     climbing_back.tracing.get_t_touched()
    # ))
    # pulling_tube = PullingTube(whether_reload=False)
    # waiting_lock = WaitingLock(whether_reload=False)
    # waiting_knife = WaitingKnife(whether_reload=False)
    # throwing_pack = ThrowingPack(whether_reload=False)
    # throwing_pack.plot_spline_on_subplots()
    stages = StagesConnector(whether_reload=False)
    print(stages.collect_connectors())

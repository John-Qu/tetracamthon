from tetracamthon.helper import trans_degree_to_time, trans_time_to_degree
from tetracamthon.package import Production, Package, Productivity
from tetracamthon.stage import Spline, StagesConnector, ThrowingPack, \
    ClimbingBack, PullingTube, WaitingLock, WaitingKnife, \
    ShakingHandWithClampingBottom, ShakingHandWithFoldingEar, ClampingBottom


class YorkProfile(Spline):
    def __init__(self,
                 machine_production=Production(
                     Package('1000SQ'),
                     Productivity(8000)
                 ),
                 whether_reload=False,
                 ):
        self.name = 'york_profile'
        self.production = machine_production
        self.each_stages = StagesConnector(
            machine_production=self.production,
            whether_reload=False
        )
        self.tracing_of_point_a = self.each_stages.tracing_of_point_a
        self.connector = self.each_stages.collect_connectors()
        self.throwing_pack = ThrowingPack(
            name='stage_of_throwing_pack',
            a_production=self.production,
            whether_reload=whether_reload
        )
        self.waiting_knife = WaitingKnife(
            name='stage_of_waiting_knife',
            a_set_of_informed_knots=(
                self.change_knots_with_info_of_waiting_knife()
            ),
            a_production=self.production,
            whether_reload=whether_reload
        )
        self.shaking_hand_with_clamping_bottom = ShakingHandWithClampingBottom(
            name='stage_of_shaking_hand_with_clamping_bottom',
            a_set_of_informed_knots=(
                self.change_knots_with_info_of_shaking_hand_with_clamping()
            ),
            a_production=self.production,
            whether_reload=whether_reload
        )
        self.pulling_tube = PullingTube(
            name='stage_of_pulling_tube',
            a_set_of_informed_knots=(
                self.change_knots_with_info_of_pulling_tube()
            ),
            a_production=self.production,
            whether_reload=whether_reload
        )
        self.shaking_hand_with_folding_ear = ShakingHandWithFoldingEar(
            name='stage_of_shaking_hand_with_folding_ear',
            a_set_of_informed_knots=(
                self.change_knots_with_info_of_shaking_hand_with_folding_ear()
            ),
            a_production=self.production,
            whether_reload=whether_reload
        )
        self.waiting_lock = WaitingLock(
            name='stage_of_waiting_lock',
            a_set_of_informed_knots=(
                self.change_knots_with_info_of_waiting_lock()
            ),
            a_production=self.production,
            whether_reload=whether_reload
        )
        self.clamping_bottom = ClampingBottom(
            name='stage_of_clamping_bottom',
            a_production=self.production,
            a_spline_of_shake_hand_with_clamping_bottom=(
                self.shaking_hand_with_clamping_bottom
            ),
            a_tracing_of_point_a=self.tracing_of_point_a,
            whether_reload=whether_reload,
        )
        self.climbing_back = ClimbingBack(
            name="stage_of_climbing_back",
            a_set_of_informed_knots=(
                self.change_knots_with_info_of_climbing_back()
            ),
            a_production=self.production,
            whether_reload=whether_reload
        )
        self.stages = [
            self.climbing_back,
            self.clamping_bottom,
            self.waiting_lock,
            self.shaking_hand_with_folding_ear,
            self.pulling_tube,
            self.shaking_hand_with_clamping_bottom,
            self.waiting_knife,
            self.throwing_pack
        ]
        self.knots = self.collect_knots()
        self.num_of_knots = len(self.knots)
        self.pieces_of_polynomial = self.collect_polynomials()
        self.num_of_pieces = len(self.pieces_of_polynomial)

    def change_knots_with_info_of_waiting_knife(self):
        informed_knots = (
            self.each_stages.waiting_knife.informed_knots
        )
        informed_knots.change_boundary_knot_info(
            'end',
            pos=self.connector['waiting_knife_end_pos']
        )
        return informed_knots

    def change_knots_with_info_of_shaking_hand_with_clamping(self):
        informed_knots = (
            self.each_stages.shaking_hand_with_clamping_bottom.informed_knots
        )
        informed_knots.change_boundary_knot_info(
            'end',
            pos=self.connector['shaking_hand_with_clamping_bottom_end_pos']
        )
        return informed_knots

    def change_knots_with_info_of_pulling_tube(self):
        informed_knots = (
            self.each_stages.pulling_tube.informed_knots
        )
        informed_knots.change_boundary_knot_info(
            'end',
            pos=self.connector['pulling_tube_end_pos']
        )
        return informed_knots

    def change_knots_with_info_of_shaking_hand_with_folding_ear(self):
        informed_knots = (
            self.each_stages.shaking_hand_with_folding_ear.informed_knots
        )
        informed_knots.change_boundary_knot_info(
            'end',
            pos=self.connector['shaking_hand_with_folding_ear_end_pos']
        )
        return informed_knots

    def change_knots_with_info_of_waiting_lock(self):
        informed_knots = (
            self.each_stages.waiting_lock.informed_knots
        )
        informed_knots.change_boundary_knot_info(
            'end',
            pos=self.connector['waiting_lock_end_pos']
        )
        return informed_knots
    
    def change_knots_with_info_of_climbing_back(self):
        informed_knots = (
            self.each_stages.climbing_back.informed_knots
        )
        informed_knots.change_boundary_knot_info(
            'end',
            pos=self.connector['climbing_back_end_pos']
        )
        informed_knots.change_boundary_knot_info(
            'end',
            vel=self.connector['climbing_back_end_vel']
        )
        informed_knots.change_boundary_knot_info(
            'end',
            acc=self.connector['climbing_back_end_acc']
        )
        informed_knots.change_boundary_knot_info(
            'end',
            jer=self.connector['climbing_back_end_jer']
        )
        informed_knots.change_boundary_knot_info(
            'start',
            acc=self.connector['climbing_back_start_acc']
        )
        informed_knots.change_boundary_knot_info(
            'start',
            jer=self.connector['climbing_back_start_jer']
        )
        return informed_knots

    def collect_knots(self):
        result = []
        num_of_stages = len(self.stages)
        for i_of_stage in range(num_of_stages):
            informed_knots_in_spline = self.stages[i_of_stage].informed_knots
            num_of_knots = len(informed_knots_in_spline.knots_with_info)
            if i_of_stage < num_of_stages - 1:
                num_of_taken_knots = num_of_knots - 1
            else:
                num_of_taken_knots = num_of_knots
            for i_of_knot in range(num_of_taken_knots):
                knots_with_info = informed_knots_in_spline.knots_with_info
                result.append(knots_with_info[i_of_knot].knot)
        return trans_degree_to_time(result)

    def collect_polynomials(self):
        result = []
        for stage in self.stages:
            pieces_of_polynomial = stage.get_pieces_of_polynomial()
            result.extend(pieces_of_polynomial)
        return result


class JawProfile(Spline):
    def __init__(self):
        pass


if __name__ == "__main__":
    york_profile = YorkProfile(whether_reload=True)
    # york_profile.stages[0].plot_spline_on_subplots(axs_num=4)
    # york_profile.stages[1].plot_spline_on_subplots(axs_num=3)
    # print(york_profile.knots)
    # print(len(york_profile.knots))
    # print(len(york_profile.pieces_of_polynomial))
    york_profile.plot_spline_on_subplots(
        axs_num=4,
        fig_title="York Profile",
        whether_knots_ticks=False,
        ignore_piece_at_depth='13'
    )
    # print(york_profile.stages[-3].informed_knots)
    # clamping_start_knot = york_profile.stages[1].knots[0]
    # print(trans_time_to_degree(clamping_start_knot))
    # clamping_start_pos = york_profile.stages[1].get_pvajp_at_point(
    #     clamping_start_knot, to_depth=1)[0]
    # print(clamping_start_pos)
    # clamping_end_knot = york_profile.stages[1].knots[-1]
    # print(clamping_start_knot)
    # clamping_end_pos = york_profile.stages[1].get_pvajp_at_point(
    #     clamping_end_knot, to_depth=1)[0]
    # print(clamping_end_pos)
    # waiting_lock_start_knot = york_profile.stages[2].knots[0]
    # print(waiting_lock_start_knot)
    # waiting_lock_start_pos = york_profile.stages[2].get_pvajp_at_point(
    #     waiting_lock_start_knot, to_depth=1
    # )[0]
    # print(waiting_lock_start_pos)
    # dif = waiting_lock_start_pos - clamping_end_pos
    # print(dif)

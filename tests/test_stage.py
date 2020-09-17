from tetracamthon.stage import JawOnYork, ShakingHandWithClampingBottom, \
    ShakingHandWithFoldingEar, PullingTube, ClampingBottom
from tetracamthon.polynomial import KnotsInSpline
from tetracamthon.helper import trans_degree_to_time


def test_jaw_on_york_init():
    an_jaw_on_york_spline = JawOnYork(
        name="O4_to_O2_spline_with_nine_knots",
        informed_knots=KnotsInSpline(
            knots_info_csv="/Users/johnqu/PycharmProjects/"
                           "tetracamthon/src/tetracamthon/knot_info/"
                           "jaw_on_york_with_nine_knots.csv"
        ),
        whether_reload=False,
    )
    assert len(
        an_jaw_on_york_spline.get_interpolating_condition_equations()) == 12
    assert len(
        an_jaw_on_york_spline.get_smoothness_condition_equations()) == 30
    assert len(
        an_jaw_on_york_spline.get_periodic_condition_equations()) == 6
    assert "C_01" in str(an_jaw_on_york_spline.get_total_equations())


def test_plot_an_jaw_on_york_spline_with_nine_knots(
        an_jaw_on_york_spline_with_nine_knots):
    an_jaw_on_york_spline_with_nine_knots.plot_symbolically()
    assert True


def test_plot_an_jaw_on_york_spline_with_minimum_five_knots(
        an_jaw_on_york_spline_with_minimum_five_knots
):
    an_jaw_on_york_spline_with_minimum_five_knots.plot_symbolically(
        whether_save_png=True)
    assert True


def test_plot_an_jaw_on_york_spline_with_trying_knots(
        an_jaw_on_york_spline_with_trying_knots
):
    an_jaw_on_york_spline_with_trying_knots.plot_symbolically(
        whether_save_png=True)
    assert True


def test_plot_shaking_hand_with_clamping_bottom_symbolically():
    sel = ShakingHandWithClampingBottom()
    print('\n', sel.informed_knots.knots_with_info[0])
    print(sel.informed_knots.knots_with_info[-1])
    sel.plot_symbolically()
    # "![](https://tva1.sinaimg.cn/large/007S8ZIlly1gin0xkbum1j30u00yjk3u.jpg)"


def test_plot_shaking_hand_with_folding_ear_symbolically():
    sel = ShakingHandWithFoldingEar()
    print('\n', sel.informed_knots.knots_with_info[0])
    print(sel.informed_knots.knots_with_info[-1])
    sel.plot_symbolically()


def test_pulling():
    sel = PullingTube()
    print('\n', sel.informed_knots.knots_with_info[0])
    print(sel.informed_knots.knots_with_info[-1])
    sel.plot_spline_on_subplots(
        whether_save_png=False,
        whether_show_figure=True,
        whether_knots_ticks=True,
        whether_annotate=False,
    )


def test_modify_pieces():
    sel = ClampingBottom()
    sel.modify_pieces()
    print(sel.get_pvajp_at_point(trans_degree_to_time(82)))
    print(sel.get_pvajp_at_point(trans_degree_to_time(137)))
    # sel.plot_spline_on_subplots(
    #     whether_annotate=False
    # )
    print("OK")

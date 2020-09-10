from tetracamthon.stage import JawToYork
from tetracamthon.polynomial import KnotsInSpline


def test_jaw_on_york_init():
    an_jaw_on_york_spline = JawToYork(
        name="O4_to_O2_spline_with_nine_knots",
        a_set_of_informed_knots=KnotsInSpline(
            path_to_knots_csv="/Users/johnqu/PycharmProjects/"
                              "Tetracamthon/src/tetracamthon/" 
                              "knots_of_o4o2_with_nine_knots.csv"
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
        an_jaw_on_york_spline_with_minimum_five_knots):
    an_jaw_on_york_spline_with_minimum_five_knots.plot_symbolically(
        whether_save_png=True)
    assert True

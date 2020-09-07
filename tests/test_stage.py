from tetracamthon.stage import O4O2
from tetracamthon.polynomial import KnotsInSpline


def test_o4o2():
    an_o4o2_spline = O4O2(
        name="O4_to_O2_spline_with_nine_knots",
        a_set_of_informed_knots=KnotsInSpline(
            path_to_csv="/src/tetracamthon/knots_of_o4o2_with_nine_knots.csv"
        ),
        whether_reload=False,
    )
    assert len(an_o4o2_spline.get_interpolating_condition_equations()) == 12
    assert len(an_o4o2_spline.get_smoothness_condition_equations()) == 30
    assert len(an_o4o2_spline.get_periodic_condition_equations()) == 6
    assert "C_01" in str(an_o4o2_spline.get_total_equations())


def test_plot_an_o4o2_spline_with_nine_knots(an_o4o2_spline_with_nine_knots):
    an_o4o2_spline_with_nine_knots.plot()
    assert True


def test_plot_an_o4o2_spline_with_minimum_five_knots(
        an_o4o2_spline_with_minimum_five_knots):
    an_o4o2_spline_with_minimum_five_knots.plot(whether_save_png=False)
    assert True

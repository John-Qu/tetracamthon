from tetracamthon.stage import O4O2
from tetracamthon.polynomial import KnotsInSpline


def test_o4o2():
    an_o4o2_spline = O4O2(
        name="O4_to_O2_spline_for_test",
        max_order=6,
        a_set_of_informed_knots=KnotsInSpline(
            path_to_csv="/Users/johnqu/PycharmProjects/Tetracamthon/"
                        "src/tetracamthon/knots_of_o4o2.csv"
        ),
        whether_reload=False,
    )
    assert len(an_o4o2_spline.get_interpolating_condition_equations()) == 12
    assert len(an_o4o2_spline.get_smoothness_condition_equations()) == 30
    assert len(an_o4o2_spline.get_periodic_condition_equations()) == 6
    assert "C_01" in str(an_o4o2_spline.get_total_equations())


def test_plot(an_o4o2_spline):
    an_o4o2_spline.plot()
    assert True

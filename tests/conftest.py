import pytest
from sympy import symbols
from tetracamthon.mechanism import Forward, Backward, SlideRocker
from tetracamthon.polynomial import Polynomial, KnotsInSpline, \
    Spline
from tetracamthon.stage import JawOnYork, TracingOfPointA
from tetracamthon.package import Package, Productivity, Production


@pytest.fixture(scope='session')
def path_to_tetra_pak_a3_flex_cam_acc_data_721_csv():
    """Return a path to a cvs file for testing."""
    return "/Users/johnqu/PycharmProjects/Tetracamthon/src" + \
           "/a3flex/tetra_pak_a3_flex_cam_acc_data_721.csv"


@pytest.fixture(scope='session')
def a_slide_rocker_of_compact_flex():
    sr = SlideRocker(name="SlideRocker",
                     a_spec_id="compact_flex",
                     path_to_link_dim_csv="/Users/johnqu/PycharmProjects"
                                          "/Tetracamthon/src/tetracamthon/"
                                          "tetracamthon_lind_dimensions.csv")
    return sr


@pytest.fixture(scope='session')
def a_forward_slide_rocker_of_compact_flex():
    fw = Forward(name="Forward", a_spec_id="compact_flex",
                 path_to_link_dim_csv="/Users/johnqu/PycharmProjects/"
                                      "Tetracamthon/src/tetracamthon/"
                                      "tetracamthon_lind_dimensions.csv")
    return fw


@pytest.fixture(scope='session')
def a_backward_slide_rocker_of_compact_flex():
    bw = Backward(name="Backward",
                  a_spec_id="compact_flex",
                  path_to_link_dim_csv="/Users/johnqu/PycharmProjects/"
                                       "Tetracamthon/src/tetracamthon/"
                                       "tetracamthon_lind_dimensions.csv")
    return bw


@pytest.fixture(scope='session')
def a_polynomial():
    result = Polynomial(max_order=6, piece_id=0, start_time=1)
    return result


@pytest.fixture(scope='session')
def a_solution():
    return {
        symbols("C_00"): 1,
        symbols("C_01"): 2,
        symbols("C_02"): 3,
        symbols("C_03"): 4,
        symbols("C_04"): 5,
        symbols("C_05"): 6
    }


@pytest.fixture(scope='session')
def a_sample_knots_in_spline():
    return KnotsInSpline(knots_info_csv="/Users/johnqu/PycharmProjects/"
                                        "Tetracamthon/data/"
                                        "sample_knots.csv")


@pytest.fixture(scope='session')
def a_sample_spline(a_sample_knots_in_spline):
    return Spline(a_set_of_informed_knots=a_sample_knots_in_spline,
                  name="a_sample_spline_with_four_knots",
                  whether_trans_knots_degree_to_time=False)


@pytest.fixture(scope='session')
def a_sample_spline_reloaded(a_sample_knots_in_spline):
    return Spline(a_set_of_informed_knots=a_sample_knots_in_spline,
                  name="a_sample_spline_with_four_knots",
                  whether_reload=False,
                  whether_trans_knots_degree_to_time=False)


@pytest.fixture(scope='session')
def an_jaw_on_york_spline_with_nine_knots():
    return JawOnYork(
        name="O4_to_O2_Spline",
        informed_knots=KnotsInSpline(
            knots_info_csv="/Users/johnqu/PycharmProjects/"
                           "Tetracamthon/src/tetracamthon/knot_info/"
                           "jaw_on_york_with_nine_knots.csv"
        ),
        whether_reload=False,
    )


@pytest.fixture(scope='session')
def an_jaw_on_york_spline_with_minimum_five_knots():
    return JawOnYork(
        name="jaw_on_york_Spline",
        informed_knots=KnotsInSpline(
            knots_info_csv="/Users/johnqu/PycharmProjects/"
                           "Tetracamthon/src/tetracamthon/knot_info/"
                           "jaw_on_york_with_minimum_five_knots.csv"
        ),
        whether_reload=False,
    )


@pytest.fixture(scope='session')
def an_jaw_on_york_spline_with_trying_knots():
    return JawOnYork(
        name="jaw_on_york_Spline",
        informed_knots=KnotsInSpline(
            knots_info_csv="/Users/johnqu/PycharmProjects/"
                           "Tetracamthon/src/tetracamthon/knot_info/"
                           "jaw_on_york_with_trying_knots.csv"
        ),
        whether_reload=False,
    )


@pytest.fixture(scope='session')
def a_tracing_of_point_a_with_330sq_dim():
    result = TracingOfPointA(
        a_jaw_on_york_spline=JawOnYork(),
        name="a_tracing_of_point_a_with_five_knots_o4o2_spline",
        a_spec_id="compact_flex",
        a_package_id='330SQ',
        a_path_to_link_dim_csv='/Users/johnqu/PycharmProjects/'
                               'Tetracamthon/src/tetracamthon/knot_info/'
                               'tetracamthon_lind_dimensions.csv',
        whether_reload=False,
        # whether_reload=True,
    )
    return result


@pytest.fixture(scope='class')
def a_tracing_of_point_a_with_1000sq_dim():
    result = TracingOfPointA(
        a_jaw_on_york_spline=JawOnYork(whether_reload=True),
        name="a_tracing_of_point_a_with_five_knots_o4o2_spline",
        a_spec_id="flex",
        a_package_id='1000SQ',
        a_path_to_link_dim_csv='/Users/johnqu/PycharmProjects/'
                               'Tetracamthon/src/tetracamthon/'
                               'tetracamthon_lind_dimensions.csv',
        whether_reload=False,
        # whether_reload=True,
    )
    return result


@pytest.fixture(scope='class')
def a_1000sq_package():
    result = Package("1000SQ")
    return result


@pytest.fixture(scope='class')
def a_330sq_package():
    result = Package("330SQ")
    return result


@pytest.fixture(scope='class')
def a_production_of_1000sq_8000pph():
    package_1000sq = Package("1000SQ")
    productivity_8000 = Productivity(8000)
    result = Production(package_1000sq, productivity_8000)
    return result


@pytest.fixture(scope='class')
def a_production_of_330sq_8000pph():
    package_1000sq = Package("330SQ")
    productivity_8000 = Productivity(8000)
    result = Production(package_1000sq, productivity_8000)
    return result

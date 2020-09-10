import pytest
from sympy import symbols
from tetracamthon.mechanism import Forward, Backward, SlideRocker, \
    TracingOfPointA
from tetracamthon.polynomial import Polynomial, KnotPVAJP, KnotsInSpline, \
    Spline
from tetracamthon.stage import JawToYork


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
    return KnotsInSpline(path_to_knots_csv="/Users/johnqu/PycharmProjects/"
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
    return JawToYork(
        name="O4_to_O2_Spline",
        a_set_of_informed_knots=KnotsInSpline(
            path_to_knots_csv="/Users/johnqu/PycharmProjects/"
                              "Tetracamthon/src/tetracamthon/"
                              "knots_of_o4o2_with_nine_knots.csv"
        ),
        whether_reload=False,
    )


@pytest.fixture(scope='session')
def an_jaw_on_york_spline_with_minimum_five_knots():
    return JawToYork(
        name="jaw_on_york_Spline",
        a_set_of_informed_knots=KnotsInSpline(
            path_to_knots_csv="/Users/johnqu/PycharmProjects/"
                              "Tetracamthon/src/tetracamthon/"
                              "knots_of_o4o2_with_minimum_five_knots.csv"
        ),
        whether_reload=False,
    )


@pytest.fixture(scope='session')
def a_tracing_of_point_a_with_five_knots_jaw_on_york_spline_of_flex_dim():
    result = TracingOfPointA(
        name="a_tracing_of_point_a_with_five_knots_o4o2_spline",
        a_spec_id="flex",
        a_path_to_link_dim_csv='/Users/johnqu/PycharmProjects/'
                               'Tetracamthon/src/tetracamthon/'
                               'tetracamthon_lind_dimensions.csv',
        # whether_reload=False,
        whether_reload=True,
    )
    return result

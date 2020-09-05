import pytest
from sympy import symbols
from tetracamthon.mechanism import Forward, Backward, SlideRocker
from tetracamthon.polynomial import Polynomial, KnotPVAJP, KnotsInSpline, \
    Spline



@pytest.fixture(scope='session')
def path_to_csv():
    """Return a path to a cvs file for testing."""
    return "/Users/johnqu/PycharmProjects/Tetracamthon/src" + \
           "/a3flex/tetra_pak_a3_flex_cam_acc_data_721.csv"


@pytest.fixture(scope='session')
def a_slide_rocker():
    sr = SlideRocker(name="SlideRocker",
                     a_spec_id=1,
                     path_to_csv="/Users/johnqu/PycharmProjects/Tetracamthon/"
                                 "src/tetracamthon/"
                                 "tetracamthon_lind_dimensions.csv")
    return sr


@pytest.fixture(scope='session')
def a_forward():
    fw = Forward(name="Forward",
                 a_spec_id=1,
                 path_to_csv="/Users/johnqu/PycharmProjects/Tetracamthon/"
                             "src/tetracamthon/"
                             "tetracamthon_lind_dimensions.csv")
    return fw


@pytest.fixture(scope='session')
def a_backward():
    bw = Backward(name="Backward",
                  a_spec_id=1,
                  path_to_csv="/Users/johnqu/PycharmProjects/Tetracamthon/"
                              "src/tetracamthon/"
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
def a_set_of_knot_pvajp():
    start = KnotPVAJP(knot=0,
                      pvajp=(
                          0,
                          0,
                          0,
                          None,
                          None,
                      ),
                      smooth_depth=6)
    knot1 = KnotPVAJP(knot=1,
                      pvajp=(
                          0.3,
                          None,
                          None,
                          None,
                          None,
                      ),
                      smooth_depth=6)
    knot2 = KnotPVAJP(knot=2,
                      pvajp=(
                          0.6,
                          None,
                          None,
                          None,
                          None,
                      ),
                      smooth_depth=6)
    end = KnotPVAJP(knot=3,
                    pvajp=(
                        1,
                        0,
                        0,
                        None,
                        None,
                    ),
                    smooth_depth=6)
    return [start, knot1, knot2, end]


@pytest.fixture(scope='session')
def a_sample_knots_in_spline():
    return KnotsInSpline(path_to_csv="/Users/johnqu/PycharmProjects/"
                                     "Tetracamthon/data/sample_knots.csv")


@pytest.fixture(scope='session')
def a_spline(a_sample_knots_in_spline):
    return Spline(max_order=6,
                  a_set_of_informed_knots=a_sample_knots_in_spline,
                  name="TestSpline")

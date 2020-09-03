import pytest
from tetracamthon.mechanism import Forward, Backward


@pytest.fixture(scope='session')
def path_to_csv():
    """Return a path to a cvs file for testing."""
    return "/Users/johnqu/PycharmProjects/Tetracamthon/src" + \
           "/a3flex/tetra_pak_a3_flex_cam_acc_data_721.csv"


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

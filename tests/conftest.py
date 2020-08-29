import pytest


@pytest.fixture(scope='session')
def path_to_csv():
    """Return a path to a cvs file for testing."""
    return "/Users/johnqu/PycharmProjects/Tetracamthon/src" + \
           "/a3flex/tetra_pak_a3_flex_cam_acc_data_721.csv"

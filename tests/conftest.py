import pytest


@pytest.fixture()
def path_to_a_cvs_file():
    """Return a path to a cvs file for testing."""
    return "../src/tetra_pak_a3_flex_cam" \
           "/tetra_pak_a3_flex_cam_acc_raw_data_360.csv"



"""Test reading and drawing the cvs raw data."""
from tetra_pak_a3_flex_cam.read_raw_data import get_csv_data
import numpy

def test_get_cvs_data(path_to_a_cvs_file):
    """Test whether the data is properly got.
    """
    data = get_csv_data(path_to_a_cvs_file)
    assert len(data) == 3
    assert len(data[0]) == 361
    assert len(data[1]) == 361
    assert len(data[2]) == 361
    assert isinstance(data[0][5], numpy.int64)
    assert isinstance(data[1][5], numpy.float64)
    assert isinstance(data[2][5], numpy.float64)

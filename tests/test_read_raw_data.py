from tetra_pak_a3_flex_cam.read_data import TetraPakA3AccMeasured


def test_read_in_csv_data(path_to_a_cvs_file):
    a_set_of_TetraPakA3AccMeasured = TetraPakA3AccMeasured(path_to_a_cvs_file)
    assert len(a_set_of_TetraPakA3AccMeasured.machine_degree) == len(
        a_set_of_TetraPakA3AccMeasured.york_acc)
    assert len(a_set_of_TetraPakA3AccMeasured.york_acc) == len(
        a_set_of_TetraPakA3AccMeasured.jaw_acc)
    assert len(a_set_of_TetraPakA3AccMeasured.machine_degree) != 0


def test_adjust_a_little_as_a_whole():
    assert False


def test_meet_york_jaw_there():
    assert False


def test_become_zeroes_there():
    assert False

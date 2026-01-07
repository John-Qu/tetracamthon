import pytest
from pathlib import Path
from tetracamthon.stage import JawOnYork, TracingOfPointA
from tetracamthon.polynomial import KnotsInSpline
from tetracamthon.package import Package, Productivity, Production

@pytest.fixture(scope="session")
def project_root() -> Path:
    return Path(__file__).resolve().parents[3]

@pytest.fixture(scope="session")
def src_path(project_root) -> Path:
    return project_root / "src"

@pytest.fixture(scope="session")
def data_path(project_root) -> Path:
    return project_root / "data"

@pytest.fixture(scope="session")
def cam_acc_csv(project_root: Path) -> Path:
    return project_root / "src" / "a3flex" / "tetra_pak_a3_flex_cam_acc_data_721.csv"

@pytest.fixture(scope="session")
def knot_info_dir(project_root: Path) -> Path:
    return project_root / "src" / "tetracamthon" / "knot_info"

@pytest.fixture(scope='session')
def path_to_tetra_pak_a3_flex_cam_acc_data_721_csv() -> str:
    return str((Path(__file__).resolve().parents[3] /
                "src" / "a3flex" / "tetra_pak_a3_flex_cam_acc_data_721.csv").resolve())

@pytest.fixture(scope='session')
def an_jaw_on_york_spline_with_nine_knots():
    return JawOnYork(
        name="O4_to_O2_Spline",
        informed_knots=KnotsInSpline(
            knots_info_csv=str(
                Path(__file__).resolve().parents[3] /
                "src" / "tetracamthon" / "knot_info" /
                "jaw_on_york_with_nine_knots.csv"
            )
        ),
        whether_reload=False,
    )

@pytest.fixture(scope='session')
def an_jaw_on_york_spline_with_minimum_five_knots():
    return JawOnYork(
        name="jaw_on_york_Spline",
        informed_knots=KnotsInSpline(
            knots_info_csv=str(
                Path(__file__).resolve().parents[3] /
                "src" / "tetracamthon" / "knot_info" /
                "jaw_on_york_with_five_knots.csv"
            )
        ),
        whether_reload=False,
    )

@pytest.fixture(scope='session')
def an_jaw_on_york_spline_with_trying_knots():
    return JawOnYork(
        name="jaw_on_york_Spline",
        informed_knots=KnotsInSpline(
            knots_info_csv=str(
                Path(__file__).resolve().parents[3] /
                "src" / "tetracamthon" / "knot_info" /
                "jaw_on_york_with_trying_knots.csv"
            )
        ),
        whether_reload=False,
    )

@pytest.fixture(scope='session')
def a_1000sq_package():
    return Package("1000SQ")

@pytest.fixture(scope='session')
def a_330sq_package():
    return Package("330SQ")

@pytest.fixture(scope='class')
def a_production_of_1000sq_8000pph():
    package_1000sq = Package("1000SQ")
    productivity_8000 = Productivity(8000)
    return Production(package_1000sq, productivity_8000)

@pytest.fixture(scope='class')
def a_production_of_330sq_8000pph():
    package_330sq = Package("330SQ")
    productivity_8000 = Productivity(8000)
    return Production(package_330sq, productivity_8000)

@pytest.fixture(scope='session')
def a_tracing_of_point_a_with_330sq_dim():
    return TracingOfPointA(
        a_jaw_on_york_spline=JawOnYork(),
        name="a_tracing_of_point_a_with_five_knots_o4o2_spline",
        a_spec_id="compact_flex",
        a_package_id='330SQ',
        a_path_to_link_dim_csv=str(
            Path(__file__).resolve().parents[3] /
            'src' / 'tetracamthon' / 'tetracamthon_lind_dimensions.csv'
        ),
        whether_reload=False,
    )

@pytest.fixture(scope='class')
def a_tracing_of_point_a_with_1000sq_dim():
    return TracingOfPointA(
        a_jaw_on_york_spline=JawOnYork(whether_reload=True),
        name="a_tracing_of_point_a_with_five_knots_o4o2_spline",
        a_spec_id="flex",
        a_package_id='1000SQ',
        a_path_to_link_dim_csv=str(
            Path(__file__).resolve().parents[3] /
            'src' / 'tetracamthon' / 'tetracamthon_lind_dimensions.csv'
        ),
        whether_reload=False,
    )

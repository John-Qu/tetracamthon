import pytest
from pathlib import Path

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

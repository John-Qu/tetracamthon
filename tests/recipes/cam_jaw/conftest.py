import pytest
from pathlib import Path

@pytest.fixture(scope="session")
def cam_acc_csv(project_root: Path) -> Path:
    return project_root / "src" / "a3flex" / "tetra_pak_a3_flex_cam_acc_data_721.csv"

@pytest.fixture(scope="session")
def knot_info_dir(project_root: Path) -> Path:
    return project_root / "src" / "tetracamthon" / "knot_info"
import pytest
from pathlib import Path

@pytest.fixture(scope="session")
def project_root() -> Path:
    return Path(__file__).resolve().parents[2]

@pytest.fixture(scope="session")
def src_path(project_root) -> Path:
    return project_root / "src"

@pytest.fixture(scope="session")
def data_path(project_root) -> Path:
    return project_root / "data"
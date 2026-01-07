import pytest

@pytest.fixture(scope="session")
def servo_limits():
    return {
        "v_max": 1.0,
        "a_max": 10.0,
        "j_max": 100.0,
        "tau_max": 2.0,
    }

@pytest.fixture(scope="session")
def solver_config():
    return {"method": "SLSQP", "maxiter": 500, "tol": 1e-6}
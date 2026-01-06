import sys
import os
from pathlib import Path
cache_dir = Path(__file__).resolve().parents[1] / ".mplcache"
cache_dir.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(cache_dir))
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))
from tetracamthon.polynomial_spline import SplineWithPiecewisePolynomial

def main():
    s = SplineWithPiecewisePolynomial(name="practice_2_spline")
    s.update_with_solution()
    print(s.get_start_pvaj())
    print(s.get_end_pvaj())

if __name__ == "__main__":
    main()

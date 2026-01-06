import sys
import os
from pathlib import Path
cache_dir = Path(__file__).resolve().parents[1] / ".mplcache"
cache_dir.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(cache_dir))
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))
from tetracamthon.polynomial import KnotsInSpline, Spline

def main():
    knots_csv = str(Path(__file__).resolve().parents[1] / "data" / "sample_knots.csv")
    informed_knots = KnotsInSpline(knots_info_csv=knots_csv)
    s = Spline(name="practice_3_polynomial", a_set_of_informed_knots=informed_knots)
    s.solve_spline_pieces()
    print(s.get_pvajp_at_point(s.knots[0], to_depth=4))
    print(s.get_pvajp_at_point(s.knots[-1], to_depth=4))

if __name__ == "__main__":
    main()

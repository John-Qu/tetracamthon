import sys
import os
from pathlib import Path
cache_dir = Path(__file__).resolve().parents[1] / ".mplcache"
cache_dir.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(cache_dir))
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))
from tetracamthon.mechanism import Forward, Backward
from tetracamthon.package import Package

def main():
    link_csv = str(Path(__file__).resolve().parents[1] / "src" / "tetracamthon" / "tetracamthon_lind_dimensions.csv")
    fwd = Forward("Forward", "compact_flex", link_csv)
    bwd = Backward("Backward", "compact_flex", link_csv)
    pkg = Package("1000SQ")
    r_closed = bwd.get_r_O4O2_of_x_AO2().subs(bwd.lAO2.x.sym, -1.5 / 2)
    r_touched = bwd.get_r_O4O2_of_x_AO2().subs(bwd.lAO2.x.sym, -pkg.depth / 2)
    y_expr = fwd.get_y_AO2_of_r_O4O2()
    print(y_expr.subs(fwd.lO4O2.r.sym, r_closed))
    print(y_expr.subs(fwd.lO4O2.r.sym, r_touched))

if __name__ == "__main__":
    main()

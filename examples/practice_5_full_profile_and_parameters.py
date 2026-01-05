import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))
from tetracamthon.profile import YorkProfile
from tetracamthon.package import Production, Package, Productivity

def main():
    production = Production(Package("1000SQ"), Productivity(8000))
    yp = YorkProfile(machine_production=production, whether_reload=True)
    print(len(yp.knots))
    print(len(yp.pieces_of_polynomial))
    print(yp.connector["clamping_bottom_start_pos"])
    print(yp.connector["throwing_pack_end_acc"])

if __name__ == "__main__":
    main()


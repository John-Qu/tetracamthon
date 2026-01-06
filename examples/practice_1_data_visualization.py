import sys
import os
from pathlib import Path
cache_dir = Path(__file__).resolve().parents[1] / ".mplcache"
cache_dir.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(cache_dir))
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))
from a3flex.draw_data import plot_dynamic_subplots

def main():
    csv_path = str(Path(__file__).resolve().parents[1] / "src" / "a3flex" / "tetra_pak_a3_flex_cam_acc_data_721.csv")
    save_path = str(Path(__file__).resolve().parents[1] / "plots" / "practice1_pvaj_721.png")
    plot_dynamic_subplots(path_to_csv=csv_path, save_to=save_path)

if __name__ == "__main__":
    main()

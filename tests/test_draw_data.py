from a3flex.draw_data import plot_dynamic_subplots
from matplotlib import pyplot as plt


def test_plot_dynamic_subplots(path_to_csv):
    plot_dynamic_subplots(
        path_to_csv=path_to_csv,
        # if_annotate=False,
        # saved_name="/Users/johnqu/PycharmProjects/Tetracamthon/tests"
        #            "/tested_Tetra_Pak_A3_flex_Curves_with_721_points.png"
    )
    plt.show()

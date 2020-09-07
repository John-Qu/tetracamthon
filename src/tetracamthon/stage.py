from tetracamthon.polynomial import Spline, KnotsInSpline
from tetracamthon.helper import plot_subplots_on_one_figure


class O4O2(Spline):
    def __init__(self,
                 name="O4_to_O2_spline",
                 a_set_of_informed_knots=KnotsInSpline(
                     path_to_csv="/Users/johnqu/PycharmProjects/Tetracamthon/"
                                 "src/tetracamthon/knots_of_o4o2.csv"
                 ),
                 whether_reload=False,
                 ):
        Spline.__init__(self,
                        name=name,
                        a_set_of_informed_knots=a_set_of_informed_knots,
                        whether_reload=whether_reload,
                        )
        self.a_set_of_informed_knots = a_set_of_informed_knots

    def plot(self):
        name = self.name + "\n" + str(self.a_set_of_informed_knots)
        plot_subplots_on_one_figure(
            self.prepare_plots_for_plt(),
            self.knots,
            name=name,
            whether_save_png=False,
            whether_show_figure=True,
            whether_knots_ticks=True,
        )

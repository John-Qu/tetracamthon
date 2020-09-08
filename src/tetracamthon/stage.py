from tetracamthon.polynomial import Spline, KnotsInSpline


class O4O2(Spline):
    def __init__(self,
                 name="O4_to_O2_spline",
                 a_set_of_informed_knots=KnotsInSpline(
                     # path_to_csv="/src/tetracamthon/knots_of_o4o2_with_minimum_five_knots.csv"
                     path_to_csv="/Users/johnqu/PycharmProjects/Tetracamthon/"
                                 "src/tetracamthon/"
                                 "knots_of_o4o2_with_minimum_five_knots.csv"
                 ),
                 whether_reload=False,
                 ):
        Spline.__init__(self,
                        name=name,
                        a_set_of_informed_knots=a_set_of_informed_knots,
                        whether_reload=whether_reload,
                        )
        self.a_set_of_informed_knots = a_set_of_informed_knots

    def plot_symbolically(self, whether_save_png=False):
        self.plot_spline_on_subplots(
            whether_save_png=whether_save_png,
            whether_show_figure=True,
            whether_knots_ticks=True,
            whether_annotate=True,
        )

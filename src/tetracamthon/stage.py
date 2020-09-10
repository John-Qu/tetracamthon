from tetracamthon.polynomial import Spline, KnotsInSpline


class JawToYork(Spline):
    def __init__(self,
                 name="Jaw_to_York_spline",
                 a_set_of_informed_knots=KnotsInSpline(
                     path_to_knots_csv="/Users/johnqu/PycharmProjects/"
                                       "Tetracamthon/src/tetracamthon/"
                                       "knots_of_o4o2_"
                                       "with_minimum_five_knots.csv"
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


class ShakingHandWithTouching(Spline):
    def __init__(self,
                 name="Shaking_hand_with_touching_spline",
                 a_set_of_informed_knots=KnotsInSpline(
                     path_to_knots_csv="/Users/johnqu/PycharmProjects/"
                                       "Tetracamthon/src/tetracamthon/"
                                       "knots_of_shaking_hand_"
                                       "with_touching.csv"
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


class Touching(Spline):
    def __init__(self,
                 name="Touching_spline",
                 a_set_of_informed_knots=KnotsInSpline(
                     path_to_knots_csv="/Users/johnqu/PycharmProjects/"
                                       "Tetracamthon/src/tetracamthon/"
                                       "knots_of_o4o2_"
                                       "with_minimum_five_knots.csv"
                 ),
                 whether_reload=False,
                 ):
        Spline.__init__(self,
                        name=name,
                        a_set_of_informed_knots=a_set_of_informed_knots,
                        whether_reload=whether_reload,
                        )
        self.a_set_of_informed_knots = a_set_of_informed_knots

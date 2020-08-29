import matplotlib.pyplot as plt
import numpy as np
from math import sqrt
from tetra_pak_a3_flex_cam.read_data import \
    AllLinksWithDynData, \
    RightYork, RightJaw, LeftYork, LeftJaw, RightJawToYork, LeftJawToYork


class CurveStyle(object):
    def __init__(self, a_dyn_data):
        color = ('blue', 'green', 'blue', 'green', 'red', 'red')
        line_width = (3.0, 3.0, 1.0, 1.0, 3.0, 1.0)
        line_style = ("-", "-", "--", "--", "-", "--")
        label = ("Right York", "Right Jaw", "Left York", "Left Jaw",
                 "Right Jaw to York", "Left Jaw to York")
        i = [RightYork, RightJaw, LeftYork, LeftJaw,
             RightJawToYork, LeftJawToYork].index(type(a_dyn_data))
        self.color = color[i]
        self.line_width = line_width[i]
        self.line_style = line_style[i]
        self.label = label[i]
        self.font_size = 12


class Annotation(CurveStyle):
    def __init__(self, a_dyn_data):
        CurveStyle.__init__(self, a_dyn_data)
        self.a_link = a_dyn_data

    def mark_peak_point(self,
                        index_in_pvaj,
                        max_or_min,
                        scope,
                        indicator,
                        place=(30, 30),
                        mark_size=50,
                        font_size=12):
        a = self.a_link.pvaj_data[index_in_pvaj]
        if max_or_min == "max":
            f = np.argmax
        elif max_or_min == "min":
            f = np.argmin
        else:
            raise IndexError
        from_i = self.a_link.m_deg.index(scope[0])
        to_i = self.a_link.m_deg.index(scope[1])
        index = f(a[from_i:to_i]) + from_i
        self.scatter_and_annotate(a, font_size, index, indicator,
                                  mark_size, place)

    def mark_zero_point(self,
                        index_in_pvaj,
                        scope,
                        indicator,
                        step=1,
                        place=(30, 30),
                        mark_size=50,
                        font_size=12):
        a = self.a_link.pvaj_data[index_in_pvaj]
        from_i = self.a_link.m_deg.index(scope[0])
        to_i = self.a_link.m_deg.index(scope[1])
        index = np.argmin(np.abs(a[from_i:to_i:step])) * step + from_i
        self.scatter_and_annotate(a, font_size, index, indicator,
                                  mark_size, place)

    def scatter_and_annotate(self, a, font_size, index, indicator, mark_size,
                             place):
        degree = index / 2
        plt.scatter([degree, ], [a[index], ], mark_size,
                    color=self.color)
        plt.annotate(indicator +
                     "(" + str(degree) + ', ' + str(round(a[index], 1)) + ")",
                     xy=(degree, a[index]), xycoords='data',
                     xytext=place,
                     textcoords='offset points',
                     fontsize=font_size,
                     arrowprops=dict(arrowstyle="->",
                                     connectionstyle="arc3,rad=.2"))


class SupPlotStyle(object):
    def __init__(self, num_row=4, num_col=1, position=1, grid_on=True):
        self.num_row = num_row
        self.num_col = num_col
        self.position = position
        self.grid_on = grid_on


class SuperPlot(object):
    def __init__(self, fig_size=(15, 12), dpi=80):
        self.fig = plt.figure(figsize=fig_size, dpi=dpi)
        self.set_super_title()

    def set_super_title(self,
                        title='Tetra Pak A3 Flex @ 8000 p/h \n York and Jaw'
                              ' PVAJ curves @ 0.9s/cycle',
                        font_size='xx-large'):
        self.fig.suptitle(title, fontsize=font_size)

    def get_fig_handle(self):
        return self.fig


class SubPlot(object):
    def __init__(self, index):
        self.index = index
        self.x_label = "Machine Degrees"
        self.y_label = ("Position and Distance (mm)",
                        "Velocity (mm/s)",
                        "Acceleration (m/s^2)",
                        "Jerk (m/s^3)"
                        )[self.index]
        self.sub_plot_style = (SupPlotStyle(4, 1, 1, True),
                               SupPlotStyle(4, 1, 2, True),
                               SupPlotStyle(4, 1, 3, True),
                               SupPlotStyle(4, 1, 4, True)
                               )[self.index]
        self.axes = self.set_subplots()
        self.set_grid_for_subplot()

    def set_subplots(self):
        return plt.subplot(self.sub_plot_style.num_row,
                           self.sub_plot_style.num_col,
                           self.sub_plot_style.position)

    def set_grid_for_subplot(self):
        plt.grid(self.sub_plot_style.grid_on)

    def set_y_label(self):
        plt.ylabel(self.y_label)

    def set_x_label(self):
        plt.xlabel(self.x_label)


def plt_plot(a_dyn_data, index_of_pvaj):
    style = CurveStyle(a_dyn_data)
    plt.plot(a_dyn_data.m_deg, a_dyn_data.pvaj_data[index_of_pvaj],
             color=style.color,
             linewidth=style.line_width,
             linestyle=style.line_style,
             label=style.label)


class SubPvajPlot(SubPlot):
    def __init__(self, index_in_pvaj, an_all_links_with_dyn_data,
                 if_has_left_links=True):
        self.index = index_in_pvaj
        SubPlot.__init__(self, self.index)
        self.an_all_links = an_all_links_with_dyn_data
        self.position_of_subplots = self.index + 1
        self.if_has_left_links = if_has_left_links

    def plot_a_dynamic_data(self, index_of_link, index_of_pvaj):
        plt_plot(self.an_all_links.links[index_of_link], index_of_pvaj)

    def plot_dynamic_curves_on_one_subplot(self, index_of_pvaj):
        if self.if_has_left_links:
            for index_of_link in (1, 2, 0, 4, 5, 3):
                self.plot_a_dynamic_data(index_of_link, index_of_pvaj)
        else:
            for index_of_link in (1, 2, 0):
                self.plot_a_dynamic_data(index_of_link, index_of_pvaj)

    def plot_subplot(self, index_in_pvaj):
        self.plot_dynamic_curves_on_one_subplot(index_of_pvaj=index_in_pvaj)
        self.set_grid_for_subplot()
        self.set_y_label()

    def set_x_limits(self):
        plt.xlim(0, int(max(self.an_all_links.links[0].m_deg) + 1))

    def set_x_ticks(self):
        plt.xticks(np.linspace(0, max(self.an_all_links.links[0].m_deg),
                               37, endpoint=True))


def set_legend():
    plt.legend(loc='upper right')


def plot_one_subplot(index_in_pvaj, a_dynamic_data, if_has_left_links=True,
                     whether_legend=False):
    curves = SubPvajPlot(index_in_pvaj, a_dynamic_data, if_has_left_links)
    curves.plot_subplot(index_in_pvaj)
    curves.set_x_limits()
    curves.set_x_ticks()
    if whether_legend:
        set_legend()
    return curves


def get_mark_handle_on_curve(dynamic_data):
    right_york_marks = Annotation(dynamic_data.links[0])
    right_jaw_marks = Annotation(dynamic_data.links[1])
    right_jaw_to_york_marks = Annotation(dynamic_data.links[2])
    left_york_marks = Annotation(dynamic_data.links[3])
    left_jaw_marks = Annotation(dynamic_data.links[4])
    left_jaw_to_york_marks = Annotation(dynamic_data.links[5])
    result = (
        right_york_marks, right_jaw_marks, right_jaw_to_york_marks,
        left_york_marks, left_jaw_marks, left_jaw_to_york_marks)
    return result


def mark_on_position_subplot(handles_of_marks_on_curve):
    rym, rjm, rjym, lym, ljm, lyjm = handles_of_marks_on_curve
    rym.mark_peak_point(0, "max", (70, 100), "pA", place=(20, -40))
    rjym.mark_peak_point(0, "min", (20, 60), "rA", place=(10, 20))
    rjym.mark_zero_point(0, (120, 150), "rB", place=(-50, 30))


def mark_on_velocity_subplot(handles_of_marks_on_curve):
    rym, rjm, rjym, lym, ljm, lyjm = handles_of_marks_on_curve
    rym.mark_zero_point(1, (80, 90), "yA", place=(-100, 20))
    rym.mark_peak_point(1, "max", (30, 50), "yB", place=(-30, -40))
    rym.mark_peak_point(1, "min", (90, 100), "yC", place=(-50, -40))
    rym.mark_peak_point(1, "max", (100, 110), "yC", place=(-10, -25))
    rym.mark_peak_point(1, "min", (130, 140), "yE", place=(-15, -30))
    rym.mark_peak_point(1, "max", (160, 180), "yF", place=(10, 30))
    rym.mark_peak_point(1, "min", (180, 200), "yG", place=(-10, -30))
    rym.mark_peak_point(1, "min", (260, 270), "yH", place=(-30, -30))
    rym.mark_peak_point(1, "max", (280, 310), "yK", place=(-50, 50))
    rym.mark_peak_point(1, "min", (310, 320), "yL", place=(-60, 50))
    rym.mark_peak_point(1, "min", (340, 350), "yM", place=(-65, 40))
    rjm.mark_zero_point(1, (110, 130), "jA", place=(20, 10))
    rjm.mark_peak_point(1, "max", (40, 60), "jB", place=(35, -20))
    rjm.mark_peak_point(1, "min", (90, 96), "jC", place=(-10, 35))
    rjm.mark_peak_point(1, "max", (96, 110), "jD", place=(30, 20))
    rjm.mark_peak_point(1, "min", (350, 360), "jE", place=(-140, 10))
    rjym.mark_peak_point(1, "min", (0, 10), "rA", place=(40, -10))
    rjym.mark_peak_point(1, "max", (90, 100), "rB", place=(-120, -50))
    rjym.mark_zero_point(1, (130, 140), "rC", place=(30, 50))


def mark_on_acceleration_subplot(handles_of_marks_on_curve):
    rym, rjm, rjym, lym, ljm, lyjm = handles_of_marks_on_curve
    rym.mark_peak_point(2, "max", (10, 20), "yA", place=(-30, -30))
    rym.mark_zero_point(2, (30, 50), "yB", place=(-90, 10))
    rym.mark_peak_point(2, "min", (60, 80), "yC", place=(-100, 0))
    rym.mark_zero_point(2, (90, 100), "yD", place=(-70, 40))
    rym.mark_zero_point(2, (100, 110), "yE", place=(0, 40))
    rym.mark_peak_point(2, "min", (110, 120), "yF", place=(-50, -45))
    rym.mark_zero_point(2, (130, 140), "yG", place=(-30, 55))
    rym.mark_zero_point(2, (140, 150), "yH", place=(0, 40))
    rym.mark_peak_point(2, "max", (150, 160), "yK", place=(-30, -40))
    rym.mark_zero_point(2, (160, 180), "yL", place=(-10, 55))
    rym.mark_peak_point(2, "min", (180, 190), "yM", place=(-50, -40))
    rym.mark_zero_point(2, (190, 200), "yN", place=(-50, 20))
    rym.mark_zero_point(2, (260, 270), "yP", place=(-50, 20))
    rym.mark_peak_point(2, "max", (270, 290), "yQ", place=(-30, 20))
    rym.mark_zero_point(2, (290, 300), "yR", place=(-50, -30))
    rym.mark_peak_point(2, "min", (300, 320), "yS", place=(-170, -20))
    rym.mark_zero_point(2, (310, 320), "yT", place=(-80, 55))
    rym.mark_zero_point(2, (320, 330), "yU", place=(5, 55))
    rym.mark_peak_point(2, "min", (330, 340), "yV", place=(-50, -25))
    rym.mark_zero_point(2, (340, 350), "yW", place=(-80, 35))
    rym.mark_peak_point(2, "max", (90, 110), "yX", place=(-30, 50))
    rjm.mark_peak_point(2, "max", (10, 30), "jA", place=(30, -5))
    rjm.mark_zero_point(2, (40, 60), "jB", place=(-20, 50))
    rjm.mark_peak_point(2, "min", (60, 80), "jC", place=(-50, 15))
    rjm.mark_zero_point(2, (90, 97), "jD", place=(-100, -15))
    rjm.mark_peak_point(2, "max", (90, 110), "jE", place=(-30, -45))
    rjm.mark_zero_point(2, (97, 110), "jF", place=(-100, 25))
    rjm.mark_peak_point(2, "min", (110, 130), "jG", place=(20, -10))
    rjm.mark_zero_point(2, (130, 140), "jH", place=(-10, -50))
    rjm.mark_peak_point(2, "min", (330, 350), "jK", place=(-160, -25))
    rjym.mark_zero_point(2, (0, 10), "rA", place=(10, -20))
    rjym.mark_peak_point(2, "max", (20, 40), "rB", place=(-60, -65))
    rjym.mark_zero_point(2, (90, 100), "rC", place=(-100, 10))
    rjym.mark_peak_point(2, "min", (110, 130), "rD", place=(-30, 40))
    rjym.mark_zero_point(2, (130, 140), "rE", place=(30, 70))
    rjym.mark_zero_point(2, (330, 335), "rF", place=(-80, 20))
    rjym.mark_peak_point(2, "min", (340, 350), "rG", place=(-70, -25))


def mark_on_jerk_subplot(handles_of_marks_on_curve):
    rym, rjm, rjym, lym, ljm, lyjm = handles_of_marks_on_curve
    rym.mark_peak_point(3, "min", (30, 50), "yA", place=(-10, -15))
    rym.mark_peak_point(3, "max", (80, 100), "yB", place=(-90, -10))
    rym.mark_peak_point(3, "min", (100, 110), "yC", place=(-30, -40))
    rym.mark_zero_point(3, (140, 150), "yD", place=(-80, 50))
    rym.mark_peak_point(3, "max", (140, 150), "yE", place=(-10, 20))
    rym.mark_zero_point(3, (150, 160), "yF", place=(-90, -30))
    rym.mark_peak_point(3, "min", (150, 170), "yG", place=(-50, -40))
    rym.mark_peak_point(3, "max", (160, 180), "yH", place=(-40, -50))
    rym.mark_peak_point(3, "min", (170, 190), "yJ", place=(30, -40))
    rym.mark_zero_point(3, (180, 190), "yJ", place=(-80, 20))
    rym.mark_peak_point(3, "max", (180, 200), "yL", place=(-10, 20))
    rym.mark_zero_point(3, (190, 200), "yM", place=(20, 20))
    rym.mark_peak_point(3, "max", (260, 280), "yN", place=(-30, 25))
    rym.mark_zero_point(3, (261, 270), "yO", place=(-80, 40))
    rym.mark_zero_point(3, (270, 280), "yP", place=(-100, -30))
    rym.mark_peak_point(3, "max", (280, 300), "yQ", place=(-50, -45))
    rym.mark_peak_point(3, "min", (290, 310), "yR", place=(-20, -30))
    rym.mark_peak_point(3, "min", (280, 290), "yI", place=(-80, -40))
    rym.mark_zero_point(3, (305, 315), "yS", place=(-80, 20))
    rym.mark_peak_point(3, "max", (310, 320), "yT", place=(-105, -20))
    rym.mark_zero_point(3, (315, 320), "yU", place=(-85, -30))
    rym.mark_peak_point(3, "min", (320, 340), "yV", place=(-30, -30))
    rym.mark_zero_point(3, (330, 340), "yW", place=(-80, 30))
    rym.mark_peak_point(3, "max", (340, 350), "yX", place=(-70, 25))
    rym.mark_zero_point(3, (10, 20), "yY", place=(-20, 50))
    rym.mark_zero_point(3, (60, 80), "yZ", place=(-80, 30))


def annotate_distance_on_one_subplot(tuple_of_two_points,
                                     a_curve_style,
                                     annotator_position):
    p1, p2 = tuple_of_two_points
    x1, y1 = p1
    x2, y2 = p2
    distance = sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    plt.plot([x1, x2], [y1, y2],
             color=a_curve_style.color,
             linewidth=a_curve_style.line_width,
             linestyle=a_curve_style.line_style)
    plt.annotate(str(round(distance, 2)),
                 xy=((x1 + x2) / 2, (y1 + y2) / 2),
                 xycoords='data',
                 xytext=annotator_position,
                 textcoords='offset points',
                 fontsize=a_curve_style.font_size,
                 arrowprops=dict(
                     arrowstyle="->", connectionstyle="arc3,rad=.2"))


def plot_dynamic_subplots(if_annotate=True,
                          if_left_links=True,
                          saved_name=None):
    # fig = \
    SuperPlot().get_fig_handle()
    dynamic_data = AllLinksWithDynData()
    # Handle of Marks on a curve, such as Right York, or Right Jaw to York.
    handles_of_marks_on_curve = get_mark_handle_on_curve(dynamic_data)
    # position_subplot = \
    plot_one_subplot(0, dynamic_data, whether_legend=True)
    if if_annotate:
        mark_on_position_subplot(handles_of_marks_on_curve)
    # velocity_subplot = \
    plot_one_subplot(1, dynamic_data)
    if if_annotate:
        mark_on_velocity_subplot(handles_of_marks_on_curve)
    # acceleration_subplot = \
    plot_one_subplot(2, dynamic_data, if_has_left_links=False)
    if if_annotate:
        mark_on_acceleration_subplot(handles_of_marks_on_curve)
    jerk_subplot = plot_one_subplot(3, dynamic_data, if_has_left_links=False)
    jerk_subplot.set_x_label()
    if if_annotate:
        mark_on_jerk_subplot(handles_of_marks_on_curve)
    if saved_name:
        plt.savefig(saved_name, dpi=720)


if __name__ == "__main__":
    plot_dynamic_subplots(
        # if_annotate=False,
        saved_name="./Tetra_Pak_A3_flex_Curves_with_721_points.png",
    )

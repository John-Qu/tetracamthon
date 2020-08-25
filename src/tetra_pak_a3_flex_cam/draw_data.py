import matplotlib.pyplot as plt
import numpy as np
from tetra_pak_a3_flex_cam.read_raw_data import \
    AllDynamicData, \
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


class Annotation(CurveStyle):
    def __init__(self, a_dyn_data):
        CurveStyle.__init__(self, a_dyn_data)
        self.data = a_dyn_data

    def mark_max_or_min_point(self, index_in_pvaj,
                              slice=(0, 100),
                              position=(30, 30),
                              mark_size=50,
                              font_size=12):
        a = self.data.data[index_in_pvaj]
        if a[slice[0]] <= a[slice[0] + 1] and \
                a[slice[1] - 1] >= a[slice[1]]:
            f = np.argmax
        elif a[slice[0]] >= a[slice[0] + 1] and \
                a[slice[1] - 1] <= a[slice[1]]:
            f = np.argmin
        else:
            raise IndexError
        index = f(a[slice[0]:slice[1]]) + slice[0]
        plt.scatter([index, ], [a[index], ], mark_size,
                    color=self.color)
        plt.annotate("(" + str(index) + ', ' +
                     str(round(a[index], 1)) + ")",
                     xy=(index, a[index]), xycoords='data',
                     xytext=position, textcoords='offset points',
                     fontsize=font_size,
                     arrowprops=dict(arrowstyle="->",
                                     connectionstyle="arc3,rad=.2"))


class SupPlotStyle(object):
    def __init__(self, num_row=4, num_col=1, position=1, grid_on=True):
        self.num_row = num_row
        self.num_col = num_col
        self.position = position
        self.grid_on = grid_on


def annotate_max_min_part_curve(a, start=0, end=None, col='red', mark_size=50,
                                position=(50, 50), font_size=12):
    """Mark a scatter on the curve of an array at index with position
    coordinate.

    :param a: array-like object
    :param start, end: int indicating the place of certain item in the array
    :param col: string of scatter color, better being the same with the curve
    of array
    :param mark_size: int (of points?)
    :param position: tuple of two ints or floats, relative to
    the scatter's place
    :param font_size: int of the messages' size
    :return: None, effecting the plt object
    """
    if a[start] <= a[start + 1] and a[end - 1] >= a[end]:
        f = np.argmax
    elif a[start] >= a[start + 1] and a[end - 1] <= a[end]:
        f = np.argmin
    else:
        raise IndexError
    index = f(a[start:end]) + start
    plt.scatter([index, ], [a[index], ], mark_size, color=col)
    plt.annotate("(" + str(index) + ', ' + str(round(a[index], 1)) + ")",
                 xy=(index, a[index]), xycoords='data',
                 xytext=position, textcoords='offset points',
                 fontsize=font_size,
                 arrowprops=dict(arrowstyle="->",
                                 connectionstyle="arc3,rad=.2"))


def annotate_zero_point_on_curve(a, start=0, end=None, step=1, col='red',
                                 mark_size=50, position=(50, 50),
                                 font_size=12):
    """Mark a scatter on the curve of an array at index with position
    coordinate.

    :param a: array-like object
    :param start, end: int indicating the place of certain item in the array
    :param col: string of scatter color, better being the same with
    the curve of array
    :param mark_size: int (of points?)
    :param position: tuple of two ints or floats, relative to the scatter's place
    :param font_size: int of the messages' size
    :return: None, effecting the plt object
    """
    index = np.argmin(np.abs(a[start:end:step])) * step + start
    plt.scatter([index, ], [a[index], ], mark_size, color=col)
    plt.annotate("(" + str(index) + ', ' + str(round(a[index], 1)) + ")",
                 xy=(index, a[index]), xycoords='data',
                 xytext=position, textcoords='offset points',
                 fontsize=font_size,
                 arrowprops=dict(arrowstyle="->",
                                 connectionstyle="arc3,rad=.2"))


class SuperPlot(object):
    def __init__(self, figsize=(15, 12), dpi=80):
        self.fig = plt.figure(figsize=figsize, dpi=dpi)
        self.set_super_title()

    def set_super_title(self,
                        title='Tetra Pak A3 Flex @ 8000 p/h \n York and Jaw'
                              ' PVAJ curves @ 0.9s/cycle',
                        font_size='xx-large'):
        self.fig.suptitle(title, fontsize=font_size)

    def get_fig_handle(self):
        return self.fig


def plt_plot(a_data, index_of_pvaj):
    style = CurveStyle(a_data)
    plt.plot(a_data.m_deg, a_data.data[index_of_pvaj],
             color=style.color,
             linewidth=style.line_width,
             linestyle=style.line_style,
             label=style.label)


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
        print(self.axes)
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


class SubDynamicCurves(SubPlot):
    def __init__(self, index_in_pvaj, dyn_data):
        self.index = index_in_pvaj
        SubPlot.__init__(self, self.index)
        self.dyn = dyn_data
        self.position_of_subplots = self.index + 1

    def plot_a_dynamic_data(self, index_of_a_data, index_of_pvaj):
        plt_plot(self.dyn.data[index_of_a_data], index_of_pvaj)

    def plot_dynamic_curves_on_one_subplot(self, index_of_pvaj):
        for index_of_a_data in range(len(self.dyn.data)):
            self.plot_a_dynamic_data(index_of_a_data, index_of_pvaj)

    def plot_subplot(self, index_in_pvaj):
        self.plot_dynamic_curves_on_one_subplot(index_of_pvaj=index_in_pvaj)
        self.set_grid_for_subplot()
        self.set_y_label()

    def set_x_limits(self):
        plt.xlim(0, int(max(self.dyn.data[0].m_deg) + 1))

    def set_x_ticks(self):
        plt.xticks(np.linspace(0, max(self.dyn.data[0].m_deg) + 1, 37,
                               endpoint=True))

    def set_legend(self):
        plt.legend(loc='upper right')


def plot_one_subplot(index_in_pvaj, a_dynamic_data, whether_legend=False):
    curves = SubDynamicCurves(index_in_pvaj, a_dynamic_data)
    curves.plot_subplot(index_in_pvaj)
    curves.set_x_limits()
    curves.set_x_ticks()
    if whether_legend:
        curves.set_legend()
    return curves


if __name__ == "__main__":
    fig = SuperPlot().get_fig_handle()
    dynamic_data = AllDynamicData()

    pos_curves = plot_one_subplot(0, dynamic_data, whether_legend=True)
    right_york_annotation = Annotation(dynamic_data.data[0])
    right_york_annotation.mark_max_or_min_point(0, slice=(40, 100),
                                                position=(30, 30))
    vel_curves = plot_one_subplot(1, dynamic_data)
    acc_curves = plot_one_subplot(2, dynamic_data)
    jer_curves = plot_one_subplot(3, dynamic_data)
    jer_curves.set_x_label()

# Create a figure of size 8x6 inches, 80 dots per inch
# fig = plt.figure(figsize=(15, 12), dpi=80)
# fig.suptitle(
#     'Tetra Pak A3 Flex @ 8000 p/h \n York and Jaw SVAJ curves @ 0.9s/cycle',
#     fontsize='xx-large')
#
# plt.subplot(4, 1, 1)
# plt.grid()
# plt.xlabel("Machine Degree")
# plt.ylabel("Position and Distance (mm)")
# plt.plot(d, right_york_place, color="blue", linewidth=3.0, linestyle="-",
#          label="right york")
# plt.plot(d, left_york_place, color="blue", linewidth=1.0, linestyle="--",
#          label="left york")
# plt.plot(d, right_jaw_place, color="green", linewidth=3.0, linestyle="-",
#          label="right jaw")
# plt.plot(d, left_jaw_place, color="green", linewidth=1.0, linestyle="--",
#          label="left jaw")
# plt.plot(d, right_jaw_to_york_place, color="red", linewidth=3.0, linestyle="-",
#          label="right jaw to york")
# plt.plot(d, left_jaw_to_york_place, color="red", linewidth=1.0, linestyle="--",
#          label="left jaw to york")
# index_min_diff_right_york_place_right_jaw_place = np.argmin(
#     right_jaw_to_york_place)
# index_max_right_york_place = np.argmax(right_york_place)
# # annotate_max_min_part_curve(right_jaw_to_york_place, 20, 80, col="red",
# #                             position=(30, 17))
# annotate_max_min_part_curve(right_york_place, 40, 100, col="blue",
#                             position=(10, -30))
# plt.plot([138, 138], [left_york_place[138], right_york_place[138]],
#          color='blue', linewidth=2, linestyle=":")
# plt.annotate(str(round(right_york_place[138] - left_york_place[138])),
#              xy=(138, (right_york_place[138] + left_york_place[138]) / 2),
#              xycoords='data',
#              xytext=(20, -20), textcoords='offset points', fontsize=12,
#              arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
# plt.legend(loc='upper right')
# plt.xlim(0.0, 360.0)
# plt.xticks(np.linspace(0, 360, 37, endpoint=True))
# plt.ylim(-200, 500)
# plt.yticks(np.linspace(-200, 500, 8, endpoint=True))
# annotate_zero_point_on_curve(right_jaw_to_york_place, 110, 140, col="red",
#                              position=(10, -30))
#
# # Velocity
# plt.subplot(4, 1, 2)
# plt.grid()
# plt.ylabel("Velocity (mm/s)")
# plt.plot(d, right_york_velo, color="blue", linewidth=3.0, linestyle="-",
#          label="right york")
# plt.plot(d, left_york_velo, color="blue", linewidth=1.0, linestyle="--",
#          label="left york")
# plt.plot(d, right_jaw_velo, color="green", linewidth=3.0, linestyle="-",
#          label="right jaw")
# plt.plot(d, left_jaw_velo, color="green", linewidth=1.0, linestyle="--",
#          label="left jaw")
# plt.plot(d, right_jaw_to_york_velo, color="red", linewidth=3.0, linestyle="-",
#          label="right jaw to york")
# plt.plot(d, left_jaw_to_york_velo, color="red", linewidth=1.0, linestyle="--",
#          label="left jaw to york")
#
# annotate_max_min_part_curve(right_york_velo, 130, 150, col="green",
#                             position=(-70, 70))
# annotate_max_min_part_curve(right_york_velo, 160, 180, col="green",
#                             position=(-20, 30))
# annotate_max_min_part_curve(right_york_velo, 180, 280, col="green",
#                             position=(-10, -30))
# annotate_max_min_part_curve(right_york_velo, 280, 310, col="green",
#                             position=(10, 15))
# annotate_max_min_part_curve(right_york_velo, 310, 320, col="green",
#                             position=(-50, -30))
# annotate_zero_point_on_curve(right_jaw_to_york_velo, 120, 140, col="red")
# # plt.legend(loc='upper right')
# plt.xlim(0.0, 360.0)
# plt.xticks(np.linspace(0, 360, 37, endpoint=True))
# plt.ylim(-2000, 4000)
# plt.yticks(np.linspace(-2000, 4000, 7, endpoint=True))
#
# # Acceleration
# plt.subplot(4, 1, 3)
# plt.grid()
# plt.ylabel("Acceleration (m/s^2)")
# plt.plot(d, right_york_acc, color="blue", linewidth=3.0, linestyle="-",
#          label="right york")
# plt.plot(d, left_york_acc, color="blue", linewidth=1.0, linestyle="--",
#          label="left york")
# # Plot jaw acceleration with a green continuous line of width 1 (pixels)
# plt.plot(d, right_jaw_acc, color="green", linewidth=3.0, linestyle="-",
#          label="right jaw")
# plt.plot(d, left_jaw_acc, color="green", linewidth=1.0, linestyle="--",
#          label="left jaw")
# plt.plot(d, right_jaw_to_york_acc, color="red", linewidth=3.0, linestyle="-",
#          label="right jaw to york")
# plt.plot(d, left_jaw_to_york_acc, color="red", linewidth=1.0, linestyle="--",
#          label="left jaw")
# annotate_max_min_part_curve(right_york_acc, 0, 20, col="blue",
#                             position=(-20, -40))
# annotate_max_min_part_curve(right_jaw_acc, 10, 30, col="green",
#                             position=(40, -30))
# annotate_max_min_part_curve(right_york_acc, 60, 80, col="blue",
#                             position=(-70, -20))
# annotate_max_min_part_curve(right_jaw_acc, 60, 80, col="green",
#                             position=(20, -20))
# annotate_max_min_part_curve(right_york_acc, 90, 100, col="blue",
#                             position=(-50, 50))
# annotate_max_min_part_curve(right_jaw_acc, 90, 100, col="green",
#                             position=(-70, 10))
# annotate_max_min_part_curve(right_york_acc, 110, 130, col="blue",
#                             position=(20, 30))
# annotate_max_min_part_curve(right_jaw_acc, 110, 130, col="green",
#                             position=(10, -40))
# annotate_max_min_part_curve(right_jaw_acc, 150, 160, col="green",
#                             position=(10, 20))
# annotate_max_min_part_curve(right_jaw_acc, 180, 190, col="green",
#                             position=(-70, -30))
# annotate_max_min_part_curve(right_jaw_acc, 270, 280, col="green",
#                             position=(-70, 30))
# annotate_max_min_part_curve(right_jaw_acc, 300, 315, col="green",
#                             position=(-70, -30))
# annotate_max_min_part_curve(right_york_acc, 330, 340, col="blue",
#                             position=(-50, -40))
# annotate_max_min_part_curve(right_jaw_acc, 330, 350, col="green",
#                             position=(-50, -35))
# annotate_zero_point_on_curve(right_york_acc, 130, 140,
#                              col="blue", position=(-50, 40))
# annotate_zero_point_on_curve(right_jaw_acc, 310, 320,
#                              col="green", position=(0, 20))
# annotate_zero_point_on_curve(right_jaw_acc, 270, 260,
#                              step=-1, col="green", position=(-50, 10))
# annotate_zero_point_on_curve(right_jaw_acc, 290, 300,
#                              col="green", position=(-10, 20))
# annotate_zero_point_on_curve(right_jaw_acc, 190, 200,
#                              col="green", position=(20, 20))
# annotate_zero_point_on_curve(right_jaw_acc, 150, 140,
#                              step=-1, col="green", position=(10, -30))
# annotate_zero_point_on_curve(right_jaw_acc, 160, 180,
#                              col="green", position=(20, 20))
# annotate_zero_point_on_curve(right_york_acc, 320, 330,
#                              col="blue", position=(-20, -30))
# # plt.legend(loc='upper right')
# plt.xlim(0.0, 360.0)
# plt.xticks(np.linspace(0, 360, 37, endpoint=True))
# plt.ylim(-60.0, 60.0)
# plt.yticks(np.linspace(-60, 60, 7, endpoint=True))
#
# # Jerk
# plt.subplot(4, 1, 4)
# plt.grid()
# plt.ylabel("Jerk (m/s^3)")
# plt.plot(d, right_york_jerk, color="blue", linewidth=3.0, linestyle="-",
#          label="right york")
# plt.plot(d, right_jaw_jerk, color="green", linewidth=3.0, linestyle="-",
#          label="right jaw")
# # plt.legend(loc='upper right')
# plt.xlim(0.0, 360.0)
# plt.xticks(np.linspace(0, 360, 37, endpoint=True))
# plt.ylim(-2000.0, 2000.0)
# plt.yticks(np.linspace(-2000, 2000, 9, endpoint=True))
#
# # Save figure using 720 dots per inch
# plt.savefig("./Tetra_Pak_A3_flex_Curves_temp.png", dpi=720)

# Show result on screen

# plt.show()

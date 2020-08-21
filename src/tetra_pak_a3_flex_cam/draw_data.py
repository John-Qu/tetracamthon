from read_raw_data import calculate_avp
import matplotlib.pyplot as plt
import numpy as np

# Get data from raw csv data as right york and jaw pair.
d, \
right_york_acc, right_jaw_acc, \
right_york_velo, right_jaw_velo, \
right_york_place, right_jaw_place \
    = calculate_avp()

right_york_jerk = np.ones(361)
right_york_jerk[:360] = np.diff(right_york_acc)
right_york_jerk[-1] = right_york_jerk[
    0]  # fill the end point as the same of start
right_york_jerk = right_york_jerk / (0.9 / 360)
right_jaw_jerk = np.ones(361)
right_jaw_jerk[:360] = np.diff(right_jaw_acc)
right_jaw_jerk[-1] = right_jaw_jerk[0]  # fill end point
right_jaw_jerk = right_jaw_jerk / (0.9 / 360)

# Slicing data for the left york and jaw pair.
left_york_acc = np.hstack((right_york_acc[-181:-1], right_york_acc[:181]))
left_jaw_acc = np.hstack((right_jaw_acc[-181:-1], right_jaw_acc[:181]))
left_york_velo = np.hstack((right_york_velo[-181:-1], right_york_velo[:181]))
left_jaw_velo = np.hstack((right_jaw_velo[-181:-1], right_jaw_velo[:181]))
left_york_place = np.hstack(
    (right_york_place[-181:-1], right_york_place[:181]))
left_jaw_place = np.hstack((right_jaw_place[-181:-1], right_jaw_place[:181]))

# Calculate the relative velocities and placements between york and jaw.
right_jaw_to_york_velo = right_jaw_velo - right_york_velo
right_jaw_to_york_place = right_jaw_place - right_york_place
left_jaw_to_york_velo = left_jaw_velo - left_york_velo
left_jaw_to_york_place = left_jaw_place - left_york_place
right_jaw_to_york_acc = right_jaw_acc - right_york_acc
left_jaw_to_york_acc = left_jaw_acc - left_york_acc


def annotate_max_min_part_curve(a, start=0, end=None, col='red', mark_size=50,
                                position=(50, 50), font_size=12):
    """Mark a scatter on the curve of an array at index with position coordinate.

    :param a: array-like object
    :param start, end: int indicating the place of certain item in the array
    :param col: string of scatter color, better being the same with the curve of array
    :param mark_size: int (of points?)
    :param position: tuple of two ints or floats, relative to the scatter's place
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
    """Mark a scatter on the curve of an array at index with position coordinate.

    :param a: array-like object
    :param start, end: int indicating the place of certain item in the array
    :param col: string of scatter color, better being the same with the curve of array
    :param mark_size: int (of points?)
    :param position: tuple of two ints or floats, relative to the scatter's place
    :param font_size: int of the messages' size
    :return: None, effecting the plt object
    """
    index = np.argmin(np.abs(a[start:end:step])) * (step) + start
    plt.scatter([index, ], [a[index], ], mark_size, color=col)
    plt.annotate("(" + str(index) + ', ' + str(round(a[index], 1)) + ")",
                 xy=(index, a[index]), xycoords='data',
                 xytext=position, textcoords='offset points',
                 fontsize=font_size,
                 arrowprops=dict(arrowstyle="->",
                                 connectionstyle="arc3,rad=.2"))


# Create a figure of size 8x6 inches, 80 dots per inch
fig = plt.figure(figsize=(15, 12), dpi=80)
fig.suptitle(
    'Tetra Pak A3 Flex @ 8000 p/h \n York and Jaw SVAJ curves @ 0.9s/cycle',
    fontsize='xx-large')

plt.subplot(4, 1, 1)
plt.grid()
plt.xlabel("Machine Degree")
plt.ylabel("Position and Distance (mm)")
plt.plot(d, right_york_place, color="blue", linewidth=3.0, linestyle="-",
         label="right york")
plt.plot(d, left_york_place, color="blue", linewidth=1.0, linestyle="--",
         label="left york")
plt.plot(d, right_jaw_place, color="green", linewidth=3.0, linestyle="-",
         label="right jaw")
plt.plot(d, left_jaw_place, color="green", linewidth=1.0, linestyle="--",
         label="left jaw")
plt.plot(d, right_jaw_to_york_place, color="red", linewidth=3.0, linestyle="-",
         label="right jaw to york")
plt.plot(d, left_jaw_to_york_place, color="red", linewidth=1.0, linestyle="--",
         label="left jaw to york")
index_min_diff_right_york_place_right_jaw_place = np.argmin(
    right_jaw_to_york_place)
index_max_right_york_place = np.argmax(right_york_place)
annotate_max_min_part_curve(right_jaw_to_york_place, 20, 80, col="red",
                            position=(30, 17))
annotate_max_min_part_curve(right_york_place, 40, 100, col="blue",
                            position=(10, -30))
plt.plot([138, 138], [left_york_place[138], right_york_place[138]],
         color='blue', linewidth=2, linestyle=":")
plt.annotate(str(round(right_york_place[138] - left_york_place[138])),
             xy=(138, (right_york_place[138] + left_york_place[138]) / 2),
             xycoords='data',
             xytext=(20, -20), textcoords='offset points', fontsize=12,
             arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
plt.legend(loc='upper right')
plt.xlim(0.0, 360.0)
plt.xticks(np.linspace(0, 360, 37, endpoint=True))
plt.ylim(-200, 500)
plt.yticks(np.linspace(-200, 500, 8, endpoint=True))
annotate_zero_point_on_curve(right_jaw_to_york_place, 110, 140, col="red",
                             position=(10, -30))

# Velocity
plt.subplot(4, 1, 2)
plt.grid()
plt.ylabel("Velocity (mm/s)")
plt.plot(d, right_york_velo, color="blue", linewidth=3.0, linestyle="-",
         label="right york")
plt.plot(d, left_york_velo, color="blue", linewidth=1.0, linestyle="--",
         label="left york")
plt.plot(d, right_jaw_velo, color="green", linewidth=3.0, linestyle="-",
         label="right jaw")
plt.plot(d, left_jaw_velo, color="green", linewidth=1.0, linestyle="--",
         label="left jaw")
plt.plot(d, right_jaw_to_york_velo, color="red", linewidth=3.0, linestyle="-",
         label="right jaw to york")
plt.plot(d, left_jaw_to_york_velo, color="red", linewidth=1.0, linestyle="--",
         label="left jaw to york")

annotate_max_min_part_curve(right_york_velo, 130, 150, col="green",
                            position=(-70, 70))
annotate_max_min_part_curve(right_york_velo, 160, 180, col="green",
                            position=(-20, 30))
annotate_max_min_part_curve(right_york_velo, 180, 280, col="green",
                            position=(-10, -30))
annotate_max_min_part_curve(right_york_velo, 280, 310, col="green",
                            position=(10, 15))
annotate_max_min_part_curve(right_york_velo, 310, 320, col="green",
                            position=(-50, -30))
annotate_zero_point_on_curve(right_jaw_to_york_velo, 120, 140, col="red")
# plt.legend(loc='upper right')
plt.xlim(0.0, 360.0)
plt.xticks(np.linspace(0, 360, 37, endpoint=True))
plt.ylim(-2000, 4000)
plt.yticks(np.linspace(-2000, 4000, 7, endpoint=True))

# Acceleration
plt.subplot(4, 1, 3)
plt.grid()
plt.ylabel("Acceleration (m/s^2)")
plt.plot(d, right_york_acc, color="blue", linewidth=3.0, linestyle="-",
         label="right york")
plt.plot(d, left_york_acc, color="blue", linewidth=1.0, linestyle="--",
         label="left york")
# Plot jaw acceleration with a green continuous line of width 1 (pixels)
plt.plot(d, right_jaw_acc, color="green", linewidth=3.0, linestyle="-",
         label="right jaw")
plt.plot(d, left_jaw_acc, color="green", linewidth=1.0, linestyle="--",
         label="left jaw")
plt.plot(d, right_jaw_to_york_acc, color="red", linewidth=3.0, linestyle="-",
         label="right jaw to york")
plt.plot(d, left_jaw_to_york_acc, color="red", linewidth=1.0, linestyle="--",
         label="left jaw")
annotate_max_min_part_curve(right_york_acc, 0, 20, col="blue",
                            position=(-20, -40))
annotate_max_min_part_curve(right_jaw_acc, 10, 30, col="green",
                            position=(40, -30))
annotate_max_min_part_curve(right_york_acc, 60, 80, col="blue",
                            position=(-70, -20))
annotate_max_min_part_curve(right_jaw_acc, 60, 80, col="green",
                            position=(20, -20))
annotate_max_min_part_curve(right_york_acc, 90, 100, col="blue",
                            position=(-50, 50))
annotate_max_min_part_curve(right_jaw_acc, 90, 100, col="green",
                            position=(-70, 10))
annotate_max_min_part_curve(right_york_acc, 110, 130, col="blue",
                            position=(20, 30))
annotate_max_min_part_curve(right_jaw_acc, 110, 130, col="green",
                            position=(10, -40))
annotate_max_min_part_curve(right_jaw_acc, 150, 160, col="green",
                            position=(10, 20))
annotate_max_min_part_curve(right_jaw_acc, 180, 190, col="green",
                            position=(-70, -30))
annotate_max_min_part_curve(right_jaw_acc, 270, 280, col="green",
                            position=(-70, 30))
annotate_max_min_part_curve(right_jaw_acc, 300, 315, col="green",
                            position=(-70, -30))
annotate_max_min_part_curve(right_york_acc, 330, 340, col="blue",
                            position=(-50, -40))
annotate_max_min_part_curve(right_jaw_acc, 330, 350, col="green",
                            position=(-50, -35))
annotate_zero_point_on_curve(right_york_acc, 130, 140,
                             col="blue", position=(-50, 40))
annotate_zero_point_on_curve(right_jaw_acc, 310, 320,
                             col="green", position=(0, 20))
annotate_zero_point_on_curve(right_jaw_acc, 270, 260,
                             step=-1, col="green", position=(-50, 10))
annotate_zero_point_on_curve(right_jaw_acc, 290, 300,
                             col="green", position=(-10, 20))
annotate_zero_point_on_curve(right_jaw_acc, 190, 200,
                             col="green", position=(20, 20))
annotate_zero_point_on_curve(right_jaw_acc, 150, 140,
                             step=-1, col="green", position=(10, -30))
annotate_zero_point_on_curve(right_jaw_acc, 160, 180,
                             col="green", position=(20, 20))
annotate_zero_point_on_curve(right_york_acc, 320, 330,
                             col="blue", position=(-20, -30))
# plt.legend(loc='upper right')
plt.xlim(0.0, 360.0)
plt.xticks(np.linspace(0, 360, 37, endpoint=True))
plt.ylim(-60.0, 60.0)
plt.yticks(np.linspace(-60, 60, 7, endpoint=True))

# Jerk
plt.subplot(4, 1, 4)
plt.grid()
plt.ylabel("Jerk (m/s^3)")
plt.plot(d, right_york_jerk, color="blue", linewidth=3.0, linestyle="-",
         label="right york")
plt.plot(d, right_jaw_jerk, color="green", linewidth=3.0, linestyle="-",
         label="right jaw")
# plt.legend(loc='upper right')
plt.xlim(0.0, 360.0)
plt.xticks(np.linspace(0, 360, 37, endpoint=True))
plt.ylim(-2000.0, 2000.0)
plt.yticks(np.linspace(-2000, 2000, 9, endpoint=True))

# Save figure using 720 dots per inch
plt.savefig("../plot/Tetra_Pak_A3_flex_Curves.png", dpi=720)

# Show result on screen

# plt.show()

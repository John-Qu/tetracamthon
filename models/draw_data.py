from read_raw_data import calculate_avp
import matplotlib.pyplot as plt
import numpy as np

d, \
right_york_acc, right_jaw_acc, \
right_york_velo, right_jaw_velo, \
right_york_place, right_jaw_place \
    = calculate_avp()
left_york_acc = np.hstack((right_york_acc[-181:-1], right_york_acc[:181]))
left_jaw_acc = np.hstack((right_jaw_acc[-181:-1], right_jaw_acc[:181]))
left_york_velo = np.hstack((right_york_velo[-181:-1], right_york_velo[:181]))
left_jaw_velo = np.hstack((right_jaw_velo[-181:-1], right_jaw_velo[:181]))
left_york_place = np.hstack((right_york_place[-181:-1], right_york_place[:181]))
left_jaw_place = np.hstack((right_jaw_place[-181:-1], right_jaw_place[:181]))

right_jaw_to_york_velo = right_jaw_velo - right_york_velo
right_jaw_to_york_place = right_jaw_place - right_york_place
left_jaw_to_york_velo = left_jaw_velo - left_york_velo
left_jaw_to_york_place = left_jaw_place - left_york_place

def annotate_scatter(index, a, col='red', mark_size=50, position=(50, 50), font_size=12):
    plt.scatter([index, ], [a[index], ], mark_size, color=col)
    plt.annotate("(" + str(index) + ', '+ str(round(a[index], 1)) + ")",
                 xy=(index, a[index]), xycoords='data',
                 xytext=position, textcoords='offset points', fontsize=font_size,
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))

# Create a figure of size 8x6 inches, 80 dots per inch
fig = plt.figure(figsize=(15, 12), dpi=80)
fig.suptitle('Tetra Pak A3 CompactFlex \n york and jaw curves \n cycle time: 0.9s')
# Create a new subplot from a grid of 1x1
plt.subplot(3, 1, 1)
plt.grid()
# Plot york acceleration with a blue continuous line of width 1 (pixels)
plt.plot(d, right_york_acc, color="blue", linewidth=3.0, linestyle="-", label="right york_acceleration")
plt.plot(d, left_york_acc, color="blue", linewidth=1.0, linestyle="--", label="left york acceleration")
# Plot jaw acceleration with a green continuous line of width 1 (pixels)
plt.plot(d, right_jaw_acc, color="green", linewidth=3.0, linestyle="-", label="right jaw acceleration")
plt.plot(d, left_jaw_acc, color="green", linewidth=1.0, linestyle="--", label="left jaw acceleration")
plt.legend(loc='upper right')
plt.xlim(0.0, 360.0)
plt.xticks(np.linspace(0, 360, 37, endpoint=True))
plt.ylim(-60.0, 60.0)
plt.yticks(np.linspace(-60, 60, 7, endpoint=True))

plt.subplot(3, 1, 2)
plt.grid()
plt.plot(d, right_york_velo, color="blue", linewidth=3.0, linestyle="-", label="right york velocity")
plt.plot(d, left_york_velo, color="blue", linewidth=1.0, linestyle="--", label="left york velocity")
plt.plot(d, right_jaw_velo, color="green", linewidth=3.0, linestyle="-", label="right jaw velocity")
plt.plot(d, left_jaw_velo, color="green", linewidth=1.0, linestyle="--", label="left jaw velocity")
plt.plot(d, right_jaw_to_york_velo, color="red", linewidth=3.0, linestyle="-", label="right jaw to york velocity")
plt.plot(d, left_jaw_to_york_velo, color="red", linewidth=1.0, linestyle="--", label="left jaw to york velocity")

index_min_ryav_130_150 = np.argmin(right_york_velo[130:150]) + 130
index_max_ryav_150_190 = np.argmax(right_york_velo[150:190]) + 150
index_min_ryav_190_270 = np.argmin(right_york_velo[190:270]) + 190
index_max_ryav_270_310 = np.argmax(right_york_velo[270:310]) + 270
index_min_ryav_310_325 = np.argmin(right_york_velo[310:325]) + 310
annotate_scatter(index_min_ryav_130_150, right_york_velo, col="green", position=(-70,70))
annotate_scatter(index_max_ryav_150_190, right_york_velo, col="green", position=(-20,40))
annotate_scatter(index_min_ryav_190_270, right_york_velo, col="green", position=(-10,-30))
annotate_scatter(index_max_ryav_270_310, right_york_velo, col="green", position=(10, 15))
annotate_scatter(index_min_ryav_310_325, right_york_velo, col="green", position=(-50, -30))

plt.legend(loc='upper right')
plt.xlim(0.0, 360.0)
plt.xticks(np.linspace(0, 360, 37, endpoint=True))
plt.ylim(-2000, 4000)
plt.yticks(np.linspace(-2000, 4000, 7, endpoint=True))

plt.subplot(3, 1, 3)
plt.grid()
plt.plot(d, right_york_place, color="blue", linewidth=3.0, linestyle="-", label="right york placement")
plt.plot(d, left_york_place, color="blue", linewidth=1.0, linestyle="--", label="left york placement")
plt.plot(d, right_jaw_place, color="green", linewidth=3.0, linestyle="-", label="right york placement")
plt.plot(d, left_jaw_place, color="green", linewidth=1.0, linestyle="--", label="left york placement")
plt.plot(d, right_jaw_to_york_place, color="red", linewidth=3.0, linestyle="-", label="right jaw to york position")
plt.plot(d, left_jaw_to_york_place, color="red", linewidth=1.0, linestyle="--", label="left jaw to york position")
index_min_diff_right_york_place_right_jaw_place = np.argmin(right_jaw_to_york_place)
index_max_right_york_place = np.argmax(right_york_place)
annotate_scatter(index_min_diff_right_york_place_right_jaw_place, right_jaw_to_york_place, col="red", position=(30, 20))
annotate_scatter(index_max_right_york_place, right_york_place, col="blue", position=(10, -40))
plt.plot([133, 133], [left_york_place[133], right_york_place[133]], color='blue', linewidth=1, linestyle=":")
plt.annotate(str(round(right_york_place[133] - left_york_place[133])),
                 xy=(133, (right_york_place[133] + left_york_place[133])/2), xycoords='data',
                 xytext=(20, -20), textcoords='offset points', fontsize=12,
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
plt.legend(loc='upper right')
plt.xlim(0.0, 360.0)
plt.xticks(np.linspace(0, 360, 37, endpoint=True))
plt.ylim(-200, 500)
plt.yticks(np.linspace(-200, 500, 8, endpoint=True))

# Save figure using 720 dots per inch
plt.savefig("Tetra Pak A3 flex Curves.png", dpi=720)

# Show result on screen

# plt.show()

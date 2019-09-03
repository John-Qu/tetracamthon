import csv
from collections import namedtuple
import numpy as np
import matplotlib.pyplot as plt

def get_csv_data():
    """
    Get 360 degree york and jaw acceleration data from csv file.
    :return: lists of float of data
    """
    with open('../data/RawData_360.csv') as f:
        f_csv = csv.reader(f)
        headings = next(f_csv)
        Row = namedtuple('Row', headings)
        degree, york_acc, jaw_acc = [], [], []
        for r in f_csv:
            row = Row(*r)
            degree.append(int(row.Degree))
            york_acc.append(float(row.York_acc))
            jaw_acc.append(float(row.Jaw_acc))
    return degree, york_acc, jaw_acc

def meet_jork_jaw_there(york_acc, jaw_acc):
    for i in range(130, 340):
        if abs(york_acc[i] - jaw_acc[i]) < 0.3:
            york_acc[i] = jaw_acc[i] = (york_acc[i] + jaw_acc[i])/2
    return york_acc, jaw_acc


degree, york_acc, jaw_acc = get_csv_data()
york_acc, jaw_acc = meet_jork_jaw_there(york_acc, jaw_acc)


if __name__ == "__main__":
    # degree, york_acc, jaw_acc = get_csv_data()
    # york_acc, jaw_acc = meet_jork_jaw_there(york_acc, jaw_acc)
    # # Create a figure of size 8x6 inches, 80 dots per inch
    plt.figure(figsize=(30, 10), dpi=80)
    # Create a new subplot from a grid of 1x1
    plt.subplot(1, 1, 1)
    # X = np.linspace(-np.pi, np.pi, 256, endpoint=True)
    X = np.array(degree)
    # C, S = np.cos(X), np.sin(X)
    C = np.array(york_acc)
    S = np.array(jaw_acc)
    # Plot cosine with a blue continuous line of width 1 (pixels)
    plt.plot(X, C, color="blue", linewidth=2.0, linestyle="-", label="york_acc")
    # Plot sine with a green continuous line of width 1 (pixels)
    plt.plot(X, S, color="green", linewidth=2.0, linestyle="-", label="jaw_acc") # Set x limits
    # plt.xlim(-4.0, 4.0) # Set x ticks
    plt.legend(loc='upper right')
    plt.xlim(0.0, 360.0) # Set x ticks
    plt.xticks(np.linspace(0, 360, 37, endpoint=True)) # Set y limits
    plt.ylim(-60.0, 60.0) # Set y ticks
    plt.yticks(np.linspace(-60, 60, 7, endpoint=True)) # Save figure using 72 dots per inch
    plt.savefig("exercise_2.png", dpi=720)

    # Show result on screen

    plt.show()

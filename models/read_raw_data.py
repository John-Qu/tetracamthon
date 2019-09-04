import csv
from collections import namedtuple
import numpy as np
from scipy.integrate import cumtrapz

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
    return np.array(degree), np.array(york_acc), np.array(jaw_acc)

def meet_jork_jaw_there(york_acc, jaw_acc):
    for i in range(130, 340):
        if abs(york_acc[i] - jaw_acc[i]) < 0.3:
            york_acc[i] = jaw_acc[i] = (york_acc[i] + jaw_acc[i])/2
    return york_acc, jaw_acc


def zerolyse_part_of_acc(york_acc, jaw_acc):
    """In the center part, they should be exact zeros.

    :param york_acc:
    :param jaw_acc:
    :return: side effect
    """
    for i in range(198, 263):
        if abs(york_acc[i]) < 0.3:
            york_acc[i] = jaw_acc[i] = 0
    return york_acc, jaw_acc


def calculate_avp():
    """Calculate the acceleration, velocity and placement from csv data.
    :return """
    degree, york_acc, jaw_acc = get_csv_data()
    york_acc -= 0.169
    jaw_acc -= 0.159
    york_acc, jaw_acc = meet_jork_jaw_there(york_acc, jaw_acc)
    york_acc, jaw_acc = zerolyse_part_of_acc(york_acc,jaw_acc)
    york_velo = cumtrapz(york_acc, degree, initial=0) * (0.9 / 360 * 1000)
    jaw_velo = cumtrapz(jaw_acc, degree, initial=0) * (0.9 / 360 * 1000)
    jaw_velo = jaw_velo - (jaw_velo[220] - york_velo[220])
    york_place = cumtrapz(york_velo, degree, initial=0) * (0.9 / 360)
    jaw_place = cumtrapz(jaw_velo, degree, initial=0) * (0.9 / 360)
    jaw_place += york_place[230]-jaw_place[230]
    return degree, york_acc, jaw_acc, york_velo, jaw_velo, york_place, jaw_place

if __name__ == "__main__":
    degree, york_acc, jaw_acc, york_velo, jaw_velo, york_place, jaw_place = calculate_avp()
    print('the last three of york_velocity:', york_velo[-3], york_velo[-2], york_velo[-1])
    # print('the last two of jaw_velocity:', jaw_velo[-2], jaw_velo[-1])
    print('the first three of york_velocity:', york_velo[0], york_velo[1], york_velo[2])
    print(york_velo[-3] - york_velo[-2])
    print(york_velo[1] - york_velo[2])
    print(york_velo[-2] - york_velo[1])

    print('the last three of jaw_velocity:', jaw_velo[-3], jaw_velo[-2], jaw_velo[-1])
    # print('the last two of jaw_velocity:', jaw_velo[-2], jaw_velo[-1])
    print('the first three of jaw_velocity:', jaw_velo[0], jaw_velo[1], jaw_velo[2])
    print(jaw_velo[-3] - jaw_velo[-2])
    print(jaw_velo[1] - jaw_velo[2])
    print(jaw_velo[-2] - jaw_velo[1])
    print("-"*10)
    print(york_place[133]-york_place[133+180])


# def bisection_search(start ,end):
# TODO: fine tune the adjust value
# stage_diff = abs(york_velo[-2] - york_velo[1] -
#                  ((york_velo[-3] - york_velo[-2]) +
#                   (york_velo[2] - york_velo[1])) / 2)
# while stage_diff > 10:
#
#


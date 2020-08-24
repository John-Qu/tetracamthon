import csv
from collections import namedtuple
import numpy as np
from scipy.integrate import cumtrapz


class TetraPakA3AccMeasured(object):
    """Get the acceleration of Tetra Pak A3 Flex curve."""

    def __init__(self,
                 path_to_csv='./tetra_pak_a3_flex_cam_acc_raw_data_360.csv'):
        self.machine_degree = []
        self.york_acc = []
        self.jaw_acc = []
        self.read_in_csv_data(path_to_csv)

    def read_in_csv_data(self, path_to_csv):
        """Get 360 degree york and jaw acceleration data from a csv file."""
        with open(path_to_csv) as f:
            f_csv = csv.reader(f)
            headings = next(f_csv)
            Row = namedtuple('Row', headings)
            for r in f_csv:
                row = Row(*r)
                self.machine_degree.append(int(row.machine_degree))
                self.york_acc.append(float(row.york_acc_raw))
                self.jaw_acc.append(float(row.jaw_acc_raw))
        return self


class TetraPakA3AccModified(TetraPakA3AccMeasured):
    """Modified the measured acceleration data of Tetra Pak A3 Flex curve."""

    def __init__(self,
                 york_by_this=-0.169, jaw_by_that=-0.159,
                 meet_there=(130, 340), zeroes_there=(198, 263),
                 error_tolerance=0.3):
        TetraPakA3AccMeasured.__init__(self)
        self.adjust_a_little_as_a_whole(york_by_this, jaw_by_that)
        self.meet_york_jaw_there(meet_there, error_tolerance)
        self.become_zeroes_there(zeroes_there, error_tolerance)

    def adjust_a_little_as_a_whole(self, york_by_this, jaw_by_that):
        # TODO: fine tune the adjust value
        for i in range(len(self.york_acc)):
            self.york_acc[i] += york_by_this
            self.jaw_acc[i] += jaw_by_that

    def meet_york_jaw_there(self, there, error_tolerance):
        for i in range(there[0], there[1]):
            if abs(self.york_acc[i] - self.jaw_acc[i]) < error_tolerance:
                self.york_acc[i] = self.jaw_acc[i] = \
                    (self.york_acc[i] + self.jaw_acc[i]) / 2

    def become_zeroes_there(self, there, error_tolerance):
        """In the center part, they should be exact zeros."""
        for i in range(there[0], there[1]):
            if abs(self.york_acc[i]) < error_tolerance:
                self.york_acc[i] = self.jaw_acc[i] = 0


def move_data_half_circle(data):
    l = len(data)
    return np.hstack((data[l//2:], data[:l//2]))

class DynamicData(object):
    def __init__(self, acc=TetraPakA3AccModified()):
        self.type = type(self)
        if self.type == RightYork:
            self.acc = np.array(acc.york_acc)
        elif self.type == RightJaw:
            self.acc = np.array(acc.jaw_acc)
        elif self.type == LeftYork:
            self.acc = move_data_half_circle(acc.york_acc)
        elif self.type == LeftJaw:
            self.acc = move_data_half_circle(acc.jaw_acc)
        self.m_deg = list(range(len(self.acc)))
        self.vel = self.cum_velocity_in_mm_per_s(self.acc)
        self.pos = self.cum_position_in_mm(self.vel)
        self.jer = self.diff_jerk_in_m_per_s(self.acc)

    def cum_velocity_in_mm_per_s(self, data):
        return cumtrapz(np.array(data), self.m_deg, initial=0) * \
               (0.9 / 360 * 1000)

    def cum_position_in_mm(self, data):
        return cumtrapz(np.array(data), self.m_deg, initial=0) * \
               (0.9 / 360)

    def diff_jerk_in_m_per_s(self, data):
        result = np.ones(len(self.m_deg))
        result[:-1] = np.diff(np.array(data)) / (0.9 / 360)
        result[-1] = result[0]
        return result


class RightYork(DynamicData):
    def __init__(self, a_set_of_acc=TetraPakA3AccModified()):
        DynamicData.__init__(self, a_set_of_acc)


class RightJaw(DynamicData):
    def __init__(self, a_set_of_acc=TetraPakA3AccModified()):
        DynamicData.__init__(self, a_set_of_acc)


class LeftYork(DynamicData):
    def __init__(self, a_set_of_acc=TetraPakA3AccModified()):
        DynamicData.__init__(self, a_set_of_acc)


class LeftJaw(DynamicData):
    def __init__(self, a_set_of_acc=TetraPakA3AccModified()):
        DynamicData.__init__(self, a_set_of_acc)


if __name__ == "__main__":
    a_york = RightYork()
    a_jaw = LeftJaw()
    print('the last three of york_velocity:', a_york.vel[-3],
          a_york.vel[-2], a_york.vel[-1])
    print("The length of right york p, v, a, and j are ",
          len(a_york.pos),
          len(a_york.vel),
          len(a_york.acc),
          len(a_york.jer))
    print("The length of left jaw  p, v, a, and j are ",
          len(a_jaw.pos),
          len(a_jaw.vel),
          len(a_jaw.acc),
          len(a_jaw.jer))

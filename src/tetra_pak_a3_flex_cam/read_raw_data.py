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


class TetraPakPVA(TetraPakA3AccModified):
    def __init__(self):
        TetraPakA3AccModified.__init__(self)
        self.york_acc = np.array(self.york_acc)
        self.jaw_acc = np.array(self.jaw_acc)
        self.york_vel = self.cum_velocity_in_mm_per_s(self.york_acc)
        self.jaw_vel = self.cum_velocity_in_mm_per_s(self.jaw_acc)
        self.jaw_vel += self.york_vel[220] - self.jaw_vel[220]
        self.york_pos = self.cum_position_in_mm(self.york_vel)
        self.jaw_pos = self.cum_position_in_mm(self.jaw_vel)
        self.jaw_pos += self.york_pos[230] - self.jaw_pos[230]

    def cum_velocity_in_mm_per_s(self, data):
        return cumtrapz(np.array(data), self.machine_degree, initial=0) * \
               (0.9 / 360 * 1000)

    def cum_position_in_mm(self, data):
        return cumtrapz(np.array(data), self.machine_degree, initial=0) * \
               (0.9 / 360)


if __name__ == "__main__":
    pva = TetraPakPVA()
    print('the last three of york_velocity:', pva.york_vel[-3], pva.york_vel[
        -2], pva.york_vel[-1])
    print("The length of york pva is ",
          len(pva.york_pos),
          len(pva.york_vel),
          len(pva.york_acc))
    print("The length of jaw pva is ",
          len(pva.jaw_pos),
          len(pva.jaw_vel),
          len(pva.jaw_acc))

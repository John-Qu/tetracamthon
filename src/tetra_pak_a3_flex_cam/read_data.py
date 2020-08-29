import csv
from collections import namedtuple
import numpy as np
from scipy.integrate import cumtrapz


class TetraPakA3AccMeasured(object):
    """Get the acceleration of Tetra Pak A3 Flex curve."""

    def __init__(self,
                 # path_to_csv='./tetra_pak_a3_flex_cam_acc_data_360.csv',
                 path_to_csv='./tetra_pak_a3_flex_cam_acc_data_721.csv'
                 ):
        self.m_deg = []
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
                self.m_deg.append(float(row.machine_degree))
                self.york_acc.append(float(row.york_acc_mps2))
                self.jaw_acc.append(float(row.jaw_acc_mps2))
        return self


class TetraPakA3AccModified(TetraPakA3AccMeasured):
    """Modified the measured acceleration data of Tetra Pak A3 Flex curve."""

    def __init__(self,
                 york_by_this=-0.26, jaw_by_that=-0.26,
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
        start_i = self.m_deg.index(there[0])
        stop_i = self.m_deg.index(there[1])
        for i in range(start_i, stop_i):
            if abs(self.york_acc[i] - self.jaw_acc[i]) < error_tolerance:
                self.york_acc[i] = self.jaw_acc[i] = \
                    (self.york_acc[i] + self.jaw_acc[i]) / 2

    def become_zeroes_there(self, there, error_tolerance):
        """In the center part, they should be exact zeros."""
        start_i = self.m_deg.index(there[0])
        stop_i = self.m_deg.index(there[1])
        for i in range(start_i, stop_i):
            if abs(self.york_acc[i]) < error_tolerance:
                self.york_acc[i] = self.jaw_acc[i] = 0


def move_data_half_circle(data):
    length = len(data)
    return np.hstack((data[length//2:], data[:length//2]))


class DynamicData(object):
    def __init__(self,
                 acc=TetraPakA3AccModified(),
                 # acc=TetraPakA3AccMeasured()
                 ):
        if isinstance(self, RightYork):
            self.acc = np.array(acc.york_acc)
        elif isinstance(self, RightJaw):
            self.acc = np.array(acc.jaw_acc)
        self.m_deg = acc.m_deg
        self.vel = self.cum_velocity_in_mm_per_s(self.acc)
        self.pos = self.cum_position_in_mm(self.vel)
        self.jer = self.diff_jerk_in_m_per_s(self.acc)
        self.pvaj_data = [self.pos, self.vel, self.acc, self.jer]

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
    def __init__(self):
        DynamicData.__init__(self)


class RightJaw(DynamicData):
    def __init__(self):
        DynamicData.__init__(self)
        self.updated_vel = np.ones(len(self.vel))
        self.updated_pos = np.ones(len(self.pos))

    def offset_vel(self):
        a_right_york_vel = RightYork().vel
        a_right_jaw_vel = RightJaw().vel
        check_index = self.m_deg.index(220)
        self.updated_vel = self.vel - (
                a_right_jaw_vel[check_index] - a_right_york_vel[check_index])

    def update_pos(self):
        self.updated_pos = self.cum_position_in_mm(self.updated_vel)

    def offset_pos(self):
        self.offset_vel()
        self.update_pos()
        a_right_york_pos = RightYork().pos
        check_index = self.m_deg.index(230)
        self.updated_pos = self.updated_pos - (
                self.updated_pos[check_index] - a_right_york_pos[check_index]
        )

    def modify_vel_pos(self):
        self.offset_pos()
        self.pvaj_data = [self.updated_pos, self.updated_vel,
                          self.acc, self.jer]


class LeftYork(RightYork):
    def __init__(self):
        DynamicData.__init__(self)
        for i in range(4):
            self.pvaj_data[i] = move_data_half_circle(self.pvaj_data[i])


class LeftJaw(RightJaw):
    def __init__(self):
        DynamicData.__init__(self)
        self.modify_vel_pos()
        for i in range(4):
            self.pvaj_data[i] = move_data_half_circle(self.pvaj_data[i])


class RightJawToYork(object):
    def __init__(self):
        ry = RightYork()
        rj = RightJaw()
        rj.modify_vel_pos()
        self.m_deg = ry.m_deg
        self.pvaj_data = [None, None, None, None]
        for i in range(4):
            self.pvaj_data[i] = rj.pvaj_data[i] - ry.pvaj_data[i]


class LeftJawToYork(RightJawToYork):
    def __init__(self):
        RightJawToYork.__init__(self)
        for i in range(4):
            self.pvaj_data[i] = move_data_half_circle(self.pvaj_data[i])


class AllLinksWithDynData(object):
    def __init__(self):
        self.ry = RightYork()
        self.rj = RightJaw()
        self.rj.modify_vel_pos()
        self.ly = LeftYork()
        self.lj = LeftJaw()
        self.rjy = RightJawToYork()
        self.ljy = LeftJawToYork()
        self.d = self.ry.m_deg
        self.links = [self.ry, self.rj, self.rjy, self.ly, self.lj, self.ljy]


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

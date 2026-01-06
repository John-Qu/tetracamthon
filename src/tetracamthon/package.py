import csv
import math
from collections import namedtuple
from tetracamthon.helper import trans_degree_to_time, DATA_DIR


class PackageDimension(object):
    def __init__(self,
                 path_to_package_dim_csv: str =
                 str(DATA_DIR / "package_dimensions.csv")
                 ):
        self.spec_id = []
        self.volume = []
        self.shape = []
        self.width = []
        self.depth = []
        self.height = []
        self.longitude_sealing_overlap = []
        self.web_repeated_length = []
        self.top_gap = []
        self.read_in_csv_data(path_to_package_dim_csv)

    def read_in_csv_data(self, path_to_package_dim_csv):  # test passed
        with open(path_to_package_dim_csv) as f:
            f_csv = csv.reader(f)
            headings = next(f_csv)
            Row = namedtuple('Row', headings)
            for r in f_csv:
                row = Row(*r)
                self.spec_id.append(str(row.spec_id))
                self.volume.append(int(row.volume))
                self.shape.append(str(row.shape))
                self.width.append(float(row.width))
                self.depth.append(float(row.depth))
                self.height.append(float(row.height))
                self.longitude_sealing_overlap.append(
                    float(row.longitude_sealing_overlap))
                self.web_repeated_length.append(float(row.web_repeated_length))
                self.top_gap.append(float(row.top_gap))
        return self


class Package(object):
    def __init__(self, a_package_id: str, a_spec_id: str = 'flex'):
        self.package_id = a_package_id
        self.spec_id = a_spec_id
        dims = PackageDimension()
        i = dims.spec_id.index(self.package_id)
        self.volume = dims.volume[i]
        self.shape = dims.shape[i]
        self.width = dims.width[i]
        self.depth = dims.depth[i]
        self.height = dims.height[i]
        self.longitude_sealing_overlap = dims.longitude_sealing_overlap[i]
        self.web_repeated_length = dims.web_repeated_length[i]
        self.top_gap = dims.top_gap[i]
        self.web_width = self.get_web_width()
        self.horizontal_sealing_length = self.get_horizontal_sealing_length()
        self.tube_diameter = self.get_tube_diameter()

    def get_web_width(self):
        result = (
                self.longitude_sealing_overlap + 2 * (self.width + self.depth)
        )
        return result

    def get_horizontal_sealing_length(self):
        result = self.web_repeated_length - (self.height + self.depth)
        return result

    def get_tube_diameter(self):
        result = (self.web_width - self.longitude_sealing_overlap) / math.pi
        return result


class Productivity(object):
    def __init__(self, packages_per_hour: int):
        self.packages_per_hour = packages_per_hour
        self.cycle_time = self.get_cycle_time()

    def get_cycle_time(self):
        try:
            return self.cycle_time
        except AttributeError:
            seconds_per_hour = 3600
            packages_per_cycle = 2
            return (
                    seconds_per_hour /
                    self.packages_per_hour *
                    packages_per_cycle
            )


class Production(object):
    def __init__(self, a_package, a_productivity):
        self.package = a_package
        self.productivity = a_productivity

    def get_average_velocity(self):
        result = - (
                self.package.web_repeated_length /
                (self.productivity.get_cycle_time() / 2)
        )
        return result

    def get_time_of_main_pulling(self):
        result = trans_degree_to_time(
            (264 - 194),
            cycle_time=self.productivity.get_cycle_time()
        )
        return result

    def get_time_of_pre_pulling(self):
        result = trans_degree_to_time(
            (144 - 140),
            cycle_time=self.productivity.get_cycle_time()
        )
        return result

    def get_time_of_folding(self):
        result = trans_degree_to_time(
            (194 - 144),
            cycle_time=self.productivity.get_cycle_time()
        )
        return result

    def get_extra_length_of_folding(self, ratio=0.7):
        length_fold_fully = self.package.depth / 2
        result = length_fold_fully * ratio
        return result

    def get_time_of_clamping(self):
        result = trans_degree_to_time(
            (320 - 264),
            cycle_time=self.productivity.get_cycle_time()
        )
        return result

    def get_extra_length_of_clamping(self):
        result = self.package.depth / 2 - self.package.top_gap
        return result


    def get_less_pulled_length_in_shaking_with_holding(self,
                                                       ratio: float = 1.0):
        length_hold_fully = self.package.depth / 2
        result = - length_hold_fully * ratio
        return result

    def get_less_pulled_length_in_shaking_with_folding(self,
                                                       ratio: float = 0.7):
        length_fold_fully = self.package.depth / 2
        result = - length_fold_fully * ratio
        return result

    def get_main_pulling_velocity(self):
        """With 330SQ 8000 pph, just right with Tetra's curve. But the
        algorithm is wrong."""
        average_velocity = self.get_average_velocity()
        time_of_main_pulling = self.get_time_of_main_pulling()
        result = (
                (
                        self.get_less_pulled_length_in_shaking_with_holding() +
                        self.get_less_pulled_length_in_shaking_with_folding() +
                        average_velocity * time_of_main_pulling
                ) / time_of_main_pulling
        )
        return result

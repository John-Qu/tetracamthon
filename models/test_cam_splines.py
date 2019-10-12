import unittest
from unittest import TestCase
from .cam_splines import *

class TestHelperFunctions(TestCase):
    def test_degree_to_radial(self):
        deg = 90
        self.assertEqual(degree_to_radial(deg), pi/2)
        # a_deg = np.array([0, 90, 180, 11])
        # a_rad = np.array([0, 0.5*pi, 1.0*pi, 0.0611*pi])
        # self.assertTrue((round(degree_to_radial(a_deg), 4) == a_rad).all())

    def test_radial_to_degree(self):
        pass
        # radial =

    def test_duplicate_start_end(self):
        a = [1, 2, 3, 4]
        num = 6
        d_a = [1, 1, 1, 1, 1, 1, 2, 3, 4, 4, 4, 4, 4, 4]
        self.assertEqual(duplicate_start_end(a, num), d_a)


class TestKnots(TestCase):
    def test_init(self):


if __name__ == '__main__':
    unittest.main()

# Created at 2019-09-12
#
# Author: John Qu

import math
import sympy

class Point(object):
    def __init__(self, co_type, ori_point, *coord):
        self.ori = ori_point
        if co_type == 'cas'
            self.x = coord[0]  # absolute position
            self.y = coord[1]  # absolute position
            self.r = math.sqrt(self.x**2 + self.y**2)  ## length of vector
            self.t = math.atan2(self.y, self.x)  # theta


class Linkage(object):
    idnum = 1
    def __init__(self, idnum, ori_point):
        self.id = idnum  #Todo: find how to use class attribute
        idnum += 1
        self.ori = ori_point  # Local coordination orient point.


class Joint(Point):
    NUM = 1
    def __init__(self, ori_point, (rx, ry)):
        self.ori = ori_point
        self.id = NUM
        Point.__init__(self, rx, ry)


class Vector(object):
    def __init__(self, start_point, end_point):
        self.fr = start_point
        self.to = end_point

latex(solve((60 - 100*cos(theta))**2 + (r - 100*sin(theta))**2 - 155**2, r))

theta = acos(0.01*b + 0.01*x - 1.53969262078591)
from math import *
r = 100*sin(theta)+sqrt(-400*(cos(theta)**2)+480*cos(theta) + 817)

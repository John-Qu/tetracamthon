# EXAMPLE 5-4 Using a B-Spline for a constant velocity Cam.

from sympy import pi
from sympy.abc import x
import numpy as np
from scipy.interpolate import BSpline
import matplotlib.pyplot as plt
b = BSpline.basis_element([0, 1, 2, 3, 4])
k = b.k
b.t[k:-k]
k

t = [-1, 0, 1, 1, 2]
b = BSpline.basis_element(t[1:])
def f(x):
    return np.where(x < 1, x*x, (2. - x)**2)

import matplotlib.pyplot as plt
fig, ax = plt.subplots()
x = np.linspace(0, 2, 51)
ax.plot(x, b(x), 'g', lw=3)
ax.plot(x, f(x), 'r', lw=8, alpha=0.4)
ax.grid(True)
plt.show()

class BsplineCoefficients(object):
    def __init__(self, num_of_knots, order):
        self.c = []
        self.m = order
        self.k = num_of_knots
        for i in range(self.k - self.m):
            self.c.append(symbols('c_' + str(i + 1)))

    def __str__(self):
        return str(self.c)


order = 6
degree = order - 1
knots = np.array(
    [0, 0, 0, 0, 0, 0, pi / 2, pi / 2, pi, pi, pi, pi, pi, pi])
positions = np.array([5, 5, 5, 5, 5, 5, nan, nan, 0, 0, 0, 0, 0, 0])
velocities = np.array([10, 10, 10, 10, 10, 10, nan, nan, 10, 10, 10, 10, 10, 10,])
accelerations = np.array([0, 0, 0, 0, 0, 0, nan, nan, 0, 0, 0, 0, 0, 0])
omega = 2*pi

bs = bspline_basis_set(degree, knots, x)
print("length of b-splines: ", len(bs))
b = plot(bs[0], bs[1], bs[2], bs[3], bs[4], bs[5], bs[6], bs[7], (x, 0, pi))
c = plot(bs[3], (x, 0, pi))

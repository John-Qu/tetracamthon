from scipy.interpolate import BSpline
from sympy import *
import numpy as np
import matplotlib.pyplot as plt


def degree_to_radial(degree):
    return (degree / 180 * pi).evalf()


def radial_to_degree(radial):
    return (radial / pi * 180).evalf()


order = 6
degree = order - 1
knots = [0, 0, 0, 0, 0, 0,
     pi / 4, pi / 2, 3 * pi / 4,
     pi, pi, pi, pi, pi, pi]
positions = np.array([0, 0, 0, 0, 0, 0, 0.45, 1, 0.45, 0, 0, 0, 0, 0, 0])
velocities = np.array([0, 0, 0, 0, 0, 0, nan, nan, nan, 0, 0, 0, 0, 0, 0])
accelerations = np.array([0, 0, 0, 0, 0, 0, nan, nan, nan, 0, 0, 0, 0, 0, 0])
omega = 15

bs = []
fig, ax = plt.subplots()
x = np.linspace(0, 3.1416, 101)
for i in range(len(knots)-order):
    bs_i = BSpline.basis_element(knots[i:(i+order+1)])
    s, e = float(knots[i]), float(knots[i+order])
    x = np.linspace(s, e, num=1001)
    ax.plot(x, bs_i(x), 'b', lw=2)
    bs.append(bs_i)
ax.set_title('B-splines of order 6' + '\n with knots:' + str(knots)+
             '\nGenerated with scipy.interpolate.BSpline.basis_element')
ax.grid(True)
plt.show()

# a = 1
# b = 10
# n = 9
# x = np.linspace(a, b, num=n)
# i = 1
# s, e = knots[i], knots[i + order]
# print(s, e)
# print(str(i) + 'th start and end: ' + str(start) +', '+str(end))
# x = np.linspace(float(str(s)), float(str(e)))
# x = np.linspace(float(s), float(e))
# x = np.linspace(0, 0.785398163397448)

# bsv = []
# for i in range(len(bs)):
#     bsv_i = bs[i].derivative()
#     bsv.append(bsv_i)
#
# b4knots = np.array([0, 0, pi / 4, pi / 2, 3 * pi / 4, pi, pi])
# b4 = BSpline.basis_element(b4knots)
# fig, ax = plt.subplots()
# x = np.linspace(0, 3.14, 101)
# ax.plot(x, b4(x), 'g', lw=3)
# ax.grid(True)
# plt.show()


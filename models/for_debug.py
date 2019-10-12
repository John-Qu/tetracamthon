from sympy import *
from sympy.abc import x
import numpy as np

order = 6
degree = order - 1
knots = np.array(
    [0, 0,
     pi / 4, pi / 2, 3 * pi / 4,
     pi, pi])
b4 = bspline_basis(degree, tuple(knots), 0, x)
print(latex(b4))
plot(b4, (x, 0, 180))

# knots = tuple([0, 0, 0, 1, 1, 2, 2, 2])
# order = len(knots) - 1
# degree = order - 1
# bs = bspline_basis_set(degree, knots, x)
# print(latex(bs))
# plot(bs[0], (x, 0, knots[-1]),
#      title="B-spline of order "+str(order)+"\nwith knots: "+str(knots))
# import matplotlib.pyplot as plt
# fig, ax = plt.subplots()
# x = np.linspace(0, 2, 51)
# ax.plot(x, b(x), 'g', lw=3)
# ax.plot(x, f(x), 'r', lw=8, alpha=0.4)
# ax.grid(True)
# plt.show()

from scipy.interpolate import BSpline
b = BSpline.basis_element([0, 1, 2, 3, 4])

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


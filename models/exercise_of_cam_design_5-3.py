# EXAMPLE 5-3 Using a B-Spline for a Single-Dwell Cam.

from sympy import *
from sympy.abc import x
import numpy as np
import matplotlib.pyplot as plt


def move_sympyplot_to_axes(p, ax):
    backend = p.backend(p)
    backend.ax = ax
    backend.process_series()
    backend.ax.spines['right'].set_color('none')
    backend.ax.spines['bottom'].set_position('zero')
    backend.ax.spines['top'].set_color('none')
    plt.close(backend.fig)


def degree_to_radial(degree):
    return (degree / 180 * pi).evalf()


def radial_to_degree(radial):
    return (radial / pi * 180).evalf()


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
piecewise_polynomials = []
knots = np.array(
    [0, 0, 0, 0, 0, 0, pi / 4, pi / 2, 3 * pi / 4, pi, pi, pi, pi, pi, pi])
positions = np.array([0, 0, 0, 0, 0, 0, 0.45, 1, 0.45, 0, 0, 0, 0, 0, 0])
velocities = np.array([0, 0, 0, 0, 0, 0, nan, nan, nan, 0, 0, 0, 0, 0, 0])
accelerations = np.array([0, 0, 0, 0, 0, 0, nan, nan, nan, 0, 0, 0, 0, 0, 0])
omega = 15

bs = bspline_basis_set(degree, knots, x)
c = BsplineCoefficients(len(knots), order)
p = sum([c.c[i] * bs[i] for i in range(len(bs))])
v = diff(p, x) * omega
a = diff(v, x) * omega
j = diff(a, x) * omega
# print(latex(v))
pf = lambdify(x, p)
vf = lambdify(x, v)
af = lambdify(x, a)

ps_b9 = lambdify(x, bs[8])
plot(bs[8], (x, 0, pi))
print(latex(bs[8]))
for i in range(len(c.c)):
    var.append(c.c[i])

equations = []
for i in range(order, len(knots) - order):
    equations.append(Eq(pf(knots[i]).evalf(), positions[i]))
equations.append(Eq(pf(knots[0]).evalf(), positions[0]))
equations.append(Eq(vf(knots[0]).evalf(), velocities[0]))
equations.append(Eq(af(knots[0]).evalf(), accelerations[0]))
# epsilon = 1e-15
epsilon = 0
equations.append(Eq(pf(knots[-1] - epsilon).evalf(), positions[-1]))
equations.append(Eq(vf(knots[-1] - epsilon).evalf(), velocities[-1]))
equations.append(Eq(af(knots[-1] - epsilon).evalf(), accelerations[-1]))

solutions = solve(equations, var)
s_expr = p.subs([(c.c[i], solutions[c.c[i]]) for i in range(len(bs) - 3)])
s_expr = s_expr.subs([(c.c[i], 0) for i in range(len(bs) - 3, len(bs))])
# print(latex(s_expr))
p1 = plot(s_expr, (x, 0, pi),
          title="Displacement",
          ylabel="(in)",
          show=False)
# for i in range(len(bs)):
#     b = plot(bs[i], (x, 0, pi),
#              title="b_" + str(i),
#              ylabel="(in)",
#              show=False)
#     p1.extend(b)

p1.show()
b = plot(bs[0], bs[1], bs[2], bs[3], bs[4], bs[5], bs[6], bs[7], bs[8], (x, 0, pi))
b4knots = np.array([0, 0, pi / 4, pi / 2, 3 * pi / 4, pi, pi])
b4 = bspline_basis(degree, b4knots, 0, x)
print(latex(bs[3]))
print(latex(b4))
plot(b4, (x, 0, pi))

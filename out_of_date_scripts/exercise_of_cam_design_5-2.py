# EXAMPLE 5-2 Using a general spline for a constant velocity critical path motion.

from sympy import *
from sympy.abc import x
import numpy as np


def degree_to_radial(degree):
    return (degree/180*pi).evalf()


def radial_to_degree(radial):
    return (radial/pi*180).evalf()


class Coefficients(object):
    def __init__(self, id, order = 6):
        self.c = []
        self.m = order
        for i in range(self.m, 0,-1):
            self.c.append(symbols('C_' + str(id) + str(i)))

    def __str__(self):
        return str(self.c)


# theta = symbols('theta')
order = 6
degree = order - 1
piecewise_polynomials = []
# knots = np.array([0, 45, 90, 135, 180])
# knots = np.array([0, degree_to_radial(14.04), pi/2, pi])
# positions = np.array([5, 5.25, nan, 0])
# velocities = np.array([10, 0, nan, 10])
# accelerations = np.array([0, nan, nan, 0])
knots = np.array([0, pi/2, pi])  # note 14.04 is not a knot
positions = np.array([5, nan, 0])
velocities = np.array([10, nan, 10])
accelerations = np.array([0, nan, 0])
omega = 2*pi

p, v, a, jerk, ping = [], [], [], [], []
c = []
var = []
for i in range(1, len(knots)):
    c.append(Coefficients(i))
    p_i = c[-1].c[-1]
    var.append(c[-1].c[0])
    for j in range(degree):
        p_i += c[-1].c[j]*(x - knots[i-1])**(degree - j)
        var.append(c[-1].c[j+1])
    v_i = diff(p_i, x)*omega
    a_i = diff(v_i, x)*omega
    jerk_i = diff(a_i, x)*omega
    ping_i = diff(jerk_i, x)*omega
    p.append(p_i)
    v.append(v_i)
    a.append(a_i)
    jerk.append(jerk_i)
    ping.append(ping_i)

pf, vf, af, jerkf, pingf = [], [], [], [], []
for i in range(len(knots) - 1):
    pf.append(lambdify(x, p[i]))
    vf.append(lambdify(x, v[i]))
    af.append(lambdify(x, a[i]))
    jerkf.append(lambdify(x, jerk[i]))
    pingf.append(lambdify(x, ping[i]))

equations = []
# interpolation equations
# release the interpolation relation at 90 degree
# for i in range(1, len(knots)-1):
#     equations.append(Eq(pf[i](knots[i]).evalf(), positions[i]))
i = 0
equations.append(Eq(pf[i](degree_to_radial(14.04)).evalf(), 5.25))
equations.append(Eq(vf[i](degree_to_radial(14.04)).evalf(), 0))
# smoothness equations 5.5 5.6
i = 1
equations.append(Eq(pf[i-1](knots[i]).evalf(), pf[i](knots[i]).evalf()))
equations.append(Eq(vf[i-1](knots[i]).evalf(), vf[i](knots[i]).evalf()))
equations.append(Eq(af[i-1](knots[i]).evalf(), af[i](knots[i]).evalf()))
equations.append(Eq(jerkf[i-1](knots[i]).evalf(), jerkf[i](knots[i]).evalf()))
# equations.append(Eq(pingf[i - 1](knots[i]).evalf(), pingf[i](knots[i]).evalf()))
# boundary conditions
equations.append(Eq(pf[0](knots[0]).evalf(), positions[0]))
equations.append(Eq(vf[0](knots[0]).evalf(), velocities[0]))
equations.append(Eq(af[0](knots[0]).evalf(), accelerations[0]))
equations.append(Eq(pf[-1](knots[-1]).evalf(), positions[-1]))
equations.append(Eq(vf[-1](knots[-1]).evalf(), velocities[-1]))
equations.append(Eq(af[-1](knots[-1]).evalf(), accelerations[-1]))

print(len(equations))
print(len(var))
solutions = solve(equations, var)

d_expr = []
for i in range(len(knots)-1):
    d_expr.append(p[i].subs([(c[i].c[j], round(solutions[c[i].c[j]], 4)) for j in range(order)]))

p_of_x = Piecewise((0, x < knots[0]),
                       (d_expr[0], x <= knots[1]),
                       (d_expr[1], x <= knots[2]),
                       (0, True))

import matplotlib.pyplot as plt

def move_sympyplot_to_axes(p, ax):
    backend = p.backend(p)
    backend.ax = ax
    backend.process_series()
    backend.ax.spines['right'].set_color('none')
    backend.ax.spines['bottom'].set_position('zero')
    backend.ax.spines['top'].set_color('none')
    plt.close(backend.fig)


v_of_x = diff(p_of_x, x)*omega
a_of_x = diff(v_of_x, x)*omega
j_of_x = diff(a_of_x, x)*omega
p1 = plot(p_of_x, (x, 0, pi),
          title="Displacement",
          ylabel="(in)",
          show=False)
p2 = plot(v_of_x, (x, 0, pi),
          title="Velocity",
          ylabel="(in/sec)",
          show=False)
p3 = plot(a_of_x, (x, 0, pi),
          title="Acceleration",
          ylabel="(in/sec^2)",
          show=False)
p4 = plot(j_of_x, (x, 0, pi),
          title="Jerk",
          ylabel="(in/sec^3)",
          show=False)
fig, (ax1,ax2,ax3,ax4) = plt.subplots(nrows=4)
move_sympyplot_to_axes(p1, ax1)
move_sympyplot_to_axes(p2, ax2)
move_sympyplot_to_axes(p3, ax3)
move_sympyplot_to_axes(p4, ax4)

plt.show()



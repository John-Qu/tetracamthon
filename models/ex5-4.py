# EXAMPLE 5-4 Using a B-Spline for a constant velocity Cam.

from sympy import pi, nan, bspline_basis_set, diff, symbols, \
    plot, lambdify, Eq, solve, latex, Piecewise, piecewise_fold, simplify
from sympy.abc import x
import matplotlib.pyplot as plt
import numpy as np

def degree_to_radial(degree):
    return (degree / 180 * pi).evalf()


def radial_to_degree(radial):
    return (radial / pi * 180).evalf()


def move_sympyplot_to_axes(p, ax):
    backend = p.backend(p)
    backend.ax = ax
    backend.process_series()
    backend.ax.spines['right'].set_color('none')
    backend.ax.spines['bottom'].set_position('zero')
    backend.ax.spines['top'].set_color('none')
    plt.close(backend.fig)


class CurveOfBsplines(object):
    def __init__(self, knots, order):
        self.knots = tuple(knots)
        self.c = []
        self.order = order
        self.degree = order - 1
        self.k = len(knots)
        for i in range(self.k - self.order):
            self.c.append(symbols('c_' + str(i + 1)))
        self.bs = bspline_basis_set(self.degree, self.knots, x)
        self.p = sum([self.c[i] * self.bs[i] for i in range(len(self.bs))])

    def __str__(self):
        return latex(self.get_position_expr())

    def plot_bsplines(self):
        pl = plot(self.bs[0], (x, 0, pi),
                  title = 'B-splines of order ' + str(self.order) +
                          '\n with knots:' + str(self.knots),
                  ylabel = '', xlabel = 'rad')
        for i in range(1, len(self.bs)):
            pl.extend(plot(self.bs[i], (x, 0, pi)))
        pl.show()

    def get_position_expr(self):
        return self.p

    def get_velocity_expr(self, omega=1):
        return diff(self.p, x, 1) * omega

    def get_acceleration_expr(self, omega=1):
        return diff(self.p, x, 2) * omega**2

    def get_jerk_expr(self, omega=1):
        return diff(self.p, x, 3) * omega**3

    def get_position_function(self):
        return lambdify(x, self.get_position_expr())

    def get_velocity_function(self, omega=1):
        return lambdify(x, self.get_velocity_expr() * omega)

    def get_acceleration_function(self, omega=1):
        return lambdify(x, self.get_acceleration_expr() * omega**2)

    def get_jerk_function(self, omega=1):
        return lambdify(x, self.get_jerk_expr() * omega**3)

    def get_position_final_expr(self, solutions, r=4):
        return self.get_position_expr().subs(
            [(self.c[i], round(solutions[self.c[i]], r))
             for i in range(len(self.c))
             ])

    def get_velocity_final_expr(self, solutions, r=4, omega=1):
        return self.get_velocity_expr(omega=omega).subs(
            [(self.c[i], round(solutions[self.c[i]], r))
             for i in range(len(self.c))
             ])

    def get_acceleration_final_expr(self, solutions, r=4, omega=1):
        return self.get_acceleration_expr(omega=omega).subs(
            [(self.c[i], round(solutions[self.c[i]], r))
             for i in range(len(self.c))
             ])

    def get_jerk_final_expr(self, solutions, r=4, omega=1):
        return self.get_jerk_expr(omega=omega).subs(
            [(self.c[i], round(solutions[self.c[i]], r))
             for i in range(len(self.c))
             ])

    def plot_svaj(self, solutions, omega=1,
                  start=0.0, end=float(pi)):
        p1 = plot(self.get_position_final_expr(solutions),
                  (x, start, end),
                  title="Position",
                  ylabel="(in)",
                  show=False)
        p2 = plot(self.get_velocity_final_expr(solutions, omega=omega),
                  (x, start, end),
                  title="Velocity",
                  ylabel="(in/sec)",
                  show=False)
        p3 = plot(self.get_acceleration_final_expr(solutions, omega=omega),
                  (x, start, end),
                  title="Acceleration",
                  ylabel="(in/sec^2)",
                  show=False)
        p4 = plot(self.get_jerk_final_expr(solutions, omega=omega),
                  (x, start, end),
                  title="Jerk",
                  ylabel="(in/sec^3)",
                  show=False)
        fig, (ax1, ax2, ax3, ax4) = plt.subplots(nrows=4)
        move_sympyplot_to_axes(p1, ax1)
        move_sympyplot_to_axes(p2, ax2)
        move_sympyplot_to_axes(p3, ax3)
        move_sympyplot_to_axes(p4, ax4)
        plt.show()


def plot_whole_svaj(position, velocity, acceleration, jerk,
                     start=0, end=2*pi):
    p1 = plot(position, (x, start, end),
              title="Position",
              ylabel="(in)",
              show=False)
    p2 = plot(velocity, (x, start, end),
              title="Velocity",
              ylabel="(in/sec)",
              show=False)
    p3 = plot(acceleration, (x, start, end),
              title="Acceleration",
              ylabel="(in/sec^2)",
              show=False)
    p4 = plot(jerk, (x, start, end),
              title="Jerk",
              ylabel="(in/sec^3)",
              show=False)
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(nrows=4)
    move_sympyplot_to_axes(p1, ax1)
    move_sympyplot_to_axes(p2, ax2)
    move_sympyplot_to_axes(p3, ax3)
    move_sympyplot_to_axes(p4, ax4)
    plt.show()


order = 6
knots = (
    [0, 0, 0, 0, 0, 0, pi / 2, pi / 2, pi, pi, pi, pi, pi, pi])
positions = ([5, 5, 5, 5, 5, 5, nan, nan, 0, 0, 0, 0, 0, 0])
velocities = ([10, 10, 10, 10, 10, 10, nan, nan, 10, 10, 10, 10, 10, 10,])
accelerations = ([0, 0, 0, 0, 0, 0, nan, nan, 0, 0, 0, 0, 0, 0])
omega = 2*pi
c = CurveOfBsplines(knots, order)
pf = c.get_position_function()
vf = c.get_velocity_function(omega=omega)
af = c.get_acceleration_function(omega=omega)
# write equations
equations = []
equations.append(Eq(pf(knots[0]).evalf(), positions[0]))
equations.append(Eq(vf(knots[0]).evalf(), velocities[0]))
equations.append(Eq(af(knots[0]).evalf(), accelerations[0]))
equations.append(Eq(pf(knots[-1] - 1e-10).evalf(), positions[-1]))
equations.append(Eq(vf(knots[-1] - 1e-10).evalf(), velocities[-1]))
equations.append(Eq(af(knots[-1] - 1e-10).evalf(), accelerations[-1]))
equations.append(Eq(pf(degree_to_radial(14.04)), 5.25))
equations.append(Eq(vf(degree_to_radial(14.04)), 0))

solutions = solve(equations, c.c)

# c.plot_svaj(solutions, omega=omega)

position_half_expr = c.get_position_final_expr(solutions)
position_half_piecewise = position_half_expr.simplify()  # Mul type to Piecewise type
# position_curve = Piecewise(
#     (-542.87*x**5/pi**5 + 667.654*x**4/pi**4 - 82.024*x**3/pi**3 - 160.0*x**2/pi**2 + 50.0*x/pi, Eq(x, pi/2)),
#     (-622.87*x**5/pi**5 + 907.654*x**4/pi**4 - 362.024*x**3/pi**3 + 5.0*x/pi + 5.0, (x >= 0) & (x <= pi/2)),
#     (-112.694*x**5/pi**5 + 452.966*x**4/pi**4 - 728.088*x**3/pi**3 + 593.408*x**2/pi**2 - 245.946*x/pi + 40.354, (x <= pi) & (x >= pi/2)),
#     (0, True))
position_whole_piecewise = Piecewise(
    (-622.87*x**5/pi**5 + 907.654*x**4/pi**4 - 362.024*x**3/pi**3 + 5.0*x/pi + 5.0, (x >= 0) & (x <= pi/2)),
    (-112.694*x**5/pi**5 + 452.966*x**4/pi**4 - 728.088*x**3/pi**3 + 593.408*x**2/pi**2 - 245.946*x/pi + 40.354, (x <= pi) & (x >= pi/2)),
    (10*x/(2*pi) - 5, (x <= 2*pi) & (x >= pi)),
    (0, True))
# position_curve = Piecewise(
#     (-622.87*x**5/pi**5 + 907.654*x**4/pi**4 - 362.024*x**3/pi**3 + 5.0*x/pi + 5.0, (x >= 0) & (x <= pi/2)),
#     (-112.694*x**5/pi**5 + 452.966*x**4/pi**4 - 728.088*x**3/pi**3 + 593.408*x**2/pi**2 - 245.946*x/pi + 40.354, (x <= pi) & (x >= pi/2)),
#     (0, True))
velocity_curve = diff(position_curve, x)*omega
acceleration_curve = diff(position_curve, x, 2)*omega**2
jerk_curve = diff(position_curve, x, 3)*omega**3
plot_whole_svaj(position_curve, velocity_curve, acceleration_curve, jerk_curve)

# v_additional = Piecewise((0, x <= pi), (10, x <= 2*pi), (0, True))
# p_additional = Piecewise((0, x <= pi), (10*x/(2*pi) - 5, x <= 2*pi), (0, True))
# position_point = Piecewise((-542.87*x**5/pi**5 + 667.654*x**4/pi**4 - 82.024*x**3/pi**3 - 160.0*x**2/pi**2 + 50.0*x/pi, Eq(x, pi/2)), (0, True))

# whole_v = piecewise_fold(v + v_additional)
# whole_p = piecewise_fold(p_piecewise + p_additional)
# whole_p = piecewise_fold(position_curve + p_additional)
# whole_p = piecewise_fold(position_curve - position_point)
# print(whole_p)
# plot(whole_p, (x, 0, 2.01*pi))

# p_func = lambdify(x, whole_p)
# v_func = lambdify(x, whole_v)
#
# p1 = plot(position_curve,
#           (x, 0, 2.01*pi),
#           title="Position",
#           ylabel="(in)",
#           show=True)
#
# p2 = plot(whole_v,
#           (x, 0, 2.01*pi),
#           title="Velocity",
#           ylabel="(in/sec)",
#           show=False)
# fig, (ax1, ax2) = plt.subplots(nrows=2)
# move_sympyplot_to_axes(p1, ax1)
# move_sympyplot_to_axes(p2, ax2)
# ax1.grid(True)
# plt.show()


fig, ax = plt.subplots()
x = np.linspace(float(0), float(2*pi), 10001)
position_func = lambdify(x, position_curve)
velocity_func
ax.plot(x, v_func(x), 'g', lw=3)
ax.plot(x, p_func(x), 'r', lw=3, alpha=0.4)
ax.grid(True)
plt.show()


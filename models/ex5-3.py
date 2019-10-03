from sympy import pi, nan, bspline_basis_set, diff, symbols, \
    plot, lambdify, Eq, solve, latex
from sympy.abc import x
import matplotlib.pyplot as plt


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

    def plot_svaj(self, solutions, omega=1):
        p1 = plot(self.get_position_final_expr(solutions),
                  (x, self.knots[0], self.knots[-1]),
                  title="Position",
                  ylabel="(in)",
                  show=False)
        p2 = plot(self.get_velocity_final_expr(solutions, omega=omega),
                  (x, self.knots[0], self.knots[-1]),
                  title="Velocity",
                  ylabel="(in/sec)",
                  show=False)
        p3 = plot(self.get_acceleration_final_expr(solutions, omega=omega),
                  (x, self.knots[0], self.knots[-1]),
                  title="Acceleration",
                  ylabel="(in/sec^2)",
                  show=False)
        p4 = plot(self.get_jerk_final_expr(solutions, omega=omega),
                  (x, self.knots[0], self.knots[-1]),
                  title="Jerk",
                  ylabel="(in/sec^3)",
                  show=False)
        fig, (ax1, ax2, ax3, ax4) = plt.subplots(nrows=4)
        move_sympyplot_to_axes(p1, ax1)
        move_sympyplot_to_axes(p2, ax2)
        move_sympyplot_to_axes(p3, ax3)
        move_sympyplot_to_axes(p4, ax4)
        plt.show()


# initialize
order = 6
knots = (0, 0, 0, 0, 0, 0, pi / 4, pi / 2, 3 * pi / 4, pi, pi, pi, pi, pi, pi)
positions = (0, 0, 0, 0, 0, 0, 0.45, 1, 0.45, 0, 0, 0, 0, 0, 0)
velocities = (0, 0, 0, 0, 0, 0, nan, nan, nan, 0, 0, 0, 0, 0, 0)
accelerations = (0, 0, 0, 0, 0, 0, nan, nan, nan, 0, 0, 0, 0, 0, 0)
omega = 15
# build splines
c = CurveOfBsplines(knots, order)
pf = c.get_position_function()
vf = c.get_velocity_function(omega=omega)
af = c.get_acceleration_function(omega=omega)
# write equations
equations = []
# interior knots interpolation equations
for i in range(order, len(knots)-order):
    equations.append(Eq(pf(knots[i]).evalf(), positions[i]))
# boundary knots condition equations
equations.append(Eq(pf(knots[0]).evalf(), positions[0]))
equations.append(Eq(vf(knots[0]).evalf(), velocities[0]))
equations.append(Eq(af(knots[0]).evalf(), accelerations[0]))
equations.append(Eq(pf(knots[-1] - 1e-10).evalf(), positions[-1]))
equations.append(Eq(vf(knots[-1] - 1e-10).evalf(), velocities[-1]))
equations.append(Eq(af(knots[-1] - 1e-10).evalf(), accelerations[-1]))

solutions = solve(equations, c.c)

c.plot_svaj(solutions, omega=omega)

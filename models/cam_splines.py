from sympy import pi, nan, bspline_basis_set, diff, symbols, \
    plot, lambdify, Eq, solve, latex, Piecewise, piecewise_fold, simplify
from sympy.abc import x
import matplotlib.pyplot as plt
import numpy as np
from .helper_functions import degree_to_time, time_to_degree, \
    move_sympyplot_to_axes, duplicate_start_end, radial_to_time, time_to_time, \
    time_to_radial


class Knots(object):
    def __init__(self, original_knots, id=1, order=6,
                 original_knots_type="deg",
                 cycle_time=0.9):
        duplicated_knots = duplicate_start_end(original_knots, order)
        convert_what_to_time = {'deg': degree_to_time,
                                'rad': radial_to_time,
                                'time': time_to_time}
        self.id = id
        self.cycle_time = cycle_time
        self.order = order
        self.knots_in_time = tuple(
            convert_what_to_time[original_knots_type](duplicated_knots,
                                                      self.cycle_time))
        self.knots_in_deg = tuple(time_to_degree(self.knots_in_time,
                                                 self.cycle_time))
        self.knots_in_rad = tuple(time_to_radial(self.knots_in_time,
                                                 self.cycle_time))
        self.knots_in_nor = tuple([self.knots_in_time[i] /
                                   abs(self.knots_in_time[-1] -
                                       self.knots_in_time[0])
                                   for i in range(len(
                self.knots_in_time))])
        self.num_of_knots = len(self.knots_in_time)

    def __str__(self):
        print_out_knots = "Knots in degree: {0}\n" \
                          "Knots in radial: {1}\n" \
                          "Knots in time: {2}\n" \
                          "Knots normalized: {3}".format(
            str(self.knots_in_deg),
            str(self.knots_in_rad),
            str(self.knots_in_time),
            str(self.knots_in_nor))
        return print_out_knots


class BasisSplines(object):
    def __init__(self, knots_objects):
        self.id = knots_objects.id
        self.knots = knots_objects.knots_in_time
        self.order = knots_objects.order
        self.degree = self.order - 1
        self.num_of_knots = knots_objects.num_of_knots
        self.coefficients = []
        self.num_of_coefficients = self.num_of_knots - self.order
        for i in range(self.num_of_coefficients):
            self.coefficients.append(symbols('c_' +
                                             str(self.id) + str(i + 1)))
        self.basis_splines = bspline_basis_set(self.degree, self.knots, x)

    def __str__(self):
        return latex(self.basis_splines)

    def plot_basis_splines(self):
        pl = plot(self.basis_splines[0], (x, self.knots[0], self.knots[-1]),
                  title='B-splines of order ' + str(self.order) +
                        '\n with knots:' + str(self.knots),
                  ylabel='', xlabel='second')
        for i in range(1, self.num_of_coefficients):
            pl.extend(plot(self.basis_splines[i],
                           (x, self.knots[0], self.knots[-1]), show=False))
        pl.show()


class SplineExpr(object):
    def __init__(self, basis_splines_object):
        self.bs = basis_splines_object
        self.expr_dict = {}

    def get_position_expr(self):
        self.expr_dict['position'] = \
            self.expr_dict.get('position',
                               sum([self.bs.coefficients[i] *
                                    self.bs.basis_splines[i]
                                    for i in
                                    range(self.bs.num_of_coefficients)]))
        return self.expr_dict['position']

    def get_velocity_expr(self):
        self.expr_dict['velocity'] = \
            self.expr_dict.get('velocity',
                               diff(self.get_position_expr(), x, 1))
        return self.expr_dict['velocity']

    def get_acceleration_expr(self):
        self.expr_dict['acceleration'] = \
            self.expr_dict.get('acceleration',
                               diff(self.get_position_expr(), x, 2))
        return self.expr_dict['acceleration']

    def get_jerk_expr(self):
        self.expr_dict['jerk'] = \
            self.expr_dict.get('jerk',
                               diff(self.get_position_expr(), x, 3))
        return self.expr_dict['jerk']

    def get_ping_expr(self):
        self.expr_dict['ping'] = \
            self.expr_dict.get('ping',
                               diff(self.get_position_expr(), x, 4))
        return self.expr_dict['ping']

    def get_puff_expr(self):
        self.expr_dict['puff'] = \
            self.expr_dict.get('puff',
                               diff(self.get_position_expr(), x, 5))
        return self.expr_dict['puff']

    def __str__(self):
        position_piecewise = self.get_position_expr().simplify()
        # velocity_piecewise = self.velocity.simplify()
        return "Position: \n" + str(position_piecewise)
        # "\nVelocity: \n" + str(velocity_piecewise)

    def get_position_functional(self):
        return lambdify(x, self.get_position_expr())

    def get_velocity_functional(self):
        return lambdify(x, self.get_velocity_expr())

    def get_acceleration_functional(self):
        return lambdify(x, self.get_acceleration_expr())

    def get_jerk_functional(self):
        return lambdify(x, self.get_jerk_expr())

    def get_ping_functional(self):
        return lambdify(x, self.get_ping_expr())

    def get_puff_functional(self):
        return lambdify(x, self.get_puff_expr())


class SplineFinalExpr(SplineExpr):
    def __init__(self, spline_expr_object, solutions, round_to=4):
        SplineExpr.__init__(self, spline_expr_object.bs)
        self.seo = spline_expr_object
        self.co = spline_expr_object.bs.coefficients
        self.solutions = solutions
        self.r = round_to
        self.knots = self.seo.bs.knots
        self.final_expr_dict = {}

    def get_position_expr(self):
        self.final_expr_dict['position'] = \
            self.final_expr_dict.get('position',
                                     self.seo.get_position_expr().subs(
                                         [(self.co[i],
                                           self.solutions[self.co[i]])
                                          for i in range(len(self.co))]))
        return self.final_expr_dict['position']

    def get_velocity_expr(self):
        self.final_expr_dict['velocity'] = \
            self.final_expr_dict.get('velocity',
                                     self.seo.get_velocity_expr().subs(
                                         [(self.co[i],
                                           self.solutions[self.co[i]])
                                          for i in range(len(self.co))]))
        return self.final_expr_dict['velocity']

    def get_acceleration_expr(self):
        self.final_expr_dict['acceleration'] = \
            self.final_expr_dict.get('acceleration',
                                     self.seo.get_position_expr().subs(
                                         [(self.co[i],
                                           self.solutions[self.co[i]])
                                          for i in range(len(self.co))]))
        return self.final_expr_dict['acceleration']

    def get_jerk_expr(self):
        self.final_expr_dict['jerk'] = \
            self.final_expr_dict.get('jerk',
                                     self.seo.get_jerk_expr().subs(
                                         [(self.co[i],
                                           self.solutions[self.co[i]])
                                          for i in range(len(self.co))]))
        return self.final_expr_dict['jerk']

    def get_ping_expr(self):
        self.final_expr_dict['ping'] = \
            self.final_expr_dict.get('jerk',
                                     self.seo.get_ping_expr().subs(
                                         [(self.co[i],
                                           self.solutions[self.co[i]])
                                          for i in range(len(self.co))]))
        return self.final_expr_dict['ping']

    def get_puff_expr(self):
        self.final_expr_dict['puff'] = \
            self.final_expr_dict.get('puff',
                                     self.seo.get_puff_expr().subs(
                                         [(self.co[i],
                                           self.solutions[self.co[i]])
                                          for i in range(len(self.co))]))
        return self.final_expr_dict['puff']

    def __str__(self):
        position_piecewise = self.get_position_expr().simplify()
        # velocity_piecewise = self.velocity.simplify()
        return "Position: \n" + str(position_piecewise)
        # "\nVelocity: \n" + str(velocity_piecewise)

    def get_position_functional(self):
        return lambdify(x, self.get_position_expr())

    def get_velocity_functional(self):
        return lambdify(x, self.get_velocity_expr())

    def get_acceleration_functional(self):
        return lambdify(x, self.get_acceleration_expr())

    def get_jerk_functional(self):
        return lambdify(x, self.get_jerk_expr())

    def get_ping_functional(self):
        return lambdify(x, self.get_ping_expr())

    def get_puff_functional(self):
        return lambdify(x, self.get_puff_expr())

    def plot_svaj(self, omega=1):
        p1 = plot(self.get_position_expr(),
                  (x, self.knots[0], self.knots[-1]),
                  title="Position",
                  ylabel="(mm)",
                  show=False)
        p2 = plot(self.get_velocity_expr(),
                  (x, self.knots[0], self.knots[-1]),
                  title="Velocity",
                  ylabel="(mm/sec)",
                  show=False)
        p3 = plot(self.get_acceleration_expr(),
                  (x, self.knots[0], self.knots[-1]),
                  title="Acceleration",
                  ylabel="(mm/sec^2)",
                  show=False)
        p4 = plot(self.get_jerk_expr(),
                  (x, self.knots[0], self.knots[-1]),
                  title="Jerk",
                  ylabel="(mm/sec^3)",
                  show=False)
        fig, (ax1, ax2, ax3, ax4) = plt.subplots(nrows=4)
        move_sympyplot_to_axes(p1, ax1)
        move_sympyplot_to_axes(p2, ax2)
        move_sympyplot_to_axes(p3, ax3)
        move_sympyplot_to_axes(p4, ax4)
        plt.show()

    def plot_numerical(self, num=100):
        t = np.linspace(self.knots[0], self.knots[-1],
                        num, endpoint=True)
        degree = time_to_degree(t)
        position = self.get_position_functional()(t)
        velocity = self.get_velocity_functional()(t)
        acceleration = self.get_acceleration_functional()(t)
        jerk = self.get_jerk_functional()(t)
        fig = plt.figure(figsize=(15, 12), dpi=80)
        fig.suptitle('SVAJ curve with knots on \n' +
                     str(time_to_degree(
                         self.knots[
                             (self.seo.bs.order - 1):(-self.seo.bs.order + 1)
                         ])),
                     fontsize='xx-large')
        plt.subplot(4, 1, 1)
        plt.grid()
        plt.ylabel("Position (mm)")
        plt.plot(degree, position,
                 color="blue", linewidth=3.0, linestyle="-")
        plt.xlim(0.0, 360.0)
        plt.xticks(np.linspace(0, 360, 37, endpoint=True))
        # plt.ylim(min(position)-10, max(position)+10)
        # plt.yticks(np.linspace(-2000, 2000, 9, endpoint=True))
        plt.subplot(4, 1, 2)
        plt.grid()
        plt.ylabel("Velocity (mm/s)")
        plt.plot(degree, velocity,
                 color="blue", linewidth=3.0, linestyle="-")
        plt.xlim(0.0, 360.0)
        plt.xticks(np.linspace(0, 360, 37, endpoint=True))
        # plt.ylim(min(position)-10, max(position)+10)
        # plt.yticks(np.linspace(-2000, 2000, 9, endpoint=True))
        plt.subplot(4, 1, 3)
        plt.grid()
        plt.ylabel("Acceleration (m/s^3)")
        plt.plot(degree, acceleration,
                 color="blue", linewidth=3.0, linestyle="-")
        plt.xlim(0.0, 360.0)
        plt.xticks(np.linspace(0, 360, 37, endpoint=True))
        # plt.ylim(min(position)-10, max(position)+10)
        # plt.yticks(np.linspace(-2000, 2000, 9, endpoint=True))
        plt.subplot(4, 1, 4)
        plt.grid()
        plt.ylabel("Jerk (mm)")
        plt.plot(degree, jerk,
                 color="blue", linewidth=3.0, linestyle="-")
        plt.xlim(0.0, 360.0)
        plt.xticks(np.linspace(0, 360, 37, endpoint=True))
        # plt.ylim(min(position)-10, max(position)+10)
        # plt.yticks(np.linspace(-2000, 2000, 9, endpoint=True))
        plt.savefig("svaj_of_jaw_to_york.png", dpi=720)


class SplineNumerical(object):
    pass


class SolveSplines(object):
    def __init__(self, knots_object):
        self.knots = knots_object
        self.bs = BasisSplines(self.knots)
        self.spline = SplineExpr(self.bs)
        self.pf = self.spline.get_position_functional()
        self.vf = self.spline.get_velocity_functional()
        self.af = self.spline.get_acceleration_functional()
        self.jf = self.spline.get_jerk_functional()
        self.pif = self.spline.get_ping_functional()
        self.puf = self.spline.get_puff_functional()


class JawToYork(SolveSplines):
    def __init__(self, knots_object):
    # knots = Knots([0, 43, 84, 137, 160, 194, 265, 318, 337, 360], id=1, original_knots_type="deg")
        SolveSplines.__init__(self, knots_object)
        self.equations = [
            Eq(self.pf(degree_to_time(43)), -131),
            Eq(self.vf(degree_to_time(43)), 0),
            Eq(self.pf(degree_to_time(90)), -41.1),
            Eq(self.pf(degree_to_time(138)), 0),
            Eq(self.vf(degree_to_time(138)), 0),
            Eq(self.af(degree_to_time(138)), 0),
            Eq(self.pf(degree_to_time(330)), 0),
            Eq(self.vf(degree_to_time(330)), 0),
            Eq(self.af(degree_to_time(330)), 0),
            Eq(self.pf(degree_to_time(0)), self.pf(degree_to_time(360))),
            Eq(self.vf(degree_to_time(0)), self.vf(degree_to_time(360))),
            Eq(self.af(degree_to_time(0)), self.af(degree_to_time(360))),
            Eq(self.jf(degree_to_time(0)), self.jf(degree_to_time(360))),
            Eq(self.pif(degree_to_time(0)), self.pif(degree_to_time(360))),
        ]

    def get_solutions(self):
        solutions = solve(self.equations, self.bs.coefficients)
        return solutions

    def get_spline_final(self):
        spline_final = SplineFinalExpr(self.spline, self.get_solutions())
        return spline_final

    def plot_svaj(self):
        self.get_spline_final().plot_numerical()
        return self


if __name__ == "__main__":
    jaw_to_york_knots = Knots([0, 43, 43, 90, 90, 138, 138, 330, 330, 360],
                              id='a', original_knots_type="deg")
    j2y = JawToYork(jaw_to_york_knots)
    j2y.plot_svaj()
    j2y.get_spline_final().get_velocity_functional()(degree_to_time(90))


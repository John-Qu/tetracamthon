from sympy import symbols, Symbol, nan, diff, lambdify, Eq, solve, latex, \
    Piecewise, integrate, cot, acos, sqrt
from sympy.abc import x, y
from sympy.plotting import plot
import numpy as np
import matplotlib.pyplot as plt
from helper_functions import degree_to_time, time_to_degree, \
    move_sympyplot_to_axes
from analysis import O4DriveA
from packages import Package
from splines_building import SplineWithPiecewisePolynomial


class JawOnYorkCurve(SplineWithPiecewisePolynomial):
    """
    """

    def __init__(self, knots=None, orders=None, pvajp=None):
        # 0
        start = [degree_to_time(0), [
            symbols('pos_start'),
            symbols('vel_start'),
            symbols('acc_start'),
            symbols('jerk_start'),
            symbols('ping_start')]]
        # 1
        widest = [degree_to_time(43), [
            -131,
            0,
            symbols('acc_widest'),
            symbols('jerk_widest'),
            symbols('ping_widest')]]
        # 2
        closed = [degree_to_time(138), [
            0,
            symbols('vel_closed'),
            symbols('acc_closed'),
            symbols('jerk_closed'),
            symbols('ping_closed')]]
        # 3
        open = [degree_to_time(330), [
            0,
            symbols('vel_open'),
            symbols('acc_open'),
            symbols('jerk_open'),
            symbols('ping_open')]]
        # 4
        end = [degree_to_time(360), [
            symbols('pos_end'),
            symbols('vel_end'),
            symbols('acc_end'),
            symbols('jerk_end'),
            symbols('ping_end')]]
        if knots == None:
            knots = np.array([start[0], widest[0], closed[0],
                              open[0], end[0]])
        if pvajp == None:
            pvajp = np.array([[start[1][i], widest[1][i], closed[1][i],
                               open[1][i], end[1][i]] for i in range(5)])
        if orders == None:
            orders = [6, 6, 2, 6]
        SplineWithPiecewisePolynomial.__init__(self, knots, orders)
        self.pvajp = pvajp
        self.equations = []
        self.variables = []
        self.count_of_var = sum(self.orders)
        self.count_of_interpolation = 0
        self.count_of_boundary = 0
        self.count_of_not_at_knot = 0
        self.count_of_periodic = 0
        self.count_of_smoothness = 0
        self.piecewise = []

    def build_interpolating_condition(self):
        """
        j1 = JawOnYorkCurve()
        print(j1.build_interpolating_condition())
        """
        if self.count_of_interpolation != 0:
            return self.count_of_interpolation
        for d in range(5):
            for k in range(1, len(self.knots) - 1):
                if isinstance(self.pvajp[d][k], Symbol):
                    continue
                else:
                    p = self.get_pieces()[k]
                    f = p.get_functions()
                    knot = self.knots[k]
                    eq = Eq(f[d](knot), self.pvajp[d][k])
                    self.equations.append(eq)
                    self.count_of_interpolation += 1
        return self.count_of_interpolation

    def build_boundary_condition(self):
        """
        j1 = JawOnYorkCurve()
        print(j1.build_boundary_condition())
        """
        if self.count_of_boundary != 0:
            return self.count_of_boundary
        for d in range(5):
            for k in [0, -1]:
                if isinstance(self.pvajp[d][k], Symbol):
                    continue
                else:
                    p = self.get_pieces()[k]
                    f = p.get_functions()
                    knot = self.knots[k]
                    eq = Eq(f[d](knot), self.pvajp[d][k])
                    self.equations.append(eq)
                    self.count_of_boundary += 1
        return self.count_of_boundary

    def build_not_at_knot_condition(self, points, depths, values):
        """
        j1 = JawOnYorkCurve()
        points = [degree_to_time(23), degree_to_time(123)]
        depths = [3, 3]
        values = [0, 0]
        print(j1.build_not_at_knot_condition(points, depths, values))
        """
        if self.count_of_not_at_knot != 0:
            return self.count_of_not_at_knot
        for i in range(len(points)):
            for k in range(self.num_of_pieces, -1, -1):
                if points[i] >= self.knots[k]:
                    p = self.get_pieces()[k]
                    f = p.get_functions()
                    knot = self.knots[k]
                    eq = Eq(f[depths[i]](knot), values[i])
                    self.equations.append(eq)
                    self.count_of_not_at_knot += 1
                    break
        return self.count_of_not_at_knot

    def build_periodic_condition(self):
        """
        j1 = JawOnYorkCurve()
        print(j1.build_periodic_condition())
        """
        if self.count_of_periodic != 0:
            return self.count_of_period
        ps = self.get_pieces()[0]
        fs = ps.get_functions()
        s = self.knots[0]
        pe = self.get_pieces()[-1]
        fe = pe.get_functions()
        e = self.knots[-1]
        for d in range(min(ps.order, pe.order)):
            eq = Eq(fs[d](s), fe[d](e))
            self.equations.append(eq)
            self.count_of_periodic += 1
            # TODO: less than 6 order condition?
        return self.count_of_periodic

    def how_many_smoothness_equations_available(self):
        """
        j1 = JawOnYorkCurve()
        print(j1.how_many_smoothness_equations_available())
        """
        if self.count_of_interpolation == 0:
            self.build_interpolating_condition()
        if self.count_of_boundary == 0:
            self.build_boundary_condition()
        if self.count_of_periodic == 0:
            self.build_periodic_condition()
        result = (self.count_of_var - self.count_of_interpolation -
                  self.count_of_boundary - self.count_of_periodic)
        return result

    def build_smoothness_condition(self, depths=[0, 4, 3, 3, 0]):
        """
        j1 = JawOnYorkCurve()
        print(j1.build_smoothness_condition())
        """
        if self.count_of_smoothness != 0:
            return self.count_of_smoothness
        k1 = self.knots[1]
        p1b = self.get_pieces()[0]
        p1a = self.get_pieces()[1]
        f1b = p1b.get_functions()
        f1a = p1a.get_functions()
        for d in range(4):
            eq = Eq(f1b[d](k1), f1a[d](k1))
            self.equations.append(eq)
            self.count_of_smoothness += 1
        k2 = self.knots[2]
        p2b = self.get_pieces()[1]
        p2a = self.get_pieces()[2]
        f2b = p2b.get_functions()
        f2a = p2a.get_functions()
        for d in range(2):
            eq = Eq(f2b[d](k2), f2a[d](k2))
            self.equations.append(eq)
            self.count_of_smoothness += 1
        eq = Eq(f2b[2](k2), 0)
        self.equations.append(eq)
        self.count_of_smoothness += 1
        k3 = self.knots[3]
        p3b = self.get_pieces()[2]
        p3a = self.get_pieces()[3]
        f3b = p3b.get_functions()
        f3a = p3a.get_functions()
        for d in range(2):
            eq = Eq(f3b[d](k3), f3a[d](k3))
            self.equations.append(eq)
            self.count_of_smoothness += 1
        eq = Eq(0, f3a[2](k3))
        self.equations.append(eq)
        self.count_of_smoothness += 1
        return self.count_of_smoothness

    def build_equations(self):
        """
        j1 = JawOnYorkCurve()
        print(j1.build_equations())
        """
        if self.count_of_interpolation == 0:
            self.build_interpolating_condition()
        if self.count_of_boundary == 0:
            self.build_boundary_condition()
        if self.count_of_periodic == 0:
            self.build_periodic_condition()
        if self.count_of_smoothness == 0:
            self.build_smoothness_condition()
        return len(self.equations)

    def get_equations(self):
        if len(self.equations) == 0:
            self.build_equations()
        return self.equations

    def build_variables(self):
        """
        j1 = JawOnYorkCurve()
        print(j1.build_variables())
        """
        if len(self.variables) != 0:
            return len(self.variables)
        for i in range(self.num_of_pieces):
            polynomial_i = self.get_pieces()[i]
            coe_i = polynomial_i.coe
            for j in range(len(coe_i)):
                self.variables.append(coe_i[j])
        return len(self.variables)

    def get_variables(self):
        if len(self.variables) == 0:
            self.build_variables()
        return self.variables

    def solve_coefficients(self):
        """
        j1 = JawOnYorkCurve()
        print(j1.solve_coefficients())
        """
        equations = self.get_equations()
        variables = self.get_variables()
        solutions = solve(equations, variables)
        return solutions

    def update_with_solution(self):
        """
        j1 = JawOnYorkCurve()
        j1.update_with_solution()
        """
        solution = self.solve_coefficients()
        self.involve_solutions(solution)

    def build_spline(self):
        self.update_with_solution()
        if len(self.piecewise) == 0:
            for k in range(min(self.orders)):
                self.piecewise.append(Piecewise(
                    (0, x < self.knots[0]),
                    (self.get_pieces()[0].get_expr()[k], x <= self.knots[1]),
                    (self.get_pieces()[1].get_expr()[k], x <= self.knots[2]),
                    (self.get_pieces()[2].get_expr()[k], x <= self.knots[3]),
                    (self.get_pieces()[3].get_expr()[k], x <= self.knots[4]),
                    (0, True)))

    def get_piecewise(self):
        self.build_spline()
        return self.piecewise

    def plot_numerical(self, num=3600):
        """
        j1 = JawOnYorkCurve()
        j1.plot_numerical()
        plot(j1.get_piecewise()[0], (x, 0, 0.9))
        plot(j1.get_piecewise()[1], (x, 0, 0.9))
        """
        t = np.linspace(0, degree_to_time(360),
                        num, endpoint=True)
        degree = time_to_degree(t)
        position = lambdify(self.get_piecewise()[0], x)(t)
        velocity = lambdify(self.get_piecewise()[1], x)(t)
        fig = plt.figure(figsize=(15, 12), dpi=80)
        fig.suptitle('Jaw on York, with knots on \n' +
                     str(time_to_degree(self.knots) - 30),
                     fontsize='xx-large')
        plt.subplot(2, 1, 1)
        plt.grid()
        plt.ylabel("Position (mm)")
        plt.plot(degree, position,
                 color="blue", linewidth=3.0, linestyle="-")
        plt.xlim(0.0, 360.0)
        plt.xticks(np.linspace(0, 360, 37, endpoint=True))
        plt.subplot(2, 1, 2)
        plt.grid()
        plt.ylabel("Velocity (mm/s)")
        plt.plot(degree, velocity,
                 color="blue", linewidth=3.0, linestyle="-")
        plt.xlim(0.0, 360.0)
        plt.xticks(np.linspace(0, 360, 37, endpoint=True))
        # plt.subplot(4, 1, 3)
        # plt.grid()
        # plt.ylabel("Acceleration (m/s^3)")
        # plt.plot(degree, acceleration / 1000,
        #          color="blue", linewidth=3.0, linestyle="-")
        # plt.xlim(0.0, 360.0)
        # plt.xticks(np.linspace(0, 360, 37, endpoint=True))
        # plt.subplot(4, 1, 4)
        # plt.grid()
        # plt.ylabel("Jerk (m/s^4)")
        # plt.plot(degree, jerk / 1000,
        #          color="blue", linewidth=3.0, linestyle="-")
        # plt.xlim(0.0, 360.0)
        # plt.xticks(np.linspace(0, 360, 37, endpoint=True))
        # plt.savefig("svaj_of_jaw_on_york.png", dpi=720)





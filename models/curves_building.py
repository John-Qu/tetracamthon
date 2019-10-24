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
        self.count_of_var = sum(self.orders)
        self.count_of_interpolation = 0
        self.count_of_boundary = 0
        self.count_of_not_at_knot = 0
        self.count_of_period = 0
        self.count_of_smoothness = 0

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
                    p = self.pieces[k]
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
                    p = self.pieces[k]
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
                    p = self.pieces[k]
                    f = p.get_functions()
                    knot = self.knots[k]
                    eq = Eq(f[depths[i]](knot), values[i])
                    self.equations.append(eq)
                    self.count_of_not_at_knot += 1
                    break
        return self.count_of_not_at_knot

    def how_many_smoothness_equations_available(self):
        """
        j1 = JawOnYorkCurve()
        print(j1.how_many_smoothness_equations_available())
        """
        if self.count_of_interpolation == 0:
            self.build_interpolating_condition()
        if self.count_of_boundary == 0:
            self.build_boundary_condition()
        result = (self.count_of_var - self.count_of_interpolation -
                  self.count_of_boundary)
        return result

    def build_smoothness_condition(self):
        pass

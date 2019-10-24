from sympy import symbols, diff
from sympy.abc import x
from sympy.plotting import plot
import numpy as np
import matplotlib.pyplot as plt
from helper_functions import degree_to_time, time_to_degree, \
    move_sympyplot_to_axes


class PolynomialCoefficients(object):
    """
    def test_polynomial_coefficients(self):
        c1 = PolynomialCoefficients(1, order=2)
        print(c1)
        c2 = PolynomialCoefficients('a', order=6)
        print(c2)
    """
    def __init__(self, piece_id, order=6):
        self.coe = []
        self.order = order
        for i in range(self.order, 0, -1):
            self.coe.append(symbols('C_' + str(piece_id) + '_' + str(i-1)))

    def __str__(self):
        return "Polynomial coefficients of order " + str(self.order) + ": \n" \
               + str(self.coe)


class Polynomial(object):
    """
    p1 = Polynomial('a', order=3, piece=(0, 1))
    print(p1)
    p2 = Polynomial('1', order=6, piece=(1, 3))
    print(p2)
    """
    def __init__(self, piece_id, order=6, piece=(0, 1)):
        self.piece_id = piece_id
        self.order = order
        # self.co = PolynomialCoefficients(self.id, order=self.order)
        self.piece = piece
        self.s = self.piece[0]
        self.e = self.piece[1]
        self.coe = []
        self.expr = []

    def build_expression(self):
        co_0 = symbols('C_' + str(self.piece_id) + '_' + str(0))
        expr = co_0
        for d in range(1, self.order):
            co_i = symbols('C_' + str(self.piece_id) + '_' + str(d))
            self.coe.append(co_i)
            expr += co_i * (x - self.s) ** d
        self.expr.append(expr)
        return expr

    def build_diffs(self):
        if len(self.expr) == 0:
            self.build_expression()
        elif len(self.expr) == self.order:
            return self.expr
        for depth in range(1, self.order):
            self.expr.append(diff(self.expr[0], x, depth))
        return self.expr

    def get_expr(self):
        if len(self.expr) < self.order:
            self.build_diffs()
        return self.expr

    def get_coefficients(self):
        return self.coe

    def get_piece(self):
        return self.piece

    def __str__(self):
        if len(self.expr) < self.order:
            self.build_diffs()
        who = "Polynomial on " + str(self.piece) + \
              " of order " + str(self.order) + ":"
        what = ''
        for depth in range(self.order):
            what += str(self.expr[depth]) + '\n'
        return who + "\n" + what






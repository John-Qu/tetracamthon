from sympy import symbols, diff, lambdify
from sympy.abc import x
from sympy.plotting import plot
import numpy as np
import matplotlib.pyplot as plt
from helper_functions import degree_to_time, time_to_degree, \
    move_sympyplot_to_axes


class Polynomial(object):
    """
    p1 = Polynomial('a', order=3, piece=(0, 1))
    print(p1.__str__(all_depth=True))
    p2 = Polynomial('1', order=6, piece=(1, 3))
    print(p2.__str__(all_depth=True))
    print(p2.coe)
    """
    def __init__(self, piece_id, order=6, piece=(0, 1)):
        self.piece_id = piece_id
        self.order = order
        self.piece = piece
        self.s = self.piece[0]
        self.e = self.piece[1]
        self.coe = []
        self.expr = []
        self.func = []

    def build_expression(self):
        co_0 = symbols('C_' + str(self.piece_id) + '_' + str(0))
        self.coe.append(co_0)
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

    def build_functions(self):
        if len(self.func) == self.order:
            return len(self.func)
        expr = self.get_expr()
        for i in range(self.order):
            f_i = lambdify(x, expr[i])
            self.func.append(f_i)
        return len(self.func)

    def get_functions(self):
        if len(self.func) < self.order:
            self.build_functions()
            return self.func
        else:
            return self.func

    def __str__(self, all_depth=False):
        if len(self.expr) < self.order:
            self.build_diffs()
        who = "Polynomial on " + str(self.piece) + \
              " of order " + str(self.order) + ":"
        if all_depth:
            what = ''
            for depth in range(self.order):
                what += str(self.expr[depth]) + '\n'
        else:
            what = str(self.expr[0]) + '\n'
        return who + "\n" + what


class SplineWithPiecewisePolynomial(object):
    """
    knots1 = [0, 1, 2, 3]
    orders1 = [3, 4, 5]
    s1 = SplineWithPiecewisePolynomial(knots1, orders1)
    print(s1)
    """
    def __init__(self, knots, orders):
        self.knots = knots
        self.orders = orders
        self.num_of_pieces = len(self.knots) - 1
        self.pieces = []

    def build_pieces(self):
        for piece_id in range(self.num_of_pieces):
            start, end = self.knots[piece_id], self.knots[piece_id + 1]
            piece_order = self.orders[piece_id]
            p_i = Polynomial(piece_id,
                             order=piece_order,
                             piece=(start, end))
            self.pieces.append(p_i)

    def get_pieces(self):
        if len(self.pieces) < self.num_of_pieces:
            self.build_pieces()
        return self.pieces


    def __str__(self):
        self.get_pieces()
        pieces = ''
        for i in range(self.num_of_pieces):
            pieces += str(self.pieces[i])
        return pieces


class SplineWithBsplines(object):
    def __init__(self):
        # TODO: add b-spline ability
        pass




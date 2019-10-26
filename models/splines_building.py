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

    def get_piece(self):
        return self.piece

    def get_order(self):
        return self.order

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

    def get_coefficients(self):
        if len(self.coe) < self.order:
            self.build_expression()
        return self.coe

    def build_diffs(self):
        if len(self.expr) == 0:
            self.build_expression()
        elif len(self.expr) == self.order:
            return self.expr
        # for depth in range(1, self.order):
        for depth in range(1, 6):
            self.expr.append(diff(self.expr[0], x, depth))
        return self.expr

    def get_expr(self, solution=None):
        if len(self.expr) < self.order:
            self.build_diffs()
        if solution != None:
            self.update_expr(solution)
        return self.expr

    def update_expr(self, solution):
        """ Update the coefficients with solution dictionary.

        :param solution: dict of coefficient and value pair
        :return: None
        """
        expr_0 = self.get_expr()[0]
        coe = self.get_coefficients()
        self.expr.clear()
        self.expr.append(expr_0.subs([(coe[index_of_coe],
                                       solution[coe[index_of_coe]])
                                      for index_of_coe in range(self.order)]))
        self.build_diffs()

    def replace_expr(self, new_expr, new_order):
        self.expr.clear()
        self.expr.append(new_expr)
        self.coe.clear()
        self.order = new_order
        self.build_diffs()

    def build_functions(self):
        if len(self.func) >= self.order:
            return len(self.func)
        expr = self.get_expr()
        for i in range(len(expr)):
            f_i = lambdify(x, expr[i])
            self.func.append(f_i)
        return len(self.func)

    def build_functions_with_subs(self, value):
        if len(self.func) >= self.order:
            return len(self.func)
        expr = self.get_expr()
        for i in range(len(expr)):
            f_i = expr[i].subs(x, value).evalf()
            self.func.append(f_i)
        return len(self.func)

    def update_functions(self):
        self.func.clear()
        self.build_functions()

    def get_functions(self):
        if len(self.func) <= self.order:
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
        self.expressions = []

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

    def involve_solutions(self, solution, latex_print_out=False):
        """
        """
        for index_of_piece in range(self.num_of_pieces):
            poly = self.pieces[index_of_piece]
            poly.update_expr(solution)  # poly is an instance of Polynomial.


class SplineWithBsplines(object):
    def __init__(self):
        # TODO: add b-spline ability
        pass

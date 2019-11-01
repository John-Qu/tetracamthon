from sympy import symbols, diff, lambdify, nan, Eq, solve, Piecewise
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

    def get_piece_id(self):
        return self.piece_id

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
        old_expr = self.get_expr().copy()
        coe = self.get_coefficients()
        self.expr.clear()
        for i in range(len(old_expr)):
            expr_i = old_expr[i]
            self.expr.append(expr_i.subs([(coe[index_of_coe],
                                           solution[coe[index_of_coe]])
                                          for index_of_coe
                                          in range(self.order)]))

    def replace_expr(self, new_expr, new_coe):
        self.expr.clear()
        self.expr.append(new_expr)
        self.coe.clear()
        self.coe.extend(new_coe)
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


class ShakeHand(SplineWithPiecewisePolynomial):
    # def __init__(self, start_knot=0.3625, end_knot=0.4825,
    #              start_position=0, end_position=symbols('end_p'),
    #              cons_velocity=-422, mod_velocity=-122):
    def __init__(self, start_knot=0.3625, end_knot=0.4825,
                 start_position=0, end_position=nan,
                 cons_velocity=-422, mod_velocity=-122):

        """
        s1 = ShakeHand()
        :param start_knot:
        :param end_knot:
        :param start_position:
        :param end_position:
        :param cons_velocity:
        :param mod_velocity:
        """
        self.start_knot = start_knot
        self.end_knot = end_knot
        self.start_p = start_position
        self.end_p = end_position
        self.cons_v= cons_velocity
        self.mod_v= mod_velocity
        delta = self.end_knot - self.start_knot
        knots = np.array([
            self.start_knot,
            self.start_knot + delta / 10 * 2,
            self.start_knot + delta / 10 * 3,
            self.start_knot + delta / 2,
            self.end_knot - delta / 10 * 3,
            self.end_knot - delta / 10 * 2,
            self.end_knot
        ])
        orders = [6 for i in range(len(knots) - 1)]
        SplineWithPiecewisePolynomial.__init__(self, knots, orders)
        self.pvajp = [
            [self.start_p, nan, nan, nan, nan, nan, self.end_p],
            [self.cons_v, nan, nan, self.mod_v, nan, nan, self.cons_v],
            [0, nan, nan, 0, nan, nan, 0],
            [0, 0, nan, nan, nan, 0, 0],
            [nan, nan, 0, nan, 0, nan, nan]
        ]
        self.equations = []
        self.variables = []
        self.count_of_interpolation = 0
        self.count_of_smoothness = 0
        self.piecewise = []
        self.solution = {}

    def build_variables(self):
        """
        s1 = ShakeHand()
        print(s1.build_variables())
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
        """
        s1 = ShakeHand()
        print(len(s1.get_variables()))
        """
        if len(self.variables) == 0:
            self.build_variables()
        return self.variables

    def build_interpolating_condition(self):
        """
        s1 = ShakeHand()
        print(len(s1.build_interpolating_condition()))
        """
        if self.count_of_interpolation != 0:
            return self.count_of_interpolation
        for k in range(len(self.knots)):
            knot = self.knots[k]
            if k == 0:
                p = self.get_pieces()[0]
            else:
                p = self.get_pieces()[k - 1]
            e = p.get_expr()
            for d in range(5):
                if self.pvajp[d][k] == nan:
                    continue
                else:
                    eq = Eq(e[d].subs(x, knot), self.pvajp[d][k])
                    self.equations.append(eq)
                    self.count_of_interpolation += 1
        return self.equations[-self.count_of_interpolation:]

    def build_smoothness_condition(self, depths=None):
        """
        s1 = ShakeHand()
        print(len(s1.build_smoothness_condition()))
        for i in range(len(j2.equations)):
            print(j2.equations[i])
        """
        if self.count_of_smoothness != 0:
            return self.count_of_smoothness
        if depths == None:
            depths = {
                1: 5,
                2: 4,
                3: 5,
                4: 4,
                5: 5
            }
        for i in depths.keys():
            ki = self.knots[i]  # Knot I
            pib = self.get_pieces()[i - 1]  # Piece Before knot I
            pia = self.get_pieces()[i]  # Piece After knot I
            eib = pib.get_expr()
            eia = pia.get_expr()
            for d in range(depths[i]):
                eq = Eq(eib[d].subs(x, ki), eia[d].subs(x, ki))
                self.equations.append(eq)
                self.count_of_smoothness += 1
        return self.equations[-self.count_of_smoothness:]

    def build_equations(self):
        """
        s1 = ShakeHand()
        print(len(s1.build_equations()))
        """
        if self.count_of_interpolation == 0:
            self.build_interpolating_condition()
        if self.count_of_smoothness == 0:
            self.build_smoothness_condition()
        return self.equations

    def get_equations(self):
        if len(self.equations) == 0:
            self.build_equations()
        return self.equations

    def solve_coefficients(self):
        """
        s1 = ShakeHand()
        print(s1.solve_coefficients())
        equations = s1.get_equations()
        variables = s1.get_variables()
        solutions = solve(equations, variables)
        """
        if self.solution != {}:
            return self.solution
        equations = self.get_equations()
        variables = self.get_variables()
        solution = solve(equations, variables)
        self.solution = solution
        return self.solution

    def update_with_solution(self):
        """
        s1 = ShakeHand()
        s1.update_with_solution()
        print(s1.get_pieces()[2].get_expr()[0])
        """
        solution = self.solve_coefficients()
        self.involve_solutions(solution)

    def get_kth_expr_of_ith_piece(self, k, i):
        try:
            return self.get_pieces()[i].get_expr()[k]
        except:
            return 0

    def build_spline(self):
        """
        s1 = ShakeHand()
        s1.update_with_solution()
        s1.build_spline()
        """
        for k in range(4):
            self.piecewise.append(Piecewise(
                (0, x < self.knots[0]),
                (self.get_kth_expr_of_ith_piece(k, 0), x <= self.knots[1]),
                (self.get_kth_expr_of_ith_piece(k, 1), x <= self.knots[2]),
                (self.get_kth_expr_of_ith_piece(k, 2), x <= self.knots[3]),
                (self.get_kth_expr_of_ith_piece(k, 3), x <= self.knots[4]),
                (0, True)))

    def get_piecewise(self):
        """
        s1 = ShakeHand()
        print(s1.get_piecewise()[0])
        """
        if len(self.piecewise) == 0:
            self.build_spline()
        return self.piecewise

    def plot_svaj(self):
        """
        s1 = ShakeHand()
        s1.update_with_solution()
        print(s1.get_piecewise()[0])
        s1.plot_svaj()
        """
        p0 = plot(0, (x, self.knots[0], self.knots[-1]),
                  title="Position",
                  ylabel="(mm)",
                  show=False)
        for i in range(self.num_of_pieces):
            expr_p_i = self.get_kth_expr_of_ith_piece(0, i)
            pi = plot(expr_p_i, (x, self.knots[i], self.knots[i + 1]),
                      show=False)
            p0.extend(pi)
        v0 = plot(0, (x, self.knots[0], self.knots[-1]),
                  title="Velocity",
                  ylabel="(mm/sec)",
                  show=False)
        for i in range(self.num_of_pieces):
            expr_v_i = self.get_kth_expr_of_ith_piece(1, i)
            vi = plot(expr_v_i, (x, self.knots[i], self.knots[i + 1]),
                      show=False)
            v0.extend(vi)
        a0 = plot(0, (x, self.knots[0], self.knots[-1]),
                  title="Acceleration",
                  ylabel="(mm/sec^2)",
                  show=False)
        for i in range(self.num_of_pieces):
            expr_a_i = self.get_kth_expr_of_ith_piece(2, i)
            ai = plot(expr_a_i, (x, self.knots[i], self.knots[i + 1]),
                      show=False)
            a0.extend(ai)
        j0 = plot(0, (x, self.knots[0], self.knots[-1]),
                  title="Jerk",
                  ylabel="(mm/sec^3)",
                  show=False)
        for i in range(self.num_of_pieces):
            expr_j_i = self.get_kth_expr_of_ith_piece(3, i)
            ji = plot(expr_j_i, (x, self.knots[i], self.knots[i + 1]),
                      show=False)
            j0.extend(ji)
        fig, (ax1, ax2, ax3, ax4) = plt.subplots(nrows=4)
        move_sympyplot_to_axes(p0, ax1)
        ax1.set_xticks([self.knots[i] for i in range(len(self.knots))])
        ax1.set_xticklabels([(i % 2) * '\n' +
                             str(time_to_degree(self.knots[i]))
                             for i in range(len(self.knots))])
        ax1.grid(True)
        move_sympyplot_to_axes(v0, ax2)
        ax2.set_xticks([self.knots[i] for i in range(len(self.knots))])
        ax2.set_xticklabels([(i % 2) * '\n' +
                             str(time_to_degree(self.knots[i]))
                             for i in range(len(self.knots))])
        ax2.grid(True)
        move_sympyplot_to_axes(a0, ax3)
        ax3.set_xticks([self.knots[i] for i in range(len(self.knots))])
        ax3.set_xticklabels([(i % 2) * '\n' +
                             str(time_to_degree(self.knots[i]))
                             for i in range(len(self.knots))])
        ax3.grid(True)
        move_sympyplot_to_axes(j0, ax4)
        ax4.set_xticks([self.knots[i] for i in range(len(self.knots))])
        ax4.set_xticklabels([(i % 2) * '\n' +
                             str(time_to_degree(self.knots[i]))
                             for i in range(len(self.knots))])
        ax4.grid(True)
        ax4.set_xlabel('machine degree')
        plt.show()



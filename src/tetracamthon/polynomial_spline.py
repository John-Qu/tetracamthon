import pickle

from sympy import symbols, diff, nan, Eq, solve, linsolve
from sympy.abc import x
from sympy.plotting import plot

from .helper_functions import plot_pvaj
from tetracamthon.helper import data_path


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
            self.expr.append(
                expr_i.subs([(coe[index_of_coe],
                              solution.get(coe[index_of_coe], 0))
                             for index_of_coe in range(self.order)]))

    def replace_expr(self, new_expr, new_coe):
        self.expr.clear()
        self.expr.append(new_expr)
        self.coe.clear()
        self.coe.extend(new_coe)
        self.build_diffs()

    # These codes are useless.
    # def build_functions(self):
    #     if len(self.func) >= self.order:
    #         return len(self.func)
    #     expr = self.get_expr()
    #     for i in range(len(expr)):
    #         f_i = lambdify(x, expr[i])
    #         self.func.append(f_i)
    #     return len(self.func)
    #
    # def build_functions_with_subs(self, value):
    #     if len(self.func) >= self.order:
    #         return len(self.func)
    #     expr = self.get_expr()
    #     for i in range(len(expr)):
    #         f_i = expr[i].subs(x, value).evalf()
    #         self.func.append(f_i)
    #     return len(self.func)
    #
    # def update_functions(self):
    #     self.func.clear()
    #     self.build_functions()
    #
    # def get_functions(self):
    #     if len(self.func) <= self.order:
    #         self.build_functions()
    #         return self.func
    #     else:
    #         return self.func

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

    def update_with_new_expr(self, new_expr):
        self.expr.clear()
        self.expr.append(new_expr)
        self.build_diffs()
        return self.expr

    def update_with_new_expressions(self, new_expressions):
        self.expr.clear()
        self.expr.extend(new_expressions)
        return self.expr


class SplineWithPiecewisePolynomial(object):
    """
    s1 = SplineWithPiecewisePolynomial()
    print(s1)
    """

    def __init__(self,
                 key_knots=None,
                 orders=None,
                 smooth_depth=None,
                 name='polynomials_curve'):
        start = (0, (
            0,
            0,
            0,
            nan,
            nan,
        ))
        knot1 = (1, (
            0.3,
            nan,
            nan,
            nan,
            nan,
        ))
        knot2 = (2, (
            0.6,
            nan,
            nan,
            nan,
            nan,
        ))
        end = (3, (
            1,
            0,
            0,
            nan,
            nan,
        ))
        if key_knots is None:
            key_knots = [start, knot1, knot2, end]
        if smooth_depth is None:
            smooth_depth = dict(
                zip(key_knots[1:-1], [6] * (len(key_knots) - 2)))
        knots = [key_knots[i][0]
                 for i in range(len(key_knots))]
        pvajp = [[key_knots[i][1][j]
                  for i in range(len(key_knots))]
                 for j in range(len(key_knots[0][1]))]
        if orders is None:
            orders = [6] * len(key_knots)
        self.key_knots = key_knots
        self.smooth_depth = smooth_depth
        self._name = name
        self.knots = knots
        self.orders = orders
        self.pvajp = pvajp
        self.num_of_pieces = len(self.knots) - 1
        self.pieces = []
        self.equations = []
        self.variables = []
        self.count_of_interpolation = 0
        self.count_of_smoothness = 0
        self.count_of_not_at_knot = 0
        self.count_of_periodic = 0
        self.piecewise = []
        self.solution = {}
        self.count_of_var = sum(self.orders)

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

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    def build_variables(self):
        """
        s1 = SplineWithPiecewisePolynomial()
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
        s1 = SplineWithPiecewisePolynomial()
        print(len(s1.get_variables()))
        """
        if len(self.variables) == 0:
            self.build_variables()
        return self.variables

    def build_interpolating_condition(self):
        """
        s1 = SplineWithPiecewisePolynomial()
        print(len(s1.build_interpolating_condition()))
        """
        if self.count_of_interpolation != 0:
            return self.equations[-self.count_of_interpolation:]
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
        s1 = SplineWithPiecewisePolynomial()
        print(len(s1.build_smoothness_condition()))
        for i in range(len(s1.equations)):
            print(s1.equations[i])
        """
        if self.count_of_smoothness != 0:
            return self.equations[-self.count_of_smoothness:]
        if depths is None:
            depths = self.smooth_depth
        # for i in depths.keys():
        #     ki = self.knots[i]  # Knot I
        #     pib = self.get_pieces()[i - 1]  # Piece Before knot I
        #     pia = self.get_pieces()[i]  # Piece After knot I
        #     eib = pib.get_expr()
        #     eia = pia.get_expr()
        #     for d in range(depths[i]):
        #         eq = Eq(eib[d].subs(x, ki), eia[d].subs(x, ki))
        #         self.equations.append(eq)
        #         self.count_of_smoothness += 1
        for i in range(1, len(self.key_knots) - 1):
            kpi = self.key_knots[i]  # Knot Point I
            ki = kpi[0]
            pib = self.get_pieces()[i - 1]  # Piece Before knot I
            pia = self.get_pieces()[i]  # Piece After knot I
            eib = pib.get_expr()
            eia = pia.get_expr()
            for d in range(depths[kpi]):
                eq = Eq(eib[d].subs(x, ki), eia[d].subs(x, ki))
                self.equations.append(eq)
                self.count_of_smoothness += 1
        return self.equations[-self.count_of_smoothness:]

    def build_not_at_knot_condition(self,
                                    points=None, depths=None, values=None):
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
                    e = p.get_expr()
                    # f = p.get_functions()
                    knot = self.knots[k]
                    # eq = Eq(f[depths[i]](knot), values[i])
                    eq = Eq(e[depths[i]].subs(x, knot), values[i])
                    self.equations.append(eq)
                    self.count_of_not_at_knot += 1
                    break
        return self.equations[-self.count_of_not_at_knot:]

    def build_periodic_condition(self, depth=None):
        """
        j1 = JawOnYorkCurve()
        print(j1.build_periodic_condition())
        """
        if self.count_of_periodic != 0:
            return self.equations[-self.count_of_periodic:]
        s = self.knots[0]  # Start knot
        ps = self.get_pieces()[0]  # Piece of Start
        es = ps.get_expr()  # Expressions of Start piece
        # fs = ps.get_functions()
        e = self.knots[-1]  # End knot
        pe = self.get_pieces()[-1]  # Piece of End
        ee = pe.get_expr()  # Expression of End piece
        # fe = pe.get_functions()
        if depth is None:
            depth = min(ps.order, pe.order)
        for d in range(depth):
            eq = Eq(es[d].subs(x, s), ee[d].subs(x, e))
            self.equations.append(eq)
            self.count_of_periodic += 1
            # TODO: less than 6 order condition?
        return self.equations[-self.count_of_periodic:]

    def how_many_smoothness_equations_available(self):
        """
        j1 = JawOnYorkCurve(whether_rebuild_pieces=True)
        print(j1.how_many_smoothness_equations_available())
        """
        if self.count_of_interpolation == 0:
            self.build_interpolating_condition()
        if self.count_of_periodic == 0:
            self.build_periodic_condition()
        if self.count_of_not_at_knot == 0:
            self.build_not_at_knot_condition()
        result = (self.count_of_var - self.count_of_interpolation -
                  self.count_of_periodic - self.count_of_not_at_knot)
        return result

    def build_equations(self,
                        whether_build_periodic=False,
                        whether_build_not_at_knot=False):
        """
        s1 = SplineWithPiecewisePolynomial()
        print(len(s1.build_equations()))
        """
        if self.count_of_interpolation == 0:
            self.build_interpolating_condition()
        if self.count_of_smoothness == 0:
            self.build_smoothness_condition()
        if whether_build_periodic:
            self.build_periodic_condition()
        if whether_build_not_at_knot:
            self.build_not_at_knot_condition()
        return self.equations

    def get_equations(self):
        if len(self.equations) == 0:
            self.build_equations()
        return self.equations

    def solve_coefficients(self):
        """
        s1 = SplineWithPiecewisePolynomial()
        print(s1.solve_coefficients())
        """
        if self.solution != {}:
            return self.solution
        equations = self.get_equations()
        variables = self.get_variables()
        # Prefer linear solver to get ordered values aligned with variables
        sol_set = linsolve(equations, variables)
        if sol_set:
            first = list(sol_set)[0]
            try:
                self.solution = dict(zip(variables, list(first)))
            except Exception:
                self.solution = {}
        else:
            # Fallbacks for non-linear systems
            solution = solve(equations, variables, dict=True)
            if isinstance(solution, list) and len(solution) > 0 and isinstance(solution[0], dict):
                self.solution = solution[0]
            else:
                alt = solve(equations, variables)
                if isinstance(alt, dict):
                    self.solution = alt
                elif isinstance(alt, (list, tuple)) and len(alt) == len(variables):
                    try:
                        self.solution = dict(zip(variables, alt))
                    except Exception:
                        self.solution = {}
                else:
                    self.solution = {}
        return self.solution

    def update_with_solution(self):
        """
        s1 = SplineWithPiecewisePolynomial()
        s1.update_with_solution()
        print(s1.get_pieces()[0].get_expr()[0])
        """
        solution = self.solve_coefficients()
        self.involve_solutions(solution)

    def save_solved_pieces(self):
        """
        s1 = SplineWithPiecewisePolynomial()
        s1.update_with_solution()
        s1.save_solved_pieces()
        """
        output = open(data_path('{}_pieces'.format(self.name)), 'wb')
        pickle.dump(self.get_pieces(), output)
        output.close()

    def load_solved_pieces(self):
        """
        s1 = SplineWithPiecewisePolynomial()
        s1.load_solved_pieces()
        print(s1.get_pieces()[2].get_expr()[0])
        """
        pkl_file = open(data_path('{}_pieces'.format(self.name)), 'rb')
        self.pieces = pickle.load(pkl_file)
        pkl_file.close()

    def get_kth_expr_of_ith_piece(self, k, i):
        try:
            return self.get_pieces()[i].get_expr()[k]
        except:
            return 0

    def combine_pieces_for_plot(self,
                                whether_save_png=False,
                                line_color='blue',
                                whether_show_figure=False,
                                whether_knots_ticks=True,
                                ):
        """
        s1 = SplineWithPiecewisePolynomial()
        s1.update_with_solution()
        s1.plot_svaj()
        """
        p0 = plot(0, (x, self.knots[0], self.knots[-1]),
                  show=False)
        for i in range(self.num_of_pieces):
            expr_p_i = self.get_kth_expr_of_ith_piece(0, i)
            pi = plot(expr_p_i, (x, self.knots[i], self.knots[i + 1]),
                      show=False, line_color=line_color)
            p0.extend(pi)
        v0 = plot(0, (x, self.knots[0], self.knots[-1]),
                  show=False)
        for i in range(self.num_of_pieces):
            expr_v_i = self.get_kth_expr_of_ith_piece(1, i)
            vi = plot(expr_v_i, (x, self.knots[i], self.knots[i + 1]),
                      show=False, line_color=line_color)
            v0.extend(vi)
        a0 = plot(0, (x, self.knots[0], self.knots[-1]),
                  show=False)
        for i in range(self.num_of_pieces):
            expr_a_i = self.get_kth_expr_of_ith_piece(2, i)
            ai = plot(expr_a_i, (x, self.knots[i], self.knots[i + 1]),
                      show=False, line_color=line_color)
            a0.extend(ai)
        j0 = plot(0, (x, self.knots[0], self.knots[-1]),
                  show=False)
        for i in range(self.num_of_pieces):
            expr_j_i = self.get_kth_expr_of_ith_piece(3, i)
            ji = plot(expr_j_i, (x, self.knots[i], self.knots[i + 1]),
                      show=False, line_color=line_color)
            j0.extend(ji)
        if whether_show_figure:
            plot_pvaj([p0, v0, a0, j0], self.knots,
                      name=self.name,
                      whether_save_png=whether_save_png,
                      whether_show_figure=whether_show_figure,
                      whether_knots_ticks=whether_knots_ticks,
                      )
        return p0, v0, a0, j0

    def get_start_pvaj(self):
        """
        s1 = SplineWithPiecewisePolynomial()
        s1.load_solved_pieces()
        print(s1.get_start_pvaj())
        :return: tuple of pvaj on the start knot
        """
        k_s = self.knots[0]
        return tuple([self.get_kth_expr_of_ith_piece(k, 0).subs(x, k_s)
                      for k in range(4)])

    def get_end_pvaj(self):
        """
        s1 = SplineWithPiecewisePolynomial()
        s1.load_solved_pieces()
        print(s1.get_end_pvaj())
        :return: tuple of pvaj on the end knot
        """
        k_e = self.knots[-1]
        return tuple([self.get_kth_expr_of_ith_piece(k, -1).subs(x, k_e)
                      for k in range(4)])

    def get_point_pvaj(self, point):
        """
        s1 = SplineWithPiecewisePolynomial()
        s1.load_solved_pieces()
        print(s1.get_end_pvaj())
        :return: tuple of pvaj on the point knot
        """
        return tuple([self.get_piecewise()[k].subs(x, point)
                      for k in range(4)])

    def build_spline(self):
        """
        To be replaced by subclass method.
        """
        pass

    def get_piecewise(self):
        """
        s3 = ClimbUp()
        s3 = ShakeHand()
        print(s3.get_piecewise()[0])
        """
        if len(self.piecewise) == 0:
            self.build_spline()
        return self.piecewise

    def update_piece_with_new_expr(self, index, new_expr):
        self.pieces[index].update_with_new_expr(new_expr)

    def update_piece_with_new_expressions(self, index, new_expressions):
        self.pieces[index].update_with_new_expressions(new_expressions)

    def get_knots(self):
        return self.knots

from sympy import symbols, diff, lambdify, nan, Eq, solve, Piecewise, \
    piecewise_fold
from sympy.abc import x
from sympy.plotting import plot
import numpy as np
import pickle
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
        for depth in range(1, self.order):
        # for depth in range(1, 6):
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
                                          for index_of_coe in range(self.order)]))

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

    def update_with_new_expr(self, expr_added, value_add_to_x):
        ori_expr = self.expr[0]
        self.expr.clear()
        new_expr = ori_expr.subs(x, x + value_add_to_x) + expr_added
        self.expr.append(new_expr)
        self.piece = (self.s - value_add_to_x, self.e - value_add_to_x)
        self.build_diffs()
        # for i in range(1, self.order):
        #     self.expr.append(0)
        return self.expr


class SplineWithPiecewisePolynomial(object):
    """
    s1 = SplineWithPiecewisePolynomial()
    print(s1)
    """

    def __init__(self, knots=None, orders=None, pvajp=None,
                 name='polynomials_curve'):
        if knots is None:
            knots = np.linspace(0, 3, 4, endpoint=True)
        if orders is None:
            orders = [6 for i in range(len(knots)-1)]
        if pvajp is None:
            pvajp = [
                [0, 0.3, 0.6, 1],
                [0, nan, nan, 0],
                [0, nan, nan, 0],
                [nan, nan, nan, nan],
                [nan, nan, nan, nan]
            ]
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
        self.piecewise = []
        self.solution = {}

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
            return self.count_of_smoothness
        if depths is None:
            depths = {
                1: 5,
                2: 5
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
        s1 = SplineWithPiecewisePolynomial()
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
        s1 = SplineWithPiecewisePolynomial()
        print(s1.solve_coefficients())
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
        output = open('{}_pieces.pkl'.format(self.name), 'wb')
        pickle.dump(self.get_pieces(), output)
        output.close()

    def load_solved_pieces(self):
        """
        s1 = SplineWithPiecewisePolynomial()
        s1.load_solved_pieces()
        print(s1.get_pieces()[2].get_expr()[0])
        """
        pkl_file = open('{}_pieces.pkl'.format(self.name), 'rb')
        self.pieces = pickle.load(pkl_file)
        pkl_file.close()


    def get_kth_expr_of_ith_piece(self, k, i):
        try:
            return self.get_pieces()[i].get_expr()[k]
        except:
            return 0

    def plot_svaj(self):
        """
        s1 = SplineWithPiecewisePolynomial()
        s1.update_with_solution()
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

    def get_piecewise(self):
        """
        s3 = ClimbUp()
        s3 = ShakeHand()
        print(s3.get_piecewise()[0])
        """
        return self.piecewise

    def add_expr_to_pieces(self, expr_added, value_add_to_x):
        for i in range(self.num_of_pieces):
            self.pieces[i].update_expr_with_new_expr(expr_added,
                                                     value_add_to_x)


class ShakeHand(SplineWithPiecewisePolynomial):
    # def __init__(self, start_knot=0.3625, end_knot=0.4825,
    #              start_position=0, end_position=symbols('end_p'),
    #              cons_velocity=-422, mod_velocity=-122):
    def __init__(self, name='shake_hand_curve_1',
                 start_knot=degree_to_time(262),
                 end_knot=degree_to_time(317),
                 start_position=0, end_position=nan,
                 cons_velocity=-422, mod_velocity=-122,
                 if_rebuild_pieces=False):
        """
        s1 = ShakeHand(name='shake_hand_curve_262_317', if_rebuild_pieces=True)
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
        pvajp = [
            [self.start_p, nan, nan, nan, nan, nan, self.end_p],
            [self.cons_v, nan, nan, self.mod_v, nan, nan, self.cons_v],
            [0, nan, nan, 0, nan, nan, 0],
            [0, 0, nan, nan, nan, 0, 0],
            [nan, nan, 0, nan, 0, nan, nan]
        ]
        orders = [6 for i in range(len(knots) - 1)]
        SplineWithPiecewisePolynomial.__init__(self, knots, orders, pvajp,
                                               name=name)
        if if_rebuild_pieces:
            self.update_with_solution()
            self.save_solved_pieces()
        else:
            self.load_solved_pieces()

    def build_smoothness_condition(self, depths=None):
        """
        s1 = ShakeHand(if_save_pieces=False, if_load_pieces=False)
        print(len(s1.build_smoothness_condition()))
        print(len(s1.build_interpolating_condition()))
        for i in range(len(s1.equations)):
            print(s1.equations[i])
        """
        if self.count_of_smoothness != 0:
            return self.count_of_smoothness
        if depths is None:
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

    def build_spline(self):
        """
        s1 = ShakeHand(if_save_pieces=True, if_load_pieces=False)
        s1 = ShakeHand(if_save_pieces=False, if_load_pieces=True)
        s1.build_spline()
        s1.plot_svaj()
        """
        for k in range(4):
            self.piecewise.append(Piecewise(
                (0, x < self.knots[0]),
                (self.get_kth_expr_of_ith_piece(k, 0), x <= self.knots[1]),
                (self.get_kth_expr_of_ith_piece(k, 1), x <= self.knots[2]),
                (self.get_kth_expr_of_ith_piece(k, 2), x <= self.knots[3]),
                (self.get_kth_expr_of_ith_piece(k, 3), x <= self.knots[4]),
                (self.get_kth_expr_of_ith_piece(k, 4), x <= self.knots[5]),
                (self.get_kth_expr_of_ith_piece(k, 5), x <= self.knots[6]),
                (0, True)))

    def get_piecewise(self):
        """
        s1 = ShakeHand()
        print(s1.get_piecewise()[0])
        s1.plot_svaj()
        """
        if len(self.piecewise) == 0:
            self.build_spline()
        return self.piecewise


class Pull(SplineWithPiecewisePolynomial):
    def __init__(self, name='shake_hand_curve_1',
                 start_knot=0, end_knot=0.45,
                 start_position=0, end_position=nan,
                 cons_velocity=-422):
        """
        s2 = SmoothPulling()
        """
        self.start_knot = start_knot
        self.end_knot = end_knot
        self.start_p = start_position
        self.end_p = end_position
        self.cons_v= cons_velocity
        knots = np.array([
            self.start_knot,
            self.end_knot
        ])
        pvajp = [
            [self.start_p, self.end_p],
            [self.cons_v, nan],
            [nan, nan],
            [nan, nan],
            [nan, nan]
        ]
        orders = [2 for i in range(len(knots) - 1)]
        SplineWithPiecewisePolynomial.__init__(self, knots, orders, pvajp,
                                               name='smooth_pulling_curve_1')

    def build_equations(self):
        """
        s1 = SplineWithPiecewisePolynomial()
        print(len(s1.build_equations()))
        """
        if self.count_of_interpolation == 0:
            self.build_interpolating_condition()
        return self.equations

    def build_spline(self):
        """
        s2 = SmoothPulling()
        s2.update_with_solution()
        s2.build_spline()
        """
        for k in range(4):
            self.piecewise.append(Piecewise(
                (0, x < self.knots[0]),
                (self.get_kth_expr_of_ith_piece(k, 0), x <= self.knots[1]),
                (0, True)))

    def get_piecewise(self):
        """
        s2 = SmoothPulling()
        print(s2.get_piecewise()[0])
        """
        if len(self.piecewise) == 0:
            self.build_spline()
        return self.piecewise


class Climb(SplineWithPiecewisePolynomial):
    def __init__(self, name='climb_up_curve_325_92',
                 start_knot=degree_to_time(-35),
                 cross_knot=degree_to_time(43),
                 high_knot=degree_to_time(84),
                 touch_knot=degree_to_time(92),
                 start_p=-50,
                 cross_p=200,
                 high_p=372.2,
                 touch_p=365,
                 start_v=-422,
                 touch_v=-200,
                 touch_a=-4444,
                 touch_j=500000):
        """
        s3 = ClimbUp()
        """
        self.name=name
        knots = np.array([
            start_knot,
            degree_to_time(-25),
            degree_to_time(-18),
            0,
            # cross_knot,
            # high_knot,
            touch_knot
        ])
        pvajp = [
            # [start_p, 0, cross_p, high_p, touch_p],
            # [start_v, 0, nan, 0, touch_v],
            # [0, nan, nan, nan, touch_a],
            # [nan, nan, nan, nan, touch_j],
            # [nan, nan, nan, nan, nan]
            [start_p, nan, nan, 0, touch_p],
            [start_v, nan, -430, 0, touch_v],
            [0, -5700, nan, nan, touch_a],
            [nan, 0, nan, nan, nan],
            [nan, nan, nan, nan, nan]
        ]
        orders = [6 for i in range(len(knots) - 1)]
        SplineWithPiecewisePolynomial.__init__(self, knots, orders, pvajp,
                                               name=name)

    def build_smoothness_condition(self, depths=None):
        """
        s3 = ClimbUp()
        print(len(s3.build_smoothness_condition()))
        for i in range(len(s3.equations)):
            print(s3.equations[i])
        s3 = ClimbUp()
        s3.update_with_solution()
        s3.plot_svaj()
        """
        if self.count_of_smoothness != 0:
            return self.count_of_smoothness
        if depths is None:
            depths = {
                1: 4,
                2: 4,
                3: 4,
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


class Throw(SplineWithPiecewisePolynomial):
    def __init__(self, name='climb_up_curve_325_92',
                 start_knot=degree_to_time(-35),
                 cross_knot=degree_to_time(43),
                 high_knot=degree_to_time(84),
                 touch_knot=degree_to_time(92),
                 start_p=-50,
                 cross_p=200,
                 high_p=372.2,
                 touch_p=365,
                 start_v=-422,
                 touch_v=-200,
                 touch_a=-4444,
                 touch_j=500000):
        """
        s3 = ClimbUp()
        """
        self.name=name
        knots = np.array([
            start_knot,
            degree_to_time(-25),
            degree_to_time(-18),
            0,
            # cross_knot,
            # high_knot,
            touch_knot
        ])
        pvajp = [
            # [start_p, 0, cross_p, high_p, touch_p],
            # [start_v, 0, nan, 0, touch_v],
            # [0, nan, nan, nan, touch_a],
            # [nan, nan, nan, nan, touch_j],
            # [nan, nan, nan, nan, nan]
            [start_p, nan, nan, 0, touch_p],
            [start_v, nan, -430, 0, touch_v],
            [0, -5700, nan, nan, touch_a],
            [nan, 0, nan, nan, nan],
            [nan, nan, nan, nan, nan]
        ]
        orders = [6 for i in range(len(knots) - 1)]
        SplineWithPiecewisePolynomial.__init__(self, knots, orders, pvajp,
                                               name=name)

    def build_smoothness_condition(self, depths=None):
        """
        s3 = ClimbUp()
        print(len(s3.build_smoothness_condition()))
        for i in range(len(s3.equations)):
            print(s3.equations[i])
        s3 = ClimbUp()
        s3.update_with_solution()
        s3.plot_svaj()
        """
        if self.count_of_smoothness != 0:
            return self.count_of_smoothness
        if depths is None:
            depths = {
                1: 4,
                2: 4,
                3: 4,
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



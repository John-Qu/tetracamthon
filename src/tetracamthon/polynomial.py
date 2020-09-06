import csv
from math import isnan
from bisect import bisect_left, bisect
from collections import namedtuple
from sympy import symbols, diff, Eq, solve
from sympy.abc import t
from sympy.plotting import plot
from tetracamthon.helper import save_attribute_to_pkl, load_attribute_from_pkl


class Coefficient(object):
    def __init__(self, piece_id=None, index_of_order=None):
        self.sym = symbols('C_' + str(piece_id) + str(index_of_order))
        self.val = None

    def __str__(self):
        return str(self.sym) + ": " + str(self.val)

    # def check_out_value_in_solution(self, a_solution):
    #     if self.sym in a_solution:
    #         self.val = a_solution[self.sym]
    #     return self.val


class Polynomial(object):
    def __init__(self,
                 max_order=None,
                 piece_id=None,
                 start_time=None,
                 solution=None,
                 ):
        self.max_order = max_order
        self.piece_id = piece_id
        self.t0 = start_time
        self.co_lis = []
        self.expr_with_co_sym = [self.init_expr_with_co_sym()]
        self.expr_with_co_sym.extend(self.diffs(self.expr_with_co_sym[0]))
        self.expr_with_co_val = []

    def __str__(self):
        result = ""
        if len(self.expr_with_co_val):
            expressions = self.expr_with_co_val
        else:
            expressions = self.expr_with_co_sym
        for expr_i in expressions:
            result += "\n" + str(expr_i)
        return result

    def init_expr_with_co_sym(self):
        lis = []
        for index_of_order in range(self.max_order):
            co = Coefficient(self.piece_id, index_of_order=index_of_order)
            self.co_lis.append(co)
            lis.append(co.sym * (t - self.t0) ** index_of_order)
        return sum(lis)

    def diffs(self, expr):
        result = []
        for index_of_depth in range(1, self.max_order):
            result.append(diff(expr, t, index_of_depth))
        return result

    def get_expr_with_co_sym(self):
        if len(self.expr_with_co_sym):
            return self.expr_with_co_sym
        else:
            self.expr_with_co_sym.append(self.init_expr_with_co_sym())
            self.expr_with_co_sym.extend(self.diffs(self.expr_with_co_sym[0]))
            return self.expr_with_co_sym

    def update_expr_and_diffs_with_co_val(self, solution):
        expr = self.expr_with_co_sym[0]
        for index_of_order in range(self.max_order):
            co_i = self.co_lis[index_of_order]
            co_i.val = solution[co_i.sym]
            expr = expr.subs(co_i.sym, co_i.val)
        self.expr_with_co_val.clear()
        self.expr_with_co_val.append(expr)
        self.expr_with_co_val.extend(self.diffs(expr))
        return self.expr_with_co_val

    def get_expr_with_co_val(self):
        if len(self.expr_with_co_val):
            return self.expr_with_co_val
        else:
            raise ValueError


class KnotPVAJP(object):
    def __init__(self, knot_id=None, knot=None, pvajp=None, smooth_depth=None):
        self.knot_id = knot_id
        self.knot = knot
        self.pvajp = pvajp
        self.smooth_depth = smooth_depth

    def __str__(self):
        result = "\n"
        result += 'Knot: "' + str(self.knot_id) + '"'
        result += " at " + str(self.knot) + "\n"
        result += "Position:     " + str(self.pvajp[0]) + "\n"
        result += "Velocity:     " + str(self.pvajp[1]) + "\n"
        result += "Acceleration: " + str(self.pvajp[2]) + "\n"
        result += "Jerk:         " + str(self.pvajp[3]) + "\n"
        result += "Ping:         " + str(self.pvajp[4]) + "\n"
        result += "With smooth depth of " + str(self.smooth_depth)
        return result


class KnotsInSpline(object):
    def __init__(self, path_to_csv="/Users/johnqu/PycharmProjects/"
                                   "Tetracamthon/data/sample_knots.csv"):
        self.knots_with_info = []
        self.read_in_csv_data(path_to_csv=path_to_csv)

    def read_in_csv_data(self, path_to_csv):
        """Get 360 degree york and jaw acceleration data from a csv file."""
        with open(path_to_csv) as f:
            f_csv = csv.reader(f)
            headings = next(f_csv)
            Row = namedtuple('Row', headings)
            for r in f_csv:
                row = Row(*r)
                self.knots_with_info.append(
                    KnotPVAJP(
                        knot_id=str(row.knot_id),
                        knot=float(row.knot),
                        pvajp=(
                            float(row.position),
                            float(row.velocity),
                            float(row.acceleration),
                            float(row.jerk),
                            float(row.ping)
                        ),
                        smooth_depth=int(row.smooth_depth)
                    )
                )
        return self


class Spline(object):
    def __init__(self,
                 max_order=None,
                 a_set_of_informed_knots=None,
                 name=None,
                 whether_reload=False):
        self.name = name
        self.max_order = max_order
        self.num_of_knots = len(a_set_of_informed_knots.knots_with_info)
        self.knots = [a_set_of_informed_knots.knots_with_info[i].knot
                      for i in range(self.num_of_knots)]
        self.pvajps = [a_set_of_informed_knots.knots_with_info[i].pvajp
                       for i in range(self.num_of_knots)]
        self.depths = [a_set_of_informed_knots.knots_with_info[i].smooth_depth
                       for i in range(self.num_of_knots)]
        self.num_of_pieces = len(self.knots) - 1
        if whether_reload:
            self.load_solved_pieces_of_polynomial()
            self.load_conditional_equations()
            self.load_variables()
            self.load_solution()
        else:
            self.pieces_of_polynomial = []
            self.interpolating_equations = []
            self.smoothness_equations = []
            self.periodic_equations = []
            self.variables = []
            self.solution = {}
            self.solve_spline_pieces()
            self.save_solved_pieces_of_polynomial()
            self.save_solution()
            self.save_conditional_equations()
            self.save_variables()

    def build_polynomials(self):
        for piece_id in range(self.num_of_pieces):
            start_t = self.knots[piece_id]
            polynomial_i = Polynomial(max_order=self.max_order,
                                      piece_id=piece_id,
                                      start_time=start_t)
            self.pieces_of_polynomial.append(polynomial_i)
        return self.pieces_of_polynomial

    def get_pieces_of_polynomial(self):
        if len(self.pieces_of_polynomial):
            return self.pieces_of_polynomial
        else:
            return self.build_polynomials()

    def collect_variables(self):
        polynomials = self.get_pieces_of_polynomial()
        for polynomial_i in polynomials:
            self.variables.extend([co.sym for co in polynomial_i.co_lis])
        return self.variables

    def get_variables(self):
        if len(self.variables):
            return self.variables
        else:
            return self.collect_variables()

    def construct_interpolating_condition_equations(self):
        for index_of_knot in range(len(self.knots)):
            knot_i = self.knots[index_of_knot]
            if index_of_knot == 0:
                polynomial_i = self.get_pieces_of_polynomial()[0]
            else:
                polynomial_i = self.get_pieces_of_polynomial(
                )[index_of_knot - 1]
            expr_i_with_coe = polynomial_i.get_expr_with_co_sym()
            for index_in_depth in range(5):
                if isnan(self.pvajps[index_of_knot][index_in_depth]):
                    continue
                else:
                    equation_k_d = Eq(
                        expr_i_with_coe[index_in_depth].subs(t, knot_i),
                        self.pvajps[index_of_knot][index_in_depth]
                    )
                    self.interpolating_equations.append(equation_k_d)
        return self.interpolating_equations

    def get_interpolating_condition_equations(self):
        if len(self.interpolating_equations):
            return self.interpolating_equations
        else:
            return self.construct_interpolating_condition_equations()

    def construct_smoothness_condition_equations(self):
        for index_of_knot in range(1, self.num_of_knots - 1):
            knot_i = self.knots[index_of_knot]
            piece_before_i = self.get_pieces_of_polynomial()[index_of_knot - 1]
            piece_after_i = self.get_pieces_of_polynomial()[index_of_knot]
            for index_of_depth in range(self.depths[index_of_knot]):
                equation_of_depth_at_knot = Eq(
                    piece_before_i.get_expr_with_co_sym()[index_of_depth].subs(
                        t, knot_i),
                    piece_after_i.get_expr_with_co_sym()[index_of_depth].subs(
                        t, knot_i)
                )
                self.smoothness_equations.append(equation_of_depth_at_knot)
        return self.smoothness_equations

    def get_smoothness_condition_equations(self):
        if len(self.smoothness_equations):
            return self.smoothness_equations
        else:
            return self.construct_smoothness_condition_equations()

    def construct_periodic_condition_equations(self):
        knot_0 = self.knots[0]
        piece_0 = self.get_pieces_of_polynomial()[0]
        knot_m1 = self.knots[-1]
        piece_m1 = self.get_pieces_of_polynomial()[-1]
        for index_of_depth in range(self.depths[0]):
            equation_of_depth_at_knot = Eq(
                piece_0.get_expr_with_co_sym()[index_of_depth].subs(
                    t, knot_0),
                piece_m1.get_expr_with_co_sym()[index_of_depth].subs(
                    t, knot_m1)
            )
            self.periodic_equations.append(equation_of_depth_at_knot)
        return self.smoothness_equations

    def get_periodic_condition_equations(self):
        if len(self.periodic_equations):
            return self.periodic_equations
        else:
            return self.construct_periodic_condition_equations()

    def get_total_equations(self):
        result = []
        result.extend(self.get_interpolating_condition_equations())
        result.extend(self.get_smoothness_condition_equations())
        result.extend(self.get_periodic_condition_equations())
        print("Called get_total_equations once.")
        return result

    def solve_to_solution(self):
        equations = self.get_total_equations()
        variables = self.get_variables()
        self.solution = solve(equations, variables)
        return self.solution

    def solve_spline_pieces(self):
        for a_polynomial in self.get_pieces_of_polynomial():
            a_polynomial.update_expr_and_diffs_with_co_val(
                self.solve_to_solution()
            )
        return self.get_pieces_of_polynomial()

    def save_solved_pieces_of_polynomial(self):
        name = self.name + "_pieces_of_polynomial"
        save_attribute_to_pkl(name, self.get_pieces_of_polynomial())

    def load_solved_pieces_of_polynomial(self):
        name = self.name + "_pieces_of_polynomial"
        self.pieces_of_polynomial = load_attribute_from_pkl(name)
        return self.pieces_of_polynomial

    def save_conditional_equations(self):
        name = self.name + "_conditional_equations"
        data = (
            self.interpolating_equations,
            self.smoothness_equations,
            self.periodic_equations
        )
        save_attribute_to_pkl(name, data)

    def load_conditional_equations(self):
        name = self.name + "_conditional_equations"
        (
            self.interpolating_equations,
            self.smoothness_equations,
            self.periodic_equations
        ) = load_attribute_from_pkl(name)

    def save_variables(self):
        name = self.name + "_variables"
        save_attribute_to_pkl(name, self.get_variables())

    def load_variables(self):
        name = self.name + "_variables"
        self.variables = load_attribute_from_pkl(name)

    def save_solution(self):
        name = self.name + "_solution"
        save_attribute_to_pkl(name, self.solution)

    def load_solution(self):
        name = self.name + "_solution"
        self.solution= load_attribute_from_pkl(name)

    def find_index_of_piece_of_point(self, t_point):
        index = bisect(self.knots, t_point)
        if index == 0:
            result = 0
        elif index == len(self.knots):
            result = len(self.knots) - 2
        else:
            result = index -1
        return result

    def get_polynomial_at_point(self, t_point):
        index_of_piece = self.find_index_of_piece_of_point(t_point)
        return self.get_pieces_of_polynomial()[index_of_piece]

    def get_pvajp_at_point(self, t_point):
        polynomial = self.get_polynomial_at_point(t_point)
        expressions = polynomial.get_expr_with_co_val()
        result = []
        for index_of_depth in range(5):
            result.append(expressions[index_of_depth].subs(t, t_point))
        return result

    def prepare_plots_for_plt(self, line_color='blue'):
        result = []
        for index_of_depth in range(4):
            result.append(
                plot(0, (t, self.knots[0], self.knots[-1]), show=False)
            )
        for index_of_piece in range(self.num_of_pieces):
            polynomial = self.get_pieces_of_polynomial()[index_of_piece]
            for index_of_depth in range(4):
                expression = polynomial.get_expr_with_co_val()[index_of_depth]
                result[index_of_depth].extend(
                    plot(expression,
                         (t,
                          self.knots[index_of_piece],
                          self.knots[index_of_piece + 1]),
                         show=False,
                         line_color=line_color)
                )
        return result


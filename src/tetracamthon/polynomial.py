import csv
from collections import namedtuple
from sympy import symbols, diff, Eq
from math import isnan
from sympy.abc import t


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
        for expr_i in self.expr_with_co_sym:
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
                 name=None):
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
        self.pieces_of_polynomial = []
        self.equations = []
        self.variables = []
        self.solution = {}

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
        for i in range(self.num_of_pieces):
            polynomial_i = self.get_pieces_of_polynomial()[i]
            coefficients_i = polynomial_i.co_lis
            self.variables.extend(coefficients_i)
        return self.variables

    def get_variables(self):
        if len(self.variables):
            return self.variables
        else:
            return self.collect_variables()

    def construct_interpolating_condition_equations(self):
        num_of_interpolating_condition_equations = 0
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
                    self.equations.append(equation_k_d)
                    num_of_interpolating_condition_equations += 1
        return self.equations[-num_of_interpolating_condition_equations:]

    def construct_smoothness_condition_equations(self):
        num_of_smoothness_condition_equations = 0
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
                self.equations.append(equation_of_depth_at_knot)
                num_of_smoothness_condition_equations += 1
        return self.equations[-num_of_smoothness_condition_equations:]

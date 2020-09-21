import csv
from math import isnan
from bisect import bisect_left, bisect
from collections import namedtuple
from sympy import symbols, diff, Eq, solve, lambdify, S, re, im
from sympy.abc import t
from sympy.plotting import plot
from tetracamthon.helper import save_attribute_to_pkl, \
    load_attribute_from_pkl, trans_degree_to_time, move_sympy_plot_to_plt_axes, \
    trans_time_to_degree, find_file_name_from_a_path
import matplotlib.pyplot as plt
import numpy as np


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
        self.lamb_lis = []

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
        # for index_of_depth in range(1, self.max_order):
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
        self.fill_expr_lis_with_diff(expr)
        return self.expr_with_co_val

    def fill_expr_lis_with_diff(self, expr):
        self.expr_with_co_val.clear()
        self.expr_with_co_val.append(expr)
        self.expr_with_co_val.extend(self.diffs(expr))

    def get_expr_with_co_val(self):
        if len(self.expr_with_co_val):
            return self.expr_with_co_val
        else:
            raise ValueError

    def lambdify_polynomial(self):
        for expr_i in self.get_expr_with_co_val():
            self.lamb_lis.append(
                lambdify(t, expr_i, 'numpy')
            )


class KnotPVAJP(object):
    def __init__(self,
                 knot_id,
                 knot,
                 polynomial_order,
                 pvajp,
                 smooth_depth):
        self.knot_id = knot_id
        self.knot = knot
        self.polynomial_order = polynomial_order
        self.pvajp = pvajp
        self.smooth_depth = smooth_depth

    def __str__(self):
        result = 'Knot: "' + str(self.knot_id) + '"'
        result += " at " + str(self.knot) + " deg "
        for data in self.pvajp:
            result += "{0:12}".format(data)
        result += " Smooth depth: " + str(self.smooth_depth)
        result += " with piece order: " + str(self.polynomial_order)
        return result


class KnotsInSpline(object):
    def __init__(self, knots_info_csv="/Users/johnqu/PycharmProjects/"
                                      "tetracamthon/data/sample_knots.csv"):
        self.knots_with_info = []
        self.csv_file_name = find_file_name_from_a_path(knots_info_csv)
        self.read_in_csv_data(path_to_knots_csv=knots_info_csv)

    def __str__(self):
        result = ""
        for knot_with_info in self.knots_with_info:
            result += str(knot_with_info) + "\n"
        return result

    def read_in_csv_data(self, path_to_knots_csv):
        """Get 360 degree york and jaw acceleration data from a csv file."""
        with open(path_to_knots_csv) as f:
            f_csv = csv.reader(f)
            headings = next(f_csv)
            Row = namedtuple('Row', headings)
            for r in f_csv:
                row = Row(*r)
                self.knots_with_info.append(
                    KnotPVAJP(
                        knot_id=str(row.knot_id),
                        knot=float(row.knot),
                        polynomial_order=int(
                            row.polynomial_order),
                        pvajp=[
                            float(row.position),
                            float(row.velocity),
                            float(row.acceleration),
                            float(row.jerk),
                            float(row.ping)
                        ],
                        smooth_depth=int(row.smooth_depth)
                    )
                )
        return self

    def change_boundary_knot_info(
            self,
            start_or_end: str,
            knot=None,
            pos=None,
            vel=None,
            acc=None,
            jer=None,
            pin=None,
    ):
        if start_or_end == 'start':
            index = 0
        else:
            index = -1
        knot_with_info = self.knots_with_info[index]
        if knot:
            knot_with_info.knot = knot
        if pos:
            knot_with_info.pvajp[0] = pos
        if vel:
            knot_with_info.pvajp[1] = vel
        if acc:
            knot_with_info.pvajp[2] = acc
        if jer:
            knot_with_info.pvajp[3] = jer
        if pin:
            knot_with_info.pvajp[4] = pin
        return knot_with_info


class Spline(object):
    def __init__(self,
                 name=None,
                 a_set_of_informed_knots=None,
                 whether_reload=False,
                 whether_trans_knots_degree_to_time=True,
                 whether_solve=True,
                 ):
        self.name = name
        self.informed_knots = a_set_of_informed_knots
        self.num_of_knots = len(self.informed_knots.knots_with_info)
        self.max_orders = [self.informed_knots.knots_with_info[
                               i].polynomial_order
                           for i in range(self.num_of_knots)]
        self.knots = [self.informed_knots.knots_with_info[i].knot
                      for i in range(self.num_of_knots)]
        if whether_trans_knots_degree_to_time:
            self.knots = trans_degree_to_time(self.knots)
        self.pvajps = [self.informed_knots.knots_with_info[i].pvajp
                       for i in range(self.num_of_knots)]
        self.depths = [self.informed_knots.knots_with_info[i].smooth_depth
                       for i in range(self.num_of_knots)]
        self.num_of_pieces = len(self.knots) - 1
        if whether_reload:
            self.load_solved_pieces_of_polynomial()
            self.load_conditional_equations()
            self.load_variables()
            self.load_solution()
        else:
            self.pieces_of_polynomial = []
            self.build_polynomials()
            self.interpolating_equations = []
            self.smoothness_equations = []
            self.periodic_equations = []
            self.variables = []
            self.solution = {}
            if whether_solve:
                self.solve_spline_pieces()
                self.save_solved_pieces_of_polynomial()
                self.save_solution()
                self.save_conditional_equations()
                self.save_variables()

    def build_polynomials(self):
        for piece_id in range(self.num_of_pieces):
            start_t = self.knots[piece_id]
            polynomial_i = Polynomial(max_order=self.max_orders[piece_id],
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
        return self.periodic_equations

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
        self.solution = load_attribute_from_pkl(name)

    def get_index_of_piece_of_point(self, t_point):
        index = bisect(self.knots, t_point)
        if index == 0:
            result = 0
        elif index == len(self.knots):
            result = len(self.knots) - 2
        else:
            result = index - 1
        return result

    def get_polynomial_at_point(self, t_point):
        index_of_piece = self.get_index_of_piece_of_point(t_point)
        return self.get_pieces_of_polynomial()[index_of_piece]

    def get_pvajp_at_point(self, t_point, to_depth=5):
        polynomial = self.get_polynomial_at_point(t_point)
        expressions = polynomial.get_expr_with_co_val()
        result = []
        for index_of_depth in range(to_depth):
            result.append(expressions[index_of_depth].subs(t, t_point))
        return result

    def get_a_dyn_at_boundary(self, start_or_end: str, i_pvajp: int):
        if start_or_end == 'start':
            index = 0
        else:
            index = -1
        expression = self.pieces_of_polynomial[index].expr_with_co_val[i_pvajp]
        result = expression.subs(t, self.knots[index])
        return result

    def prepare_plots_for_plt(self, line_color='blue'):
        result = []
        for index_of_depth in range(max([
            self.get_pieces_of_polynomial()[i].max_order for i in range(
                self.num_of_pieces)
        ])):
            result.append(
                plot(0, (t, self.knots[0], self.knots[-1]), show=False)
            )
        for index_of_piece in range(self.num_of_pieces):
            polynomial = self.get_pieces_of_polynomial()[index_of_piece]
            for index_of_depth in range(polynomial.max_order):
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

    def plot_spline_on_subplots(self,
                                axs_num=4,
                                whether_save_png=False,
                                whether_show_figure=False,
                                whether_knots_ticks=True,
                                whether_annotate=False,
                                fig_title=None
                                ):
        cur_lis = self.prepare_plots_for_plt()
        knots = self.knots
        fig, axs = plt.subplots(nrows=axs_num,
                                # fig, axs=plt.subplots(nrows=len(cur_lis),
                                figsize=(16, 10),
                                )
        if fig_title:
            fig.suptitle(fig_title, fontsize=14, fontweight='bold')
        else:
            fig.suptitle('PVAJ Curves of {} \n with {}.csv'.format(
                self.name, self.informed_knots.csv_file_name),
                fontsize=14, fontweight='bold')
        y_labels = [
            "Position\n(mm)",
            "Velocity \n(mm/sec)",
            "Acceleration \n(mm/sec^2)",
            "Jerk \n(mm/sec^3)"
        ]
        x_tick_labels = ["Pos: ", "Vel: ", "Acc: ", "Jer: "]
        for i in range(len(axs)):
            move_sympy_plot_to_plt_axes(cur_lis[i], axs[i])
            if whether_annotate:
                self.annotate_peak_points(axs, i)
            axs[i].set_ylabel(y_labels[i])
            axs[i].tick_params(labelcolor='tab:gray')
            axs[i].set_xlabel('machine degree')
            if whether_knots_ticks:
                axs[i].set_xticks([knots[j] for j in range(len(knots))])
                axs[i].set_xticklabels([(k % 2) * '\n\n' + str(
                    round(trans_time_to_degree(knots[k]), 1)
                ) +
                                        " ord: " + str(self.max_orders[k]) +
                                        '\n' + x_tick_labels[i] +
                                        str(self.pvajps[k][i])
                                        for k in range(len(knots))])
            else:
                axs[i].set_xticks(trans_degree_to_time(
                    np.linspace(0, 360, 37, endpoint=True)))
                axs[i].set_xticklabels([(i % 2) * '\n' + str(
                    int(np.linspace(0, 360, 37, endpoint=True)[i]))
                                        for i in range(37)])
            axs[i].grid(True)
        fig.align_ylabels(axs)
        if whether_save_png:
            plt.savefig("/Users/johnqu/PycharmProjects/tetracamthon/"
                        "plots/plot_of_{}.png".format(self.name), dpi=720)
        if whether_show_figure:
            plt.show()
        return fig, axs

    def annotate_peak_points(self, axs, i_of_depth):
        zero_points = self.calculate_peak_points()
        for i_of_piece in range(len(zero_points)):
            zero_points_in_piece = zero_points[i_of_piece]
            try:
                peak_points_in_depth = zero_points_in_piece[i_of_depth + 1]
            except IndexError:
                continue
            for t_point in peak_points_in_depth:
                val_point = self.get_pvajp_at_point(t_point)[i_of_depth]
                axs[i_of_depth].scatter([t_point, ],
                                        [val_point, ],
                                        12,
                                        color='blue')
                axs[i_of_depth].annotate(
                    "(" + str(round(trans_time_to_degree(t_point), 1)) + ', ' +
                    str(round(val_point, 1)) + ")",
                    xy=(t_point, val_point),
                    xycoords='data',
                    xytext=(-10, -30),
                    textcoords='offset points',
                    fontsize=10,
                    arrowprops=dict(arrowstyle="->",
                                    connectionstyle="arc3,rad=.2")
                )

    def calculate_peak_points(self):
        result = []
        for i_of_piece in range(self.num_of_pieces):
            piece_of_polynomial = self.get_pieces_of_polynomial()[i_of_piece]
            result_in_piece = []
            for expr_of_depth in piece_of_polynomial.get_expr_with_co_val():
                result_in_depth = []
                solutions = solve(expr_of_depth, t)
                for a_solution in solutions:
                    if a_solution in S.Complexes:
                        imaginary_part = im(a_solution).as_real_imag()[0]
                        if imaginary_part < 0.0001:
                            a_solution = re(a_solution)
                        else:
                            continue
                    if (self.knots[i_of_piece] <= a_solution
                            <= self.knots[i_of_piece + 1]):
                        result_in_depth.append(a_solution)
                result_in_piece.append(result_in_depth)
            result.append(result_in_piece)
        return result

    def modify_knot_value(self, knot_id, depth_of_value, value):
        for knot_with_info in self.informed_knots.knots_with_info:
            if knot_with_info.knot_id == knot_id:
                knot_with_info.pvajp[depth_of_value] = value
                return knot_with_info

    def get_knot_with_info_by_knot_id(self, a_knot_id: str):
        for knot_with_info in self.informed_knots.knots_with_info:
            if knot_with_info.knot_id == a_knot_id:
                return knot_with_info

    def modify_knot(self, a_knot_id, knot):
        the_knot_with_info = self.get_knot_with_info_by_knot_id(a_knot_id)
        the_knot_with_info.knot = knot
        return the_knot_with_info

    def insert_knot_with_info(self, knot_with_info, index_of_insert):
        self.informed_knots.knots_with_info.insert(
            index_of_insert, knot_with_info
        )

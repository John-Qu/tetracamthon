import csv
from collections import namedtuple

from sympy import symbols, cos, pi, atan2, sqrt, solve, sin, Function, \
    Derivative, Eq, diff
from sympy.abc import t
from sympy.parsing.sympy_parser import parse_expr

from tetracamthon.helper import Variable, Memory, trans_degree_to_time, \
    trans_time_to_degree
from tetracamthon.package import Package
from tetracamthon.stage import JawToYork


class Link(object):
    def __init__(self, name):
        self.name = name
        self.r = Variable("r_" + name)  # length of vector
        self.o = Variable("o_" + name)  # orientation of vector
        self.x = Variable("x_" + name)  # vector length projected to x axle
        self.y = Variable("y_" + name)  # vector length projected to y axle
        self.vr = Variable("vr_" + name)
        self.vx = Variable("vx_" + name)
        self.vy = Variable("vy_" + name)

    def set_x_exp(self):
        self.x.exp = self.r.sym * cos(self.o.sym)
        return self.x.exp

    def get_x_exp(self):
        self.set_x_exp()
        return self.x.exp


class BC(Link):
    def __init__(self, r_value, o_value=None):
        Link.__init__(self, "BC")
        self.r.set_value(r_value)
        if o_value:
            self.o.set_value(o_value)


class BO4(Link):
    def __init__(self, r_value, o_value=None):
        Link.__init__(self, "BO4")
        self.r.set_value(r_value)
        if o_value:
            self.o.set_value(o_value)


class CO2(Link):
    def __init__(self, r_value, o_value=None):
        Link.__init__(self, "CO2")
        self.r.set_value(r_value)
        if o_value:
            self.o.set_value(o_value)


class AD(Link):
    def __init__(self, r_value, o_value=None):
        Link.__init__(self, "AD")
        self.r.set_value(r_value)
        if o_value:
            self.o.set_value(o_value)


class DC(Link):
    def __init__(self, r_value, o_value=None):
        Link.__init__(self, "DC")
        self.r.set_value(r_value)
        if o_value:
            self.o.set_value(o_value)


class AC(Link):
    def __init__(self, r_value, o_value=None):
        Link.__init__(self, "AC")
        self.r.set_value(r_value)
        if o_value:
            self.o.set_value(o_value)


class O4O2(Link):
    def __init__(self, r_value, o_value=None):
        Link.__init__(self, "O4O2")
        self.r.set_value(r_value)
        if o_value:
            self.o.set_value(o_value)


class AO2(Link):
    def __init__(self, r_value, o_value=None):
        Link.__init__(self, "AO2")
        self.r.set_value(r_value)
        if o_value:
            self.o.set_value(o_value)


class LinkDimension(object):
    def __init__(self, path_to_link_dim_csv):
        self.spec_id = []
        self.r_BO4 = []
        self.r_BC = []
        self.r_CO2 = []
        self.r_DC = []
        self.r_AD = []
        self.o_O4O2 = []
        self.o_CO2 = []
        self.read_in_csv_data(path_to_link_dim_csv)

    def read_in_csv_data(self, path_to_link_dim_csv):  # test passed
        with open(path_to_link_dim_csv) as f:
            f_csv = csv.reader(f)
            headings = next(f_csv)
            Row = namedtuple('Row', headings)
            for r in f_csv:
                row = Row(*r)
                self.spec_id.append(str(row.spec_id))
                self.r_BO4.append(float(row.r_BO4))
                self.r_BC.append(float(row.r_BC))
                self.r_CO2.append(float(row.r_CO2))
                self.r_DC.append(float(row.r_DC))
                self.r_AD.append(parse_expr(row.r_AD).evalf())
                self.o_O4O2.append(parse_expr(row.o_O4O2).evalf())
                self.o_CO2.append(parse_expr(row.o_CO2).evalf())
        return self


class LinksWithDim(object):
    def __init__(self, a_spec_id, path_to_link_dim_csv):  # test passed
        link_dims = LinkDimension(path_to_link_dim_csv)
        self.spec_id = a_spec_id
        index = link_dims.spec_id.index(self.spec_id)
        self.lBO4 = BO4(link_dims.r_BO4[index])
        self.lBC = BC(link_dims.r_BC[index])
        self.lCO2 = CO2(link_dims.r_CO2[index],
                        o_value=link_dims.o_CO2[index])
        self.lDC = DC(link_dims.r_DC[index])
        self.lAD = AD(link_dims.r_AD[index])
        self.lAC = AC(sqrt(self.lAD.r.val ** 2 + self.lDC.r.val ** 2))
        self.lO4O2 = O4O2(None, o_value=link_dims.o_O4O2[index])
        self.lBC.o.sym = symbols("theta")
        self.lBO4.o.sym = symbols("alpha")
        self.ang_ACD_val = atan2(self.lAD.r.val, self.lDC.r.val)
        self.ang_DCB_val = (110 / 180 * pi).evalf()
        self.lAO2 = AO2(None, None)


class SlideRocker(LinksWithDim):
    def __init__(self, name, a_spec_id, path_to_link_dim_csv):
        LinksWithDim.__init__(self, a_spec_id, path_to_link_dim_csv)
        self.name = name
        self.r = Function("r")(t)
        self.v = Function("v")(t)
        self.memo = Memory(self.name + "_of_dim_set_" + str(self.spec_id))
        self.memo.load()

    def get_equation_of_r_O4O2_and_o_BC(self):
        name = "equation_of_r_O4O2_and_o_BC"
        if name in self.memo.dict:
            return self.memo.dict[name]
        x_eq_zero = (
                self.lO4O2.r.sym * cos(self.lO4O2.o.sym)
                + self.lBO4.r.sym * cos(self.lBO4.o.sym)
                - self.lBC.r.sym * cos(self.lBC.o.sym)
                - self.lCO2.r.sym * cos(self.lCO2.o.sym)
        )
        y_eq_zero = (
                self.lO4O2.r.sym * sin(self.lO4O2.o.sym)
                + self.lBO4.r.sym * sin(self.lBO4.o.sym)
                - self.lBC.r.sym * sin(self.lBC.o.sym)
                - self.lCO2.r.sym * sin(self.lCO2.o.sym)
        )
        alpha_expr = solve(x_eq_zero, self.lBO4.o.sym)[1]  # the second counts.
        y_eq_zero_without_alpha = y_eq_zero.subs(
            self.lBO4.o.sym, alpha_expr)
        result = y_eq_zero_without_alpha.subs([
            (self.lBC.r.sym, self.lBC.r.val),
            (self.lBO4.r.sym, self.lBO4.r.val),
            (self.lCO2.r.sym, self.lCO2.r.val),
            (self.lO4O2.o.sym, self.lO4O2.o.val),
            (self.lCO2.o.sym, self.lCO2.o.val)]).evalf()
        self.memo.update_memo(name, result)
        return result

    def get_equation_of_x_AO2_and_o_BC(self):
        name = "equation_of_x_AO2_and_o_BC"
        if name in self.memo.dict:
            return self.memo.dict[name]
        expr_x_AO2_and_o_BC = \
            self.lAO2.x.sym + \
            self.lCO2.r.sym - \
            self.lAC.r.sym * cos(
                self.lBC.o.sym - self.ang_ACD_val - self.ang_DCB_val)
        result = expr_x_AO2_and_o_BC.subs([
            (self.lCO2.r.sym, self.lCO2.r.val),
            (self.lAC.r.sym, self.lAC.r.val),
        ]).evalf()
        self.memo.update_memo(name, result)
        return result

    def get_equation_of_y_AO2_and_o_BC(self):
        name = "equation_of_y_AO2_and_o_BC"
        if name in self.memo.dict:
            return self.memo.dict[name]
        expr_y_AO2_and_o_BC = \
            self.lAO2.y.sym - \
            self.lAC.r.sym * sin(
                self.lBC.o.sym - self.ang_ACD_val - self.ang_DCB_val)
        result = expr_y_AO2_and_o_BC.subs([
            (self.lAC.r.sym, self.lAC.r.val),
        ]).evalf()
        self.memo.update_memo(name, result)
        return result


class Forward(SlideRocker):
    def __init__(self,
                 name: str,
                 a_spec_id: str,
                 path_to_link_dim_csv: str):
        SlideRocker.__init__(self, name, a_spec_id, path_to_link_dim_csv)

    def get_o_BC_of_r_O4O2(self):
        name = "o_BC_of_r_O4O2"
        if name in self.memo.dict:
            return self.memo.dict[name]
        result = solve(self.get_equation_of_r_O4O2_and_o_BC(),
                       self.lBC.o.sym)[1]
        self.memo.update_memo(name, result)
        return result

    def get_x_AO2_of_o_BC(self):
        name = "x_AO2_of_o_BC"
        if name in self.memo.dict:
            return self.memo.dict[name]
        result = solve(self.get_equation_of_x_AO2_and_o_BC(),
                       self.lAO2.x.sym)[0]
        self.memo.update_memo(name, result)
        return result

    def get_x_AO2_of_r_O4O2(self):
        name = "x_AO2_of_r_O4O2"
        if name in self.memo.dict:
            return self.memo.dict[name]
        result = self.get_x_AO2_of_o_BC().subs(
            [(self.lBC.o.sym, self.get_o_BC_of_r_O4O2())])
        self.memo.update_memo(name, result)
        return result

    def get_y_AO2_of_o_BC(self):
        name = "y_AO2_of_o_BC"
        if name in self.memo.dict:
            return self.memo.dict[name]
        result = solve(self.get_equation_of_y_AO2_and_o_BC(),
                       self.lAO2.y.sym)[0]
        self.memo.update_memo(name, result)
        return result

    def get_y_AO2_of_r_O4O2(self):
        name = "y_AO2_of_r_O4O2"
        if name in self.memo.dict:
            return self.memo.dict[name]
        result = self.get_y_AO2_of_o_BC().subs(
            [(self.lBC.o.sym, self.get_o_BC_of_r_O4O2())])
        self.memo.update_memo(name, result)
        return result

    def get_vx_AO2_of_vr_O4O2(self):
        name = "vx_AO2_of_vr_O4O2"
        if name in self.memo.dict:
            return self.memo.dict[name]
        vx_AO2 = self.get_x_AO2_of_r_O4O2().subs(
            [(self.lO4O2.r.sym, self.r)]).diff(t)
        result = vx_AO2.subs(Derivative(self.r, t), self.v)
        self.memo.update_memo(name, result)
        return result

    def get_vy_AO2_of_vr_O4O2(self):
        name = "vy_AO2_of_vr_O4O2"
        if name in self.memo.dict:
            return self.memo.dict[name]
        vy_AO2 = self.get_y_AO2_of_r_O4O2().subs(
            [(self.lO4O2.r.sym, self.r)]).diff(t)
        result = vy_AO2.subs(Derivative(self.r, t), self.v)
        self.memo.update_memo(name, result)
        return result


class Backward(SlideRocker):
    def __init__(self, name, a_spec_id, path_to_link_dim_csv):
        SlideRocker.__init__(self, name, a_spec_id, path_to_link_dim_csv)

    def get_r_O4O2_of_o_BC(self):
        name = "r_O4O2_of_o_BC"
        if name in self.memo.dict:
            return self.memo.dict[name]
        result = solve(self.get_equation_of_r_O4O2_and_o_BC(),
                       self.lO4O2.r.sym)[1]
        # TODO: why the working index is 1 above,
        #  while 0 in ./analysis.ANeedO4.get_r_O4O2_of_theta_expr?
        self.memo.update_memo(name, result)
        return result

    def get_o_BC_of_x_AO2(self):
        name = "o_BC_of_x_AO2"
        if name in self.memo.dict:
            return self.memo.dict[name]
        result = solve(self.get_equation_of_x_AO2_and_o_BC(),
                       self.lBC.o.sym)[1]
        self.memo.update_memo(name, result)
        return result

    def get_o_BC_of_y_AO2(self):
        name = "o_BC_of_y_AO2"
        if name in self.memo.dict:
            return self.memo.dict[name]
        result = solve(self.get_equation_of_y_AO2_and_o_BC(),
                       self.lBC.o.sym)[1]
        self.memo.update_memo(name, result)
        return result

    def get_r_O4O2_of_x_AO2(self):
        name = "r_O4O2_of_x_AO2"
        if name in self.memo.dict:
            return self.memo.dict[name]
        result = self.get_r_O4O2_of_o_BC().subs(
            self.lBC.o.sym, self.get_o_BC_of_x_AO2()
        )
        self.memo.update_memo(name, result)
        return result


class TracingOfPointA(object):
    def __init__(self,
                 name: str,
                 a_spec_id: str,
                 a_package_id: str,
                 a_path_to_link_dim_csv: str,
                 whether_reload: bool = True):
        self.jaw_on_york_spline = JawToYork(whether_reload=whether_reload)
        self.forward = Forward("a_forward_mechanism",
                               a_spec_id,
                               a_path_to_link_dim_csv
                               )
        self.backward = Backward("a_backward_mechanism",
                                 a_spec_id,
                                 a_path_to_link_dim_csv
                                 )
        self.package = Package(a_package_id)
        self.memo = Memory(name +
                           "with" + self.jaw_on_york_spline.name +
                           "for" + a_spec_id)
        self.r_O4O2_of_x_AO2 = self.backward.get_r_O4O2_of_x_AO2()
        self.x_AO2_sym = self.backward.lAO2.x.sym
        self.r_O4O2_sym = self.forward.lO4O2.r.sym
        self.r_O4O2_polynomial_while_touching = \
            self.jaw_on_york_spline.get_polynomial_at_point(
                trans_degree_to_time(85)
            )
        if whether_reload:
            self.memo.load()

    def get_r_O4O2_when_closed(self):
        name = "r_O4O2_when_closed"
        if name in self.memo.dict:
            return self.memo.dict[name]
        x_AO2_when_closed = -1.5 / 2
        result = self.r_O4O2_of_x_AO2.subs(self.x_AO2_sym, x_AO2_when_closed)
        self.memo.update_memo(name, result)
        return result

    def get_r_O4O2_when_touched(self):
        name = "r_O4O2_when_touched"
        if name in self.memo.dict:
            return self.memo.dict[name]
        x_AO2_when_touched = -self.package.depth / 2
        result = self.r_O4O2_of_x_AO2.subs(self.x_AO2_sym, x_AO2_when_touched)
        self.memo.update_memo(name, result)
        return result

    def get_t_touched(self):
        name = "t_touched"
        if name in self.memo.dict:
            return self.memo.dict[name]
        jaw_to_york_spline_pos_touched = - (
                self.get_r_O4O2_when_touched() - self.get_r_O4O2_when_closed()
        )
        the_polynomial = self.r_O4O2_polynomial_while_touching
        the_pos_expr = the_polynomial.get_expr_with_co_val()[0]
        the_equation = Eq(the_pos_expr, jaw_to_york_spline_pos_touched)
        # print(the_equation)
        result = solve(the_equation, t)[2]
        # print(trans_time_to_degree(result))
        self.memo.update_memo(name, result)
        return result

    def get_r_O4O2_of_t_in_jaw_on_york_spline(self):
        name = "r_O4O2_of_t_in_jaw_on_york_spline"
        if name in self.memo.dict:
            return self.memo.dict[name]
        pos_expr_O4_to_O2_in_jaw_on_york_spline = \
            self.r_O4O2_polynomial_while_touching.get_expr_with_co_val()[0]
        result = ((- pos_expr_O4_to_O2_in_jaw_on_york_spline)
                  + self.get_r_O4O2_when_closed())
        self.memo.update_memo(name, result)
        return result

    def get_y_AO2_of_t_while_touching(self):
        name = "y_AO2_of_t_while_touching"
        if name in self.memo.dict:
            return self.memo.dict[name]
        result = self.forward.get_y_AO2_of_r_O4O2().subs(
            self.r_O4O2_sym, self.get_r_O4O2_of_t_in_jaw_on_york_spline())
        self.memo.update_memo(name, result)
        return result

    def get_x_AO2_of_t_while_touching(self):
        name = "x_AO2_of_t_while_touching"
        if name in self.memo.dict:
            return self.memo.dict[name]
        result = self.forward.get_x_AO2_of_r_O4O2().subs(
            self.r_O4O2_sym, self.get_r_O4O2_of_t_in_jaw_on_york_spline())
        self.memo.update_memo(name, result)
        return result

    def get_x_AO5_of_t_while_touching(self):
        name = "x_AO5_of_t_while_touching"
        if name in self.memo.dict:
            return self.memo.dict[name]
        result = self.get_x_AO2_of_t_while_touching()
        self.memo.update_memo(name, result)
        return result

    def get_y_AO5_of_t_while_touching(self):
        name = "y_AO5_of_t_while_touching"
        if name in self.memo.dict:
            return self.memo.dict[name]
        r_GO5 = self.package.depth / 2
        s = self.package.top_gap
        r_AG = ((r_GO5 - 0.75) ** 2 + s ** 2) ** 0.5
        result = (r_AG ** 2 -
                  (r_GO5 + self.get_x_AO5_of_t_while_touching()) ** 2
                  ) ** 0.5
        self.memo.update_memo(name, result)
        return result

    def get_vx_AO5_of_t_while_touching(self):
        name = "vx_AO5_while_touching"
        if name in self.memo.dict:
            return self.memo.dict[name]
        result = diff(self.get_x_AO5_of_t_while_touching(), t)
        self.memo.update_memo(name, result)
        return result



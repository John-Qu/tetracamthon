from sympy import *
from sympy.abc import x

class Point(object):
    def __init__(self, co_type, ori_point, *coord):
        self.ori = ori_point
        if co_type == 'cas':
            self.x = coord[0]  # absolute position
            self.y = coord[1]  # absolute position
            self.r = math.sqrt(self.x**2 + self.y**2)  ## length of vector
            self.t = math.atan2(self.y, self.x)  # theta


class Linkage(object):
    idnum = 1
    def __init__(self, idnum, ori_point):
        self.id = idnum  #Todo: find how to use class attribute
        idnum += 1


init_printing(use_unicode=True)

# Use O2-O4-B-C vector loop, relating theta and r_O4O2
R_O4O2, R_BO4, R_BC, R_CO2 = symbols("R_O4O2, R_BO4, R_BC, R_CO2")
r_O4O2, r_BO4, r_BC, r_CO2 = symbols("r_O4O2, r_BO4, r_BC, r_CO2")
alpha, theta = symbols('alpha, theta')
expr_vector = R_O4O2 + R_BO4 - R_BC - R_CO2
print(latex(r_O4O2*exp(I*3/2*pi) + r_BO4*exp(I*alpha) - r_BC*exp(I*theta) - r_CO2*exp(I*pi)))
expr_x = r_O4O2*cos(3/2*pi) + r_BO4*cos(alpha) - r_BC*cos(theta) - r_CO2*cos(pi)
expr_y = r_O4O2*sin(3/2*pi) + r_BO4*sin(alpha) - r_BC*sin(theta) - r_CO2*sin(pi)
alpha_expr = solve(expr_x, alpha)  # Please use the second root
    # [-acos(-(R_CO2 - r_BC*cos(theta))/r_BO4) + 2*pi, acos((-R_CO2 + r_BC*cos(theta))/r_BO4)]
expr_y_without_alpha = expr_y.subs(alpha, alpha_expr[1]) # use second root, get r = 52.0476394259675
# get r_O4O2 with theta as input
r_O4O2_expr = solve(expr_y_without_alpha, r_O4O2)
r_O4O2_expr_simple = r_O4O2_expr[0].subs([(r_BC, 100), (r_BO4, 155), (r_CO2, 60)])
r_O4O2_min = r_O4O2_expr_simple.subs(theta, 200/180*pi).evalf()
print("r_O4O2 = f(theta): ", latex(r_O4O2_expr_simple))
print("r_O4O2_min: ", r_O4O2_min)
theta_expr = solve(expr_y_without_alpha, theta)
theta_expr_simple = theta_expr[1].subs([(r_BC, 100), (r_BO4, 155), (r_CO2, 60)])
theta_min = (theta_expr_simple.subs(r_O4O2, 52.05) + 2*pi).evalf()
print("theta = function(r_O4O2): ", latex(theta_expr_simple))
print("theta_min(in degree): ", (theta_min/pi*180).evalf())

r_AD, r_DC = symbols("r_AD, r_DC")  # with defaut value pair: (r_AD, 60), (r_DC, 164.44)
angle_ACD = atan2(r_AD, r_DC)
angle_DCB = 110/180*pi
r_AC = sqrt(r_AD**2 + r_DC**2)
# r_AC = sqrt(r_AD**2 + r_DC**2).subs([(r_AD, 60), (r_DC, 164.44)])
R_AC = r_AC*exp(I*(theta - angle_ACD - angle_DCB))
R_CO2 = r_CO2 * exp(I*pi)
R_AO2 = R_AC + R_CO2
# print(R_AO2)
# x_R_AO2 = -r_CO2 + sqrt(r_AD**2 + r_DC**2)*cos(theta - atan2(r_AD, r_DC) - 0.611111111111111*pi)
# y_R_AO2 = sqrt(r_AD**2 + r_DC**2)*sin(theta - atan2(r_AD, r_DC) - 0.611111111111111*pi)
x_R_AO2 = -r_CO2 + r_AC*cos(theta - angle_ACD - angle_DCB)
y_R_AO2 = r_AC*sin(theta - angle_ACD - angle_DCB)
R_AO2_x_zero = x_R_AO2.subs([(r_AD, 60), (r_DC, 164.44), (r_CO2, 60), (theta, theta_min)]).evalf()
R_AO2_y_high = y_R_AO2.subs([(r_AD, 60), (r_DC, 164.44), (r_CO2, 60), (theta, theta_min)]).evalf()
# print("R_AO2_x_zero: ", R_AO2_x_zero)
# print("R_AO2_y_high: ", R_AO2_y_high)
x_AO2, y_AO2 = symbols("x_AO2, y_AO2")
# theta_of_x_AO2 = solve(x_R_AO2 - x_AO2, theta)
theta_of_x_AO2 = solve((x_R_AO2 - x_AO2).subs([(r_AD, 60), (r_DC, 164.44), (r_CO2, 60)]), theta)
# print(theta_of_x_AO2[0].subs(x_AO2, 0))

x_R_AO2_simple = x_R_AO2.subs([(r_AD, 60), (r_DC, 164.44), (r_CO2, 60), (theta, theta_expr_simple)])
y_R_AO2_simple = y_R_AO2.subs([(r_AD, 60), (r_DC, 164.44), (r_CO2, 60), (theta, theta_expr_simple)])
print("x_R_AO2_simple: \n", latex(x_R_AO2_simple))
print("y_R_AO2_simple: \n", latex(y_R_AO2_simple))
print(x_R_AO2_simple.subs(r_O4O2, 52).evalf())
print(y_R_AO2_simple.subs(r_O4O2, 52).evalf())
print(x_R_AO2_simple.subs(r_O4O2, 52+131).evalf())
print(y_R_AO2_simple.subs(r_O4O2, 52+131).evalf())
print(x_R_AO2_simple.subs(r_O4O2, 52+48.33).evalf())
print(y_R_AO2_simple.subs(r_O4O2, 52+48.33).evalf())

r = Function("r")(x)
# r = symbols("r", cls=Function)
# v = Derivative(r, x)
v = Function("v")(x)
print(type(x_R_AO2_simple))
x_R_AO2_simple_velocity = x_R_AO2_simple.subs(r_O4O2, r).diff(x)
y_R_AO2_simple_velocity = y_R_AO2_simple.subs(r_O4O2, r).diff(x)
print(latex(x_R_AO2_simple_velocity))
print(latex(y_R_AO2_simple_velocity))
# print(x_R_AO2_simple_velocity)
x_R_AO2_simple_velocity = x_R_AO2_simple_velocity.subs(Derivative(r, x), v)
y_R_AO2_simple_velocity = y_R_AO2_simple_velocity.subs(Derivative(r, x), v)
print("x_R_AO2_simple_velocity: ", latex(x_R_AO2_simple_velocity))
x_R_AO2_simple_velocity_touch = x_R_AO2_simple_velocity.subs([(v, 800), (r, 100.33)])
y_R_AO2_simple_velocity_touch = y_R_AO2_simple_velocity.subs([(v, 800), (r, 100.33)])
# x_R_AO2_simple_velocity_touch = x_R_AO2_simple_velocity.subs(r, 100.33)
# y_R_AO2_simple_velocity_touch = y_R_AO2_simple_velocity.subs(r, 100.33)
print(x_R_AO2_simple_velocity_touch.evalf())  #TODO: why negative sence?
print(y_R_AO2_simple_velocity_touch.evalf())



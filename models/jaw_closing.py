from jaw_on_york import build_jaw_on_york_curves2
from analysis import O4DriveA
from sympy import lambdify, acos, cot, solve, Eq, diff
from sympy.abc import x
from packages import Package
import numpy as np
from helper_functions import degree_to_time, time_to_degree
import matplotlib.pyplot as plt

joy = build_jaw_on_york_curves2()
j2 = O4DriveA()
curves = joy.get_piecewise_of_x()
touch_time = solve(Eq(joy.get_exprs_of_x()[0][1], -41.1), x)[2]
touch_degree = time_to_degree(touch_time)
close_degree = 138
close_time = degree_to_time(close_degree)
x_R_AO2_of_r_O4O2_expr = j2.get_x_R_AO2_of_r_O4O2_expr()
y_R_AO2_of_r_O4O2_expr = j2.get_y_R_AO2_of_r_O4O2_expr()
x_V_AO2_of_vr_O4O2 = j2.get_x_V_AO2_of_vr_O4O2()
y_V_AO2_of_vr_O4O2 = j2.get_y_V_AO2_of_vr_O4O2()

x_R_AO2 = x_R_AO2_of_r_O4O2_expr.subs(j2.r_O4O2, -(joy.exprs_of_x[0][1]-52.0476394259645))
x_V_AO2 = x_V_AO2_of_vr_O4O2.subs([(j2.r, -(joy.exprs_of_x[0][1]-52.0476394259645)), (j2.v, -joy.exprs_of_x[1][1])])
# joy = build_jaw_on_york_curves()
# j2 = O4DriveA()
# x_R_AO2_of_r_O4O2_expr = j2.get_x_R_AO2_of_r_O4O2_expr()
# y_R_AO2_of_r_O4O2_expr = j2.get_y_R_AO2_of_r_O4O2_expr()
# x_V_AO2_of_vr_O4O2 = j2.get_x_V_AO2_of_vr_O4O2()
# y_V_AO2_of_vr_O4O2 = j2.get_y_V_AO2_of_vr_O4O2()
#
# x_R_AO2 = x_R_AO2_of_r_O4O2_expr.subs(j2.r_O4O2, -(joy.exprs_of_x[0][2]-52.0476394259645))
# x_V_AO2 = x_V_AO2_of_vr_O4O2.subs([(j2.r, -(joy.exprs_of_x[0][2]-52.0476394259645)), (j2.v, -joy.exprs_of_x[1][2])])
# # print(latex(x_V_AO2))print(latex(x_V_AO2))
p330sq = Package(330, "Square", 49.5, 48.5, 124.6, 6, 190)
r = p330sq.depth/2
theta = acos((r + x_R_AO2) / r)
x_V_AO5 = x_V_AO2
y_V_AO5 = x_V_AO5 * cot(theta)
y_A_AO5 = diff(y_V_AO5, x)
# print(latex(y_V_AO5))
f_x_R_AO2 = lambdify(x, x_R_AO2)
f_x_V_AO5 = lambdify(x, x_V_AO5)
f_y_V_AO5 = lambdify(x, y_V_AO5)
f_y_A_AO5 = lambdify(x, y_A_AO5)
t = np.linspace(float(touch_time), float(close_time), num=100, endpoint=True)
degrees = time_to_degree(t)
fig = plt.figure(figsize=(15, 12), dpi=80)
fig.suptitle('R_AO5 SVA curves of \n' +
             str(p330sq),
             fontsize='x-large')
plt.subplot(4, 1, 1)
plt.grid()
plt.ylabel("Position (mm)")
plt.plot(degrees, f_x_R_AO2(t),
         color="blue", linewidth=3.0, linestyle="-")
plt.xlim(float(touch_degree), float(close_degree))
plt.subplot(4, 1, 2)
plt.grid()
plt.ylabel("Velocity of x (mm/s)")
plt.plot(degrees, f_x_V_AO5(t),
         color="blue", linewidth=3.0, linestyle="-")
plt.xlim(float(touch_degree), float(close_degree))
plt.subplot(4, 1, 3)
plt.grid()
plt.ylabel("Velocity of y (mm/s)")
plt.plot(degrees, f_y_V_AO5(t),
         color="blue", linewidth=3.0, linestyle="-")
plt.xlim(float(touch_degree), float(close_degree))
print(p330sq.get_pulling_velocity())
plt.subplot(4, 1, 4)
plt.grid()
plt.ylabel("Acceleration of y (mm/s^2)")
plt.plot(degrees, f_y_A_AO5(t),
         color="blue", linewidth=3.0, linestyle="-")
plt.xlim(float(touch_degree), float(close_degree))


from sympy import *
    # bspline_basis, lambdify, diff, bspline_basis_set
from sympy.abc import x
import numpy as np


def degree_to_radial(degree):
    return (degree/180*pi).evalf()


def radial_to_degree(radial):
    return (radial/pi*180).evalf()


m = 6
d = m - 1
start_end_knot_shape = np.zeros(m)
start_knot = degree_to_radial(82)
end_knot = degree_to_radial(137)
start_knots = np.full_like(start_end_knot_shape, start_knot)
end_knots = np.full_like(start_end_knot_shape, 137)
interior_knots = np.array([])
knots = np.array(list(start_knots) + list(interior_knots) + list(end_knots))
bs = bspline_basis_set(d, knots, x)

s_ry = Function('x')
s_rj = Function('x')
s_ly = Function('x')
num_of_coefficients = len(bs)
coefficients_shape = np.zeros(num_of_coefficients)
# a = np.full_like(coefficients_shape, symbols)
a1, a2, a3, a4, a5, a6 = symbols("a1, a2, a3, a4, a5, a6")
a = [a1, a2, a3, a4, a5, a6]
b1, b2, b3, b4, b5, b6 = symbols("b1, b2, b3, b4, b5, b6")
b = [b1, b2, b3, b4, b5, b6]
c1, c2, c3, c4, c5, c6 = symbols("c1, c2, c3, c4, c5, c6")
c = [c1, c2, c3, c4, c5, c6]
# s_ry = lambdify(x, sum([a[i]*bs[i] for i in range(len(bs))]))
# s_rjy = lambdify(x, sum([b[i]*bs[i] for i in range(len(bs))]))
# s_ly = lambdify(x, sum([c[i]*bs[i] for i in range(len(bs))]))
s_ry = sum([a[i]*bs[i] for i in range(len(bs))])
v_ry = s_ry.diff(x)
a_ry = v_ry.diff(x)
j_ry = a_ry.diff(x)

s_rjy = sum([b[i]*bs[i] for i in range(len(bs))])
v_rjy = s_rjy.diff(x)
a_rjy = v_rjy.diff(x)
j_rjy = a_rjy.diff(x)

s_ly = sum([c[i]*bs[i] for i in range(len(bs))])
v_ly = s_ly.diff(x)
a_ly = v_ly.diff(x)
j_ly = a_ly.diff(x)

s_ry_func = lambdify(x, s_ry)


# d = 0
# knots = range(5)
# bspline_basis(d, knots, 4, x)
# bspline_basis(3, range(5), 0, x)
#
# d = 1
# t = sp.symbols('t')
# knots = [0, 0, t, 3, 4]
# bspline_basis(d, knots, 0, x)
# bspline_basis_set(d, knots, x)
#
# d = 3
# knots = range(10)
# b0 = bspline_basis(d, knots, 0, x)
# f = lambdify(x, b0)
# y = f(array([0.5, 1.5]))
# g = diff(b0, x)
#
# d = 2
# knots = range(5)
# splines = bspline_basis_set(d, knots, x)
#
# d = 5
# knots = np.array([0, 0, 0, 0, 0, 0, 45, 90, 135, 180, 180, 180, 180, 180, 180])*sp.pi/180
# b = sp.bspline_basis_set(d, knots, x)
# f = sp.lambdify(x, b[0])
# from sympy.plotting import plot
# p1 = plot(x*x, show=False)
# p2 = plot(x, show=False)
# p1.append(p2[0])
# p1 = plot(b[0], show=False)
# p2 = plot(b[1], show=False)
# p3 = plot(b[2], show=False)
# p4 = plot(b[3], show=False)
# p5 = plot(b[4], show=False)
# p6 = plot(b[5], show=False)
#
# f = []
# for i in range(len(b)):
#     f.append(sp.lambdify(x, b[i]))
#
# from sympy import evalf
# re = f[3]((sp.pi/4).evalf())
# print(re)
# print(type(f[5](sp.pi/4)))


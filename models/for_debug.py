from sympy import *
from sympy.abc import x
import numpy as np

# order = 6
# degree = order - 1
# knots = np.array(
#     [0, 0,
#      pi / 4, pi / 2, 3 * pi / 4,
#      pi, pi])
# b4 = bspline_basis(degree, knots, 0, x)
# print(latex(b4))
# plot(b4, (x, 0, 180))

knots = np.array(
    [0, 0, 1, 2, 2])
order = len(knots) - 1
degree = order - 1
bs = bspline_basis(degree, knots, 0, x)
print(latex(bs))
plot(bs, (x, 0, knots[-1]),
     title="B-spline of order "+str(order)+"\nwith knots: "+str(knots))

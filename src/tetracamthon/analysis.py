from sympy import *
from sympy.abc import x

init_printing(use_unicode=True)


class JawOnYork(object):
    def __init__(self, machine_type="Flex"):
        """
        -r_O4O2 + 155*sqrt(1 - (100*cos(theta) - 60)**2/24025) - 100*sin(theta)
        """
        r_BC_value = 100
        r_BO4_value = 155
        r_CO2_value = 60
        r_AD_value = 60 - 1.5 / 2
        orient_R_O4O2_value = 3 / 2 * pi
        orient_R_CO2_value = pi
        r_DC_value = 164.22 if machine_type == "CompactFlex" else 182.31
        self.r_O4O2, self.r_BO4, self.r_BC, self.r_CO2 = symbols(
            "r_O4O2, r_BO4, r_BC, r_CO2")
        self.r_AD, self.r_DC = symbols("r_AD, r_DC")
        self.x_R_AO2, self.y_R_AO2 = symbols("x_R_AO2, y_R_AO2")
        self.alpha, self.theta = symbols('alpha, theta')
        self.orient_R_O4O2, self.orient_R_CO2 = symbols(
            "orient_R_O4O2, orient_R_CO2")
        self.orient_R_O4O2_value, self.orient_R_CO2_value = \
            orient_R_O4O2_value, orient_R_CO2_value
        self.r_BC_value = r_BC_value
        self.r_BO4_value = r_BO4_value
        self.r_CO2_value = r_CO2_value
        self.r_AD_value = r_AD_value
        self.r_DC_value = r_DC_value
        self.angle_ACD = atan2(self.r_AD, self.r_DC)
        self.angle_ACD_value = atan2(self.r_AD_value, self.r_DC_value)
        self.angle_DCB = 110 / 180 * pi
        self.angle_DCB_value = (110 / 180 * pi).evalf()
        self.r_AC = sqrt(self.r_AD ** 2 + self.r_DC ** 2)
        self.r_AC_value = self.r_AC.subs([
            (self.r_AD, self.r_AD_value),
            (self.r_DC, self.r_DC_value)
        ]).evalf()

    def get_equation_of_r_O4O2_and_theta(self):
        expr_x_eq_zero = self.r_O4O2 * cos(self.orient_R_O4O2) + \
                         self.r_BO4 * cos(self.alpha) - \
                         self.r_BC * cos(self.theta) - \
                         self.r_CO2 * cos(self.orient_R_CO2)
        expr_y_eq_zero = self.r_O4O2 * sin(self.orient_R_O4O2) \
                         + self.r_BO4 * sin(self.alpha) \
                         - self.r_BC * sin(self.theta) \
                         - self.r_CO2 * sin(self.orient_R_CO2)
        alpha_expr = solve(expr_x_eq_zero, self.alpha)[1]  # second counts.
        expr_y_eq_zero_without_alpha = expr_y_eq_zero.subs(self.alpha,
                                                           alpha_expr)
        equation_of_r_O4O2_and_theta = \
            expr_y_eq_zero_without_alpha.subs([
                (self.r_BC, self.r_BC_value),
                (self.r_BO4, self.r_BO4_value),
                (self.r_CO2, self.r_CO2_value),
                (self.orient_R_O4O2, self.orient_R_O4O2_value),
                (self.orient_R_CO2, self.orient_R_CO2_value)]).evalf()
        return equation_of_r_O4O2_and_theta

    def get_equation_of_x_R_AO2_and_theta(self):
        """
        j1 = JawOnYork()
        print(j1.get_equation_of_x_R_AO2_and_theta())
        """
        expr_x_R_AO2_and_theta = \
            self.x_R_AO2 + \
            self.r_CO2 - \
            self.r_AC * cos(self.theta - self.angle_ACD - self.angle_DCB)
        expr_x_R_AO2_and_theta_simple = expr_x_R_AO2_and_theta.subs([
            (self.r_CO2, self.r_CO2_value),
            (self.r_AC, self.r_AC_value),
            (self.angle_DCB, self.angle_DCB_value),
            (self.angle_ACD, self.angle_ACD_value)
        ]).evalf()
        return expr_x_R_AO2_and_theta_simple

    def get_equation_of_y_R_AO2_and_theta(self):
        """
        j1 = JawOnYork()
        print(j1.get_equation_of_y_R_AO2_and_theta())
        """
        expr_y_R_AO2_and_theta = \
            self.y_R_AO2 - \
            self.r_AC * sin(self.theta - self.angle_ACD - self.angle_DCB)
        expr_y_R_AO2_and_theta_simple = expr_y_R_AO2_and_theta.subs([
            (self.r_AC, self.r_AC_value),
            (self.angle_DCB, self.angle_DCB_value),
            (self.angle_ACD, self.angle_ACD_value)
        ]).evalf()
        return expr_y_R_AO2_and_theta_simple

    def get_equation_of_x_R_AO2_and_y_R_AO2(self):
        equation = \
            (self.x_R_AO2 + self.r_CO2) ** 2 \
            + self.y_R_AO2 ** 2 \
            - self.r_AC ** 2
        equation_simple = equation.subs([
            (self.r_AD, self.r_AD_value),
            (self.r_DC, self.r_DC_value),
            (self.r_CO2, self.r_CO2_value)
        ]).evalf()
        return equation_simple

    def get_x_R_AO2_of_y_R_AO2_expr(self):
        """
        j1 = JawOnYork()
        print(j1.get_x_R_AO2_of_y_R_AO2_expr())
        print(j1.get_x_R_AO2_of_y_R_AO2_expr().subs(j1.y_R_AO2, 164.44))
        """
        x_R_AO2_of_y_R_AO2_expr = solve(
            self.get_equation_of_x_R_AO2_and_y_R_AO2(), self.x_R_AO2)
        return x_R_AO2_of_y_R_AO2_expr[1]

    def get_y_R_AO2_of_x_R_AO2_expr(self):
        """
        j1 = JawOnYork()
        print(j1.get_y_R_AO2_of_x_R_AO2_expr())
        # 0.04*sqrt(-625.0*x_R_AO2**2 - 75000.0*x_R_AO2 + 16900321.0)
        print(j1.get_y_R_AO2_of_x_R_AO2_expr().subs(j1.x_R_AO2, -0.75))
        # 182.310000000000
        """
        y_R_AO2_of_x_R_AO2_expr = solve(
            self.get_equation_of_x_R_AO2_and_y_R_AO2(), self.y_R_AO2)
        return y_R_AO2_of_x_R_AO2_expr[1]

    def __str__(self):
        class_name = "A JawOnYork Class Object: \n"
        linkage_dim = str(self.r_BC) + ' = ' + str(self.r_BC_value) + ';\n' + \
                      str(self.r_BO4) + ' = ' + str(self.r_BO4_value) + ';\n' + \
                      str(self.r_CO2) + ' = ' + str(self.r_CO2_value) + ';\n' + \
                      str(self.orient_R_O4O2) + ' = ' + str(
            self.orient_R_O4O2_value) + ';\n' + \
                      str(self.orient_R_CO2) + ' = ' + str(
            self.orient_R_CO2_value) + '.'
        return class_name + linkage_dim


class O4DriveA(JawOnYork):
    def __init__(self):
        JawOnYork.__init__(self)
        self.r = Function("r")(x)
        self.v = Function("v")(x)

    def __str__(self):
        about_theta = "theta = f(r_O4O2) = \n" + "\t" + \
                      latex(self.get_theta_of_r_O4O2_expr())
        return about_theta

    def get_theta_of_r_O4O2_expr(self):
        """
        j2 = O4DriveA()
        theta_expr = j2.get_theta_of_r_O4O2_expr()
        print(theta_expr)
        theta_min = (theta_expr.subs(j2.r_O4O2, 52.05) + 2*pi).evalf()
        print("theta_min(in degree): ", (theta_min/pi*180).evalf())
        # theta_min(in degree):  200.000347647433
        """
        theta_of_r_O4O2_expr = solve(
            self.get_equation_of_r_O4O2_and_theta(), self.theta
        )[1]
        # theta_of_r_O4O2_expr_simple = theta_of_r_O4O2_expr.subs([
        #     (self.r_BC, self.r_BC_value),
        #     (self.r_BO4, self.r_BO4_value),
        #     (self.r_CO2, self.r_CO2_value)])
        return theta_of_r_O4O2_expr

    def get_x_R_AO2_of_theta_expr(self):
        """
        j2 = O4DriveA()
        R_AO2_x = j2.get_x_R_AO2_of_theta_expr()
        print(R_AO2_x)
        """
        x_R_AO2_of_theta_expr = solve(self.get_equation_of_x_R_AO2_and_theta(),
                                      self.x_R_AO2)[0]
        return x_R_AO2_of_theta_expr

    def get_x_R_AO2_of_r_O4O2_expr(self):
        """
        j2 = O4DriveA()
        R_AO2_x = j2.get_x_R_AO2_of_r_O4O2_expr()
        print(j2.get_x_R_AO2_of_theta_expr())
        print(j2.get_theta_of_r_O4O2_expr())
        print(j2.theta)
        print(R_AO2_x)
        print(j2.get_x_R_AO2_of_theta_expr().subs([(j2.theta, j2.get_theta_of_r_O4O2_expr())]))
        # 175.044318959514*cos(2.0*atan((200.0*r_O4O2 + sqrt(-r_O4O2**4 + 60850.0*r_O4O2**2 + 35319375.0))/(r_O4O2**2 + 1575.0)) + 2.26972648191758) - 60.0
        print(j2.get_x_R_AO2_of_r_O4O2_expr().subs([(j2.r_O4O2, 52.05)]).evalf())
        # -0.751106183852862
        """
        x_R_AO2_of_r_O4O2_expr = self.get_x_R_AO2_of_theta_expr().subs(
            [(self.theta, self.get_theta_of_r_O4O2_expr())])
        return x_R_AO2_of_r_O4O2_expr

    def get_y_R_AO2_of_theta_expr(self):
        """
        j2 = O4DriveA()
        R_AO2_y = j2.get_y_R_AO2_of_theta_expr()
        print(R_AO2_y)
        print(R_AO2_y.subs(j2.theta, 3.49065850398866).evalf())
        """
        y_R_AO2_of_theta_expr = solve(self.get_equation_of_y_R_AO2_and_theta(),
                                      self.y_R_AO2)[0]
        return y_R_AO2_of_theta_expr

    def get_y_R_AO2_of_r_O4O2_expr(self):
        """
        j2 = O4DriveA()
        R_AO2_y = j2.get_y_R_AO2_of_r_O4O2_expr()
        print(j2.get_y_R_AO2_of_r_O4O2_expr().subs([(j2.r_O4O2, 93.1457274726962)]).evalf())
        # 171.354752195555
        print(j2.get_y_R_AO2_of_r_O4O2_expr().subs([(j2.r_O4O2, 183)]).evalf())
        # 169.165720344467
        print(j2.get_y_R_AO2_of_r_O4O2_expr().subs([(j2.r_O4O2, 52.0476394259645)]).evalf())
        ## 164.432656720374
        # 164.440000000000
        """
        y_R_AO2_of_r_O4O2_expr = self.get_y_R_AO2_of_theta_expr().subs(
            [(self.theta, self.get_theta_of_r_O4O2_expr())])
        return y_R_AO2_of_r_O4O2_expr

    def get_x_V_AO2_of_vr_O4O2(self):
        """
        j2 = O4DriveA()
        x_V_AO2_when_touch = j2.get_x_V_AO2_of_vr_O4O2().subs([(j2.v, -966.6038206895039), (j2.r, 93.14763942596754)]).evalf()
        print(round(x_V_AO2_when_touch, 4))
        # 686.7686
        print(j2.get_x_V_AO2_of_vr_O4O2())
        """
        x_V_AO2 = self.get_x_R_AO2_of_r_O4O2_expr().subs(
            [(self.r_O4O2, self.r)]).diff(x)
        x_V_AO2_of_v_r = x_V_AO2.subs(Derivative(self.r, x), self.v)
        return x_V_AO2_of_v_r

    def get_y_V_AO2_of_vr_O4O2(self):
        """
        j2 = O4DriveA()
        y_V_AO2_when_touch = j2.get_y_V_AO2_of_vr_O4O2().subs([(j2.v, -800), (j2.r, 100.33)]).evalf()
        print(round(y_V_AO2_when_touch,2))  # TODO: why negative sence?
        # -105.16
        """
        y_V_AO2 = self.get_y_R_AO2_of_r_O4O2_expr().subs(
            self.r_O4O2, self.r).diff(x)
        y_V_AO2_of_v_r = y_V_AO2.subs(Derivative(self.r, x), self.v)
        return y_V_AO2_of_v_r


class ANeedO4(JawOnYork):
    def __init__(self):
        """
        j3 = ANeedO4()
        print(j3)
        print(j3.theta)
        """
        JawOnYork.__init__(self)
        self.theta = Function("theta")(x)
        self.omega = Function("omega")(x)
        self.x_R_AO2 = Function("x_R_AO2")(x)
        self.y_R_AO2 = Function("y_R_AO2")(x)
        self.x_V_AO2 = Function("x_V_AO2")(x)
        self.y_V_AO2 = Function("y_V_AO2")(x)

    def get_r_O4O2_of_theta_expr(self):
        """
        j3 = ANeedO4()
        r_O4O2_min = j3.get_r_O4O2_of_theta_expr().subs(j3.theta, 200/180*pi).evalf()
        print(r_O4O2_min)
        # 52.0476394259675
        print(latex(j3.get_r_O4O2_of_theta_expr()))
        # 5.0 \sqrt{961.0 - 16.0 \left(5.0 \cos{\left(\theta{\left(x \right)} \right)} - 3.0\right)^{2}} - 100.0 \sin{\left(\theta{\left(x \right)} \right)}
        print(j3.get_r_O4O2_of_theta_expr())
        """
        r_O4O2_of_theta_expr = solve(
            self.get_equation_of_r_O4O2_and_theta(), self.r_O4O2
        )
        return r_O4O2_of_theta_expr[0]

    def get_v_O4O2_of_theta_omega_expr(self):
        """
        j3 = ANeedO4()
        print(j3.get_v_O4O2_of_theta_omega())
        """
        v_O4O2_of_theta = self.get_r_O4O2_of_theta_expr().diff(x)
        v_O4O2_of_theta_omega = v_O4O2_of_theta.subs(
            Derivative(self.theta, x), self.omega
        )
        return v_O4O2_of_theta_omega

    def get_theta_of_x_R_AO2_expr(self):
        """
        j3 = ANeedO4()
        print(j3.get_theta_of_x_R_AO2_expr())
        print(j3.get_theta_of_x_R_AO2_expr()[1].subs(j3.x_R_AO2, 0).evalf())
        # 3.49065850398866
        print(j3.get_theta_of_x_R_AO2_expr()[0].subs(j3.x_R_AO2, 0).evalf())
        # 7.33197976702609
        """
        theta_of_x_R_AO2_expr = \
            solve(self.get_equation_of_x_R_AO2_and_theta(), self.theta)
        return theta_of_x_R_AO2_expr[1]

    def get_theta_of_y_R_AO2_expr(self):
        """
        j3 = ANeedO4()
        print(j3.get_theta_of_y_R_AO2_expr())
        print(j3.get_theta_of_y_R_AO2_expr().subs(j3.y_R_AO2, 164.44).evalf())
        # 3.49065850398865
        """
        theta_of_y_R_AO2_expr = \
            solve(self.get_equation_of_y_R_AO2_and_theta(), self.theta)
        return theta_of_y_R_AO2_expr[1]

    def get_r_O4O2_of_x_R_AO2_expr(self):
        """
        j3 = ANeedO4()
        print(j3.get_r_O4O2_of_x_R_AO2_expr())
        print(j3.get_r_O4O2_of_x_R_AO2_expr().subs(j3.x_R_AO2, 0))
        # 52.0476394259659
        print(j3.get_r_O4O2_of_x_R_AO2_expr().subs(j3.x_R_AO2, -100))
        # 178.451666336814
        178.451666336814-52.0476394259659
        # 126.40402691084809
        print(j3.get_r_O4O2_of_x_R_AO2_expr().subs(j3.x_R_AO2, -24.25))
        # 93.1457274726962
        93.1457274726962-52.0476394259659
        # 41.0980880467303
        """
        r_O4O2_of_x_R_AO2_expr = self.get_r_O4O2_of_theta_expr().subs(
            self.theta, self.get_theta_of_x_R_AO2_expr()
        )
        return r_O4O2_of_x_R_AO2_expr

    def get_r_O4O2_of_y_R_AO2_expr(self):
        """
        j3 = ANeedO4()
        print(j3.get_r_O4O2_of_y_R_AO2_expr())
        print(j3.get_r_O4O2_of_y_R_AO2_expr().subs(j3.y_R_AO2, 164.44))
        # 52.0476394259645
        """
        r_O4O2_of_y_R_AO2_expr = self.get_r_O4O2_of_theta_expr().subs(
            self.theta, self.get_theta_of_y_R_AO2_expr()
        )
        return r_O4O2_of_y_R_AO2_expr

    def get_v_O4O2_of_x_V_AO2_expr(self):
        """
        j3 = ANeedO4()
        print(j3.get_v_O4O2_of_x_V_AO2_expr())
        print(latex(j3.get_v_O4O2_of_x_V_AO2_expr()))
        print(j3.get_v_O4O2_of_x_V_AO2_expr().subs([(j3.x_R_AO2, -29.47),(j3.x_V_AO2, 593.71)]))
        # -800.000005067435
        """
        v_O4O2_of_x_R_AO2_expr = self.get_r_O4O2_of_x_R_AO2_expr().diff(x)
        v_O4O2_of_x_RV_AO2_expr = v_O4O2_of_x_R_AO2_expr.subs(
            Derivative(self.x_R_AO2, x), self.x_V_AO2
        )
        return v_O4O2_of_x_RV_AO2_expr

    def get_v_O4O2_of_y_V_AO2_expr(self):
        """
        j3 = ANeedO4()
        print(j3.get_v_O4O2_of_y_V_AO2_expr())
        print(latex(j3.get_v_O4O2_of_y_V_AO2_expr()))
        print(j3.get_v_O4O2_of_y_V_AO2_expr().subs([(j3.y_R_AO2, 172.36),(j3.y_V_AO2, -105.16)]))
        print(j3.get_v_O4O2_of_y_V_AO2_expr().subs([(j3.y_R_AO2, 172.36),(j3.y_V_AO2, -535)]))
        # -799.822346652580
        """
        v_O4O2_of_y_R_AO2_expr = self.get_r_O4O2_of_y_R_AO2_expr().diff(x)
        v_O4O2_of_y_RV_AO2_expr = v_O4O2_of_y_R_AO2_expr.subs(
            Derivative(self.y_R_AO2, x), self.y_V_AO2
        )
        return v_O4O2_of_y_RV_AO2_expr


if __name__ == '__main__':
    pass

from tetracamthon.mechanism import Forward, LinkDim, LinksWithDim, \
    SlideRocker, Forward
from sympy import pi, symbols, latex


def test_read_in_csv_data():
    link_dim = LinkDim(path_to_csv="/Users/johnqu/PycharmProjects/Tetracamthon"
                                   "/src/tetracamthon/"
                                   "tetracamthon_lind_dimensions.csv")
    assert link_dim.spec_id[0] == 1
    assert link_dim.r_BO4[0] == 155
    assert link_dim.r_BC[0] == 100
    assert link_dim.r_CO2[0] == 60
    assert link_dim.r_DC[0] == 164.44
    assert link_dim.r_AD[0] == 59.25
    assert abs(link_dim.o_O4O2[0] - 4.71238898038469) < 0.001
    assert abs(link_dim.o_CO2[0] - 3.14159265358979) < 0.001


def test_links_with_dim():
    l_w_d = LinksWithDim(a_spec_id=1,
                         path_to_csv="/Users/johnqu/PycharmProjects/"
                                     "Tetracamthon/src/tetracamthon/"
                                     "tetracamthon_lind_dimensions.csv")
    assert l_w_d.lBO4.r.val == 155
    assert l_w_d.lBO4.r.sym == symbols("r_BO4")
    assert l_w_d.lBO4.o.sym == symbols("alpha")
    assert l_w_d.lBO4.o.val is None
    assert l_w_d.lBC.r.val == 100
    assert l_w_d.lBC.o.sym == symbols("theta")
    assert l_w_d.lCO2.r.val == 60
    assert abs(l_w_d.lCO2.o.val - 3.14159265358979) < 0.001
    assert l_w_d.lDC.r.val == 164.44
    assert l_w_d.lAD.r.val == 59.25
    assert abs(l_w_d.lAC.r.val - 174.788661245517) < 0.001
    assert abs(l_w_d.lO4O2.o.val - 4.71238898038469) < 0.001
    assert abs(l_w_d.ang_ACD_val - 0.345833343399567) < 0.001
    assert abs(l_w_d.ang_DCB_val - 1.91986217719376) < 0.001


def test_get_theta_of_r_o4o2_expr():
    sr = SlideRocker(name="Basis",
                     a_spec_id=1,
                     path_to_csv="/Users/johnqu/PycharmProjects/Tetracamthon/"
                                 "src/tetracamthon/"
                                 "tetracamthon_lind_dimensions.csv")
    result = sr.get_equation_of_r_O4O2_and_o_BC()
    print("Type of result is " + str(type(result)))
    print("Here it is: " + str(result))
    assert "r_O4O2" in str(result)
    assert "theta" in str(result)


def test_get_o_bc_of_r_o4o2(a_slide_rocker_of_compact_flex):
    sr = a_slide_rocker_of_compact_flex
    result = sr.get_o_BC_of_r_O4O2()
    print("Type of result is " + str(type(result)))
    print("Here it is: " + str(result))
    assert "r_O4O2" in str(result)
    assert "theta" not in str(result)
    theta_min = (result.subs(sr.lO4O2.r.sym, 52.05) + 2 * pi).evalf()
    assert abs((theta_min / pi * 180).evalf() - 200) < 0.001


def test_get_x_a02_of_o_bc(a_forward_slide_rocker_of_compact_flex):
    fw = a_forward_slide_rocker_of_compact_flex
    result = fw.get_x_AO2_of_o_BC()
    print("Type of result is " + str(type(result)))
    print("Here it is: " + str(result))
    assert "x_AO2" not in str(result)
    assert "theta" in str(result)


def test_get_x_ao2_of_r_o4o2(a_forward_slide_rocker_of_compact_flex):
    fw = a_forward_slide_rocker_of_compact_flex
    result = fw.get_x_AO2_of_r_O4O2()
    print("Type of result is " + str(type(result)))
    print("Here it is: " + str(result))
    assert "x_AO2" not in str(result)
    assert "r_O4O2" in str(result)


def test_get_y_ao2_of_r_o4o2(a_forward_slide_rocker_of_compact_flex):
    fw = a_forward_slide_rocker_of_compact_flex
    result = fw.get_y_AO2_of_r_O4O2()
    print("Type of result is " + str(type(result)))
    print("Here it is: " + str(result))
    assert "y_AO2" not in str(result)
    assert "r_O4O2" in str(result)


def test_get_vx_ao2_of_vr_o4o2(a_forward_slide_rocker_of_compact_flex):
    fw = a_forward_slide_rocker_of_compact_flex
    result = fw.get_vx_AO2_of_vr_O4O2()
    print("Type of result is " + str(type(result)))
    print("Here it is: " + str(result))
    vx_AO2_when_touch = result.subs(
        [(fw.v, -966.6038206895039), (fw.r, 93.14763942596754)]).evalf()
    assert abs(vx_AO2_when_touch - 686.336667905566) < 0.1
    assert "r(t)" in str(result)
    assert "v(t)" in str(result)


def test_get_vy_ao2_of_vr_o4o2(a_forward_slide_rocker_of_compact_flex):
    fw = a_forward_slide_rocker_of_compact_flex
    result = fw.get_vy_AO2_of_vr_O4O2()
    print("Type of result is " + str(type(result)))
    print("Here it is: " + str(result))
    vy_AO2_when_touch = result.subs(
        [(fw.v, -800), (fw.r, 100.33)]).evalf()
    assert abs(vy_AO2_when_touch - (-102.62)) < 0.1
    assert "r(t)" in str(result)
    assert "v(t)" in str(result)


def test_get_r_o4o2_of_o_bc(a_backward_slide_rocker_of_compact_flex):
    bw = a_backward_slide_rocker_of_compact_flex
    result = bw.get_r_O4O2_of_o_BC()
    print("Type of result is " + str(type(result)))
    print("Here is its LaTex form: " + latex(str(result)))
    bw.lBC.o.val = (200 / 180 * pi).evalf()
    print("The minimal rad of lBC is ", bw.lBC.o.val)
    r_O4O2_min = result.subs(bw.lBC.o.sym, bw.lBC.o.val).evalf()
    print("The minimal distance between O4 and O2 is ", r_O4O2_min)
    assert abs(r_O4O2_min - 52.047639) < 0.001
    assert "theta" in str(result)
    assert "r_O4O2" not in str(result)


def test_get_o_bc_of_x_ao2(a_backward_slide_rocker_of_compact_flex):
    bw = a_backward_slide_rocker_of_compact_flex
    result = bw.get_o_BC_of_x_AO2()
    print("Type of result is " + str(type(result)))
    print("Here is its LaTex form: " + latex(str(result)))
    x_AO2_close = -0.75
    o_bc_min = result.subs(bw.lAO2.x.sym, x_AO2_close).evalf()
    o_bc_min_in_deg = (o_bc_min / pi * 180).evalf()
    print("The minimal deg of lBC is ", o_bc_min_in_deg)
    o_bc_min_in_deg_expected = 200
    assert abs(o_bc_min_in_deg - o_bc_min_in_deg_expected) < 1


def test_get_o_bc_of_y_ao2(a_backward_slide_rocker_of_compact_flex):
    bw = a_backward_slide_rocker_of_compact_flex
    result = bw.get_o_BC_of_y_AO2()
    print("Type of result is " + str(type(result)))
    print("Here is its LaTex form: " + latex(str(result)))
    o_bc_min = result.subs(bw.lAO2.y.sym, 164.44).evalf()
    o_bc_min_in_deg = (o_bc_min / pi * 180).evalf()
    print("The minimal deg of lBC is ", o_bc_min_in_deg)
    o_bc_min_in_deg_expected = 200
    assert abs(o_bc_min_in_deg - o_bc_min_in_deg_expected) < 1


def test_get_r_o4o2_of_x_ao2(a_backward_slide_rocker_of_compact_flex):
    bw = a_backward_slide_rocker_of_compact_flex
    result = bw.get_r_O4O2_of_x_AO2()
    print("Type of result is " + str(type(result)))
    print("Here is its LaTex form: " + latex(str(result)))
    x_AO2_close = -0.75
    r_O4O2_min = result.subs(bw.lAO2.x.sym, x_AO2_close).evalf()
    print("The minimal distance between O4 and O2 is ", r_O4O2_min)
    x_AO2_open = -24.25
    r_O4O2_max = result.subs(bw.lAO2.x.sym, x_AO2_open).evalf()
    print("The maximal distance between O4 and O2 is ", r_O4O2_max)
    r_O4O2_stroke = r_O4O2_max - r_O4O2_min
    print("The stroke distance between O4 and O2 is ", r_O4O2_stroke)
    r_O4O2_min_expected = 52
    assert abs(r_O4O2_min - r_O4O2_min_expected) < 1
    r_O4O2_max_expected = 93
    assert abs(r_O4O2_max - r_O4O2_max_expected) < 1
    r_O4O2_stroke_expected = 42.5
    assert abs(r_O4O2_stroke - r_O4O2_stroke_expected) < 5




from tetracamthon.mechanism import Forward, LinkDimension, LinksWithDim, \
    SlideRocker, Forward
from sympy import pi, symbols, latex
from sympy.abc import t
from tetracamthon.helper import trans_time_to_degree, trans_degree_to_time
from pathlib import Path


def test_read_in_csv_data():
    link_dim = LinkDimension(
        path_to_link_dim_csv=str(
            Path(__file__).resolve().parents[1] / "src" / "tetracamthon" /
            "tetracamthon_lind_dimensions.csv"
        ))
    assert link_dim.spec_id[0] == 'compact_flex'
    assert link_dim.r_BO4[0] == 155
    assert link_dim.r_BC[0] == 100
    assert link_dim.r_CO2[0] == 60
    assert link_dim.r_DC[0] == 164.44
    assert link_dim.r_AD[0] == 59.25
    assert abs(link_dim.o_O4O2[0] - 4.71238898038469) < 0.001
    assert abs(link_dim.o_CO2[0] - 3.14159265358979) < 0.001


def test_links_with_dim():
    l_w_d = LinksWithDim(a_spec_id='compact_flex',
                         path_to_link_dim_csv=str(
                             Path(__file__).resolve().parents[1] / "src" /
                             "tetracamthon" / "tetracamthon_lind_dimensions.csv"
                         ))
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
                     a_spec_id='compact_flex',
                     path_to_link_dim_csv=str(
                         Path(__file__).resolve().parents[1] / "src" /
                         "tetracamthon" / "tetracamthon_lind_dimensions.csv"
                     ))
    result = sr.get_equation_of_r_O4O2_and_o_BC()
    print("Type of result is " + str(type(result)))
    print("Here it is: " + str(result))
    assert "r_O4O2" in str(result)
    assert "theta" in str(result)


def test_get_o_bc_of_r_o4o2(a_forward_slide_rocker_of_compact_flex):
    sr = a_forward_slide_rocker_of_compact_flex
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


def test_get_r_O4O2_when_closed(
        a_tracing_of_point_a_with_1000sq_dim
):
    sel = a_tracing_of_point_a_with_1000sq_dim
    result = sel.get_r_O4O2_when_closed()
    print('r_O4O2_when_closed: ', result)
    assert abs(result - 52.0476394259659) < 0.001


def test_get_r_O4O2_when_touched(
        a_tracing_of_point_a_with_1000sq_dim
):
    sel = a_tracing_of_point_a_with_1000sq_dim
    result = sel.get_r_O4O2_when_touched()
    print(result)
    assert abs(result - 102.988204030727) < 0.001


def test_get_t_touched(
        a_tracing_of_point_a_with_1000sq_dim
):
    sel = a_tracing_of_point_a_with_1000sq_dim
    result = sel.get_t_touched()
    print('\n The degree when touched: ', trans_time_to_degree(result))
    # The degree when touched:  81.1097320417263
    # The degree when touched:  90.5571576293787 2020-09-14 20:38:32
    assert abs(
        sel.joy_spline.get_pvajp_at_point(result)[0] - (-50.94)
    ) < 0.01


def test_get_y_ao2_of_t_while_touching(
        a_tracing_of_point_a_with_1000sq_dim
):
    sel = a_tracing_of_point_a_with_1000sq_dim
    t_when_closed = trans_degree_to_time(137.5)
    y_AO2_of_t_when_closed = sel.get_y_AO2_of_t_while_clamping()[1].subs(
        t, t_when_closed
    )
    print('\n y_AO2_of_t_when_closed: ', y_AO2_of_t_when_closed)
    assert abs(y_AO2_of_t_when_closed - 182.31) < 0.01
    # y_AO2_of_t_when_closed: 182.309999999999
    t_when_touched = sel.get_t_touched()
    y_AO2_of_t_when_touched = sel.get_y_AO2_of_t_while_clamping()[0].subs(
        t, t_when_touched
    )
    print("y_AO2_of_t_when_touched: ", y_AO2_of_t_when_touched)
    assert abs(y_AO2_of_t_when_touched - 190.124297763331) < 0.01


def test_get_x_ao2_of_t_while_touching(
        a_tracing_of_point_a_with_1000sq_dim
):
    sel = a_tracing_of_point_a_with_1000sq_dim
    t_when_closed = trans_degree_to_time(137.5)
    x_AO2_of_t_when_closed = sel.get_x_AO2_of_t_while_clamping()[1].subs(
        t, t_when_closed
    )
    print("\n x_AO2_of_t_when_closed: ", x_AO2_of_t_when_closed)
    assert abs(x_AO2_of_t_when_closed - (- 1.5 / 2)) < 0.01
    t_when_touched = sel.get_t_touched()
    x_AO2_of_t_when_touched = sel.get_x_AO2_of_t_while_clamping()[0].subs(
        t, t_when_touched
    )
    print("x_AO2_of_t_when_touched: ", x_AO2_of_t_when_touched)
    assert abs(x_AO2_of_t_when_touched - (- 35.5)) < 0.01


def test_get_y_ao5_of_t_while_touching(
        a_tracing_of_point_a_with_1000sq_dim
):
    sel = a_tracing_of_point_a_with_1000sq_dim
    result = sel.get_y_AO5_of_t_while_clamping()
    t_when_touched = sel.get_t_touched()
    y_AO5_when_touched = result[0].subs(
        t, t_when_touched
    )
    print("\ny_AO5_when_touched: ", y_AO5_when_touched)
    assert abs(y_AO5_when_touched - 34.7643855116123) < 1
    t_when_closed = trans_degree_to_time(137.5)
    y_AO5_when_closed = result[1].subs(
        t, t_when_closed
    )
    print("y_AO5_when_closed: ", y_AO5_when_closed)
    assert abs(y_AO5_when_closed - sel.package.top_gap) < 0.01


def test_get_vx_ao5_while_touching(
        a_tracing_of_point_a_with_1000sq_dim
):
    sel = a_tracing_of_point_a_with_1000sq_dim
    result = sel.get_vx_AO5_of_t_while_clamping()
    t_when_touched = sel.get_t_touched()
    vx_AO5_when_touched = result[0].subs(
        t, t_when_touched
    )
    print("\nvx_AO5_when_touched: ", vx_AO5_when_touched)
    assert abs(vx_AO5_when_touched - 763.556027717147) < 1
    t_when_closed = trans_degree_to_time(137.5)
    vx_AO5_when_closed = result[1].subs(
        t, t_when_closed
    )
    print("vx_AO5_when_closed: ", vx_AO5_when_closed)
    assert abs(vx_AO5_when_closed) < 1


def test_get_vx_ao2_of_t_while_touching(
        a_tracing_of_point_a_with_1000sq_dim
):
    sel = a_tracing_of_point_a_with_1000sq_dim
    result = sel.get_vx_AO2_of_t_while_clamping()
    t_when_touched = sel.get_t_touched()
    vx_AO2_when_touched = result[0].subs(
        t, t_when_touched
    )
    print("\nvx_AO2_when_touched: ", vx_AO2_when_touched)
    assert abs(vx_AO2_when_touched - 763.556027717147) < 1
    t_when_closed = trans_degree_to_time(137.5)
    vx_AO2_when_closed = result[1].subs(
        t, t_when_closed
    )
    print("vx_AO2_when_closed: ", vx_AO2_when_closed)
    assert abs(vx_AO2_when_closed) < 1


def test_get_vy_ao2_of_t_while_touching(
        a_tracing_of_point_a_with_1000sq_dim
):
    sel = a_tracing_of_point_a_with_1000sq_dim
    result = sel.get_vy_AO2_of_t_while_clamping()
    t_when_touched = sel.get_t_touched()
    vy_AO2_when_touched = result[0].subs(
        t, t_when_touched
    )
    print("\nvy_AO2_when_touched: ", vy_AO2_when_touched)
    assert abs(vy_AO2_when_touched - (-98.3941710720057)) < 1
    t_when_closed = trans_degree_to_time(137.5)
    vy_AO2_when_closed = result[1].subs(
        t, t_when_closed
    )
    print("vy_AO2_when_closed: ", vy_AO2_when_closed)
    assert abs(vy_AO2_when_closed) < 1


def test_ploy_symbolically(
        a_tracing_of_point_a_with_1000sq_dim
):
    a_tracing_of_point_a_with_1000sq_dim.ploy_symbolically(show=False)

def test_init_with_co_sym(a_polynomial):
    print(a_polynomial.init_with_co_sym())
    assert 'C_00' in str(a_polynomial.expr_with_co_sym[0])
    assert 'C_05' in str(a_polynomial.expr_with_co_sym[0])
    assert '(t - 1)' in str(a_polynomial.expr_with_co_sym[0])


def test_diffs(a_polynomial):
    for i in range(1, a_polynomial.max_order):
        print("\n",
              a_polynomial.diffs(a_polynomial.expr_with_co_sym[0])[i - 1])
    assert 'C_00' not in str(a_polynomial.expr_with_co_sym[1])
    assert 'C_01' in str(a_polynomial.expr_with_co_sym[1])
    assert 'C_04' not in str(a_polynomial.expr_with_co_sym[5])
    assert 'C_05' in str(a_polynomial.expr_with_co_sym[5])


def test_get_expr_with_co_sym(a_polynomial):
    expressions_with_sym = a_polynomial.get_expr_with_co_sym()
    print(a_polynomial.expr_with_co_sym[0])
    print(a_polynomial.expr_with_co_sym[5])
    assert len(expressions_with_sym) == 6


def test_update_expr_and_diffs_with_co_val(a_polynomial, a_solution):
    expressions_with_val = a_polynomial.update_expr_and_diffs_with_co_val(
        a_solution
    )
    print(a_polynomial.expr_with_co_val[0])
    print(a_polynomial.expr_with_co_val[5])
    assert len(expressions_with_val) == 6


def test_get_expr_with_co_val(a_polynomial, a_solution):
    a_polynomial.update_expr_and_diffs_with_co_val(a_solution)
    expressions_with_val = a_polynomial.get_expr_with_co_val()
    print(a_polynomial.expr_with_co_val[0])
    print(a_polynomial.expr_with_co_val[5])
    assert len(expressions_with_val) == 6


def test_read_in_csv_data(a_sample_knots_in_spline):
    print(a_sample_knots_in_spline.knots_with_info[0])
    print(a_sample_knots_in_spline.knots_with_info[1])
    print(a_sample_knots_in_spline.knots_with_info[2])
    print(a_sample_knots_in_spline.knots_with_info[3])
    assert True


def test_build_polynomials(a_sample_spline):
    a_sample_spline.build_polynomials()
    print(a_sample_spline.pieces_of_polynomial[0])
    print(a_sample_spline.pieces_of_polynomial[1])
    print(a_sample_spline.pieces_of_polynomial[2])
    assert True


def test_get_pieces_of_polynomial(a_sample_spline):
    a_sample_spline.build_polynomials()
    print(a_sample_spline.get_pieces_of_polynomial()[0])
    print(a_sample_spline.get_pieces_of_polynomial()[1])
    print(a_sample_spline.get_pieces_of_polynomial()[2])
    assert True


def test_collect_variables(a_sample_spline):
    a_sample_spline.get_pieces_of_polynomial()
    variables = a_sample_spline.collect_variables()
    for v in variables:
        print(v)
    assert True


def test_get_variables(a_sample_spline):
    a_sample_spline.get_pieces_of_polynomial()
    variables = a_sample_spline.get_variables()
    for v in variables:
        print(v)
    assert True


def test_construct_interpolating_condition_equations(a_sample_spline):
    a_sample_spline.get_pieces_of_polynomial()
    interpolating_equations = \
        a_sample_spline.construct_interpolating_condition_equations()
    for eq in interpolating_equations:
        print(eq)
    assert True


def test_construct_smoothness_condition_equations(a_sample_spline):
    a_sample_spline.get_pieces_of_polynomial()
    smoothness_condition_equations = \
        a_sample_spline.construct_smoothness_condition_equations()
    for eq in smoothness_condition_equations:
        print(eq)
    assert True


def test_construct_periodic_condition_equations(a_sample_spline):
    a_sample_spline.get_pieces_of_polynomial()
    periodic_condition_equations = \
        a_sample_spline.construct_periodic_condition_equations()
    for eq in periodic_condition_equations:
        print(eq)
    assert True


def test_construct_equations(a_sample_spline):
    a_sample_spline.construct_equations()
    assert True


def test_solve_to_solution(a_sample_spline):
    a_solution = a_sample_spline.solve_to_solution()
    print(a_solution)
    assert True


def test_solve_spline_pieces(a_sample_spline):
    for a_polynomial in a_sample_spline.solve_spline_pieces():
        print(a_polynomial)
    assert True


def test_load_solution(a_sample_spline_reloaded):
    print(a_sample_spline_reloaded.solution)
    assert True


def test_load_variables(a_sample_spline_reloaded):
    print(a_sample_spline_reloaded.variables)
    assert True


def test_load_conditional_equations(a_sample_spline_reloaded):
    print("Interpolating condition equations: ")
    for eq in a_sample_spline_reloaded.interpolating_equations:
        print(eq)
    print("Smoothness condition equations: ")
    for eq in a_sample_spline_reloaded.smoothness_equations:
        print(eq)
    print("Periodic condition equations: ")
    for eq in a_sample_spline_reloaded.periodic_equations:
        print(eq)
    assert True


def test_load_solved_pieces_of_polynomial(a_sample_spline_reloaded):
    for piece in a_sample_spline_reloaded.pieces_of_polynomial:
        print(piece)
    assert True


def test_find_index_of_piece_of_point(a_sample_spline_reloaded):
    index_a = a_sample_spline_reloaded.get_index_of_piece_of_point(0)
    assert index_a == 0
    index_b = a_sample_spline_reloaded.get_index_of_piece_of_point(1.2)
    assert index_b == 1
    index_c = a_sample_spline_reloaded.get_index_of_piece_of_point(1)
    assert index_c == 1
    index_d = a_sample_spline_reloaded.get_index_of_piece_of_point(2.2)
    assert index_d == 2
    index_e = a_sample_spline_reloaded.get_index_of_piece_of_point(3)
    assert index_e == 2


def test_get_pvajp_at_point(a_sample_spline_reloaded):
    result_a = a_sample_spline_reloaded.get_pvajp_at_point(1)
    assert len(result_a) == 5
    assert abs(result_a[0] - 0.3) < 0.001
    result_b = a_sample_spline_reloaded.get_pvajp_at_point(1.2)
    result_c = a_sample_spline_reloaded.get_pvajp_at_point(0)
    assert abs(result_c[0]) < 0.001
    assert abs(result_c[1]) < 0.001
    assert abs(result_c[2]) < 0.001
    result_d = a_sample_spline_reloaded.get_pvajp_at_point(3)
    assert abs(result_d[0] - 1) < 0.001
    assert abs(result_d[1]) < 0.001
    assert abs(result_d[2]) < 0.001


def test_prepare_plots_for_plt(a_sample_spline_reloaded):
    a_sample_spline_reloaded.plot_spline_on_subplots(
        whether_save_png=False,
        whether_show_figure=True,
        whether_knots_ticks=True,
        whether_annotate=True,
    )
    assert True


def test_calculate_peak_points(a_sample_spline):
    result = a_sample_spline.calculate_peak_points()
    print(result)
    assert True


def test_change_boundary_knot_info():

    assert False

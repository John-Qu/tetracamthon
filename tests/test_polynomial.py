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


def test_build_polynomials(a_spline):
    a_spline.build_polynomials()
    print(a_spline.pieces_of_polynomial[0])
    print(a_spline.pieces_of_polynomial[1])
    print(a_spline.pieces_of_polynomial[2])
    assert True


def test_get_pieces_of_polynomial(a_spline):
    a_spline.build_polynomials()
    print(a_spline.get_pieces_of_polynomial()[0])
    print(a_spline.get_pieces_of_polynomial()[1])
    print(a_spline.get_pieces_of_polynomial()[2])
    assert True


def test_collect_variables(a_spline):
    a_spline.get_pieces_of_polynomial()
    variables = a_spline.collect_variables()
    for v in variables:
        print(v)
    assert True


def test_get_variables(a_spline):
    a_spline.get_pieces_of_polynomial()
    variables = a_spline.get_variables()
    for v in variables:
        print(v)
    assert True


def test_construct_interpolating_condition_equations(a_spline):
    a_spline.get_pieces_of_polynomial()
    interpolating_equations = \
        a_spline.construct_interpolating_condition_equations()
    for eq in interpolating_equations:
        print(eq)
    assert True

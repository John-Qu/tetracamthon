def test_get_tube_diameter(a_1000sq_package):
    result = a_1000sq_package.get_tube_diameter()
    assert abs(result - 91) < 1


def test_get_average_velocity(
    a_production_of_330sq_8000pph
):
    sel = a_production_of_330sq_8000pph
    result = sel.get_average_velocity()
    print("\naverage_velocity: ", result)
    assert abs(result - (-422.22)) < 1


def test_get_time_of_main_pulling(
    a_production_of_330sq_8000pph
):
    sel = a_production_of_330sq_8000pph
    result = sel.get_time_of_main_pulling()
    print('\ntime_of_main_pulling: ', result)
    assert abs(result - 0.175) < 0.01


def test_get_less_pulled_length_in_shaking_with_holding(
        a_production_of_330sq_8000pph
):
    sel = a_production_of_330sq_8000pph
    result = sel.get_less_pulled_length_in_shaking_with_holding()
    print('\nless_pulled_length_in_shaking_with_holding: ', result)
    assert abs(result - 24.25) < 1


def test_get_less_pulled_length_in_shaking_with_folding(
        a_production_of_330sq_8000pph
):
    sel = a_production_of_330sq_8000pph
    result = sel.get_less_pulled_length_in_shaking_with_folding()
    print('\nless_pulled_length_in_shaking_with_folding: ', result)
    assert abs(result - 16.975) < 1


# def test_get_main_pulling_velocity(a_production_of_1000sq_8000pph):
#     result = a_production_of_1000sq_8000pph.get_main_pulling_velocity()
def test_get_main_pulling_velocity(a_production_of_330sq_8000pph):
    result = a_production_of_330sq_8000pph.get_main_pulling_velocity()
    print("\nmain_pulling_velocity for a_production_of_330sq_8000pph: ",
          result)
    assert abs(result - (-657)) < 1



def test_get_tube_diameter(a_1000sq_package):
    result = a_1000sq_package.get_tube_diameter()
    assert abs(result - 91) < 1


# def test_get_main_pulling_velocity(a_production_of_1000sq_8000pph):
#     result = a_production_of_1000sq_8000pph.get_main_pulling_velocity()
def test_get_main_pulling_velocity(a_production_of_330sq_8000pph):
    result = a_production_of_330sq_8000pph.get_main_pulling_velocity()
    print("main_pulling_velocity for a_production_of_330sq_8000pph: ", result)
    assert abs(result - (-657)) < 1

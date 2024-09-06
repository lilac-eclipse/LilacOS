from sandbox.turtle_homework.turtle_themed_learning import (
    Turtle,
    old_enough_for_booze,
    add_five,
    calculate_age_in_months,
    get_turtle_name_length,
    add_turtle_to_pond,
    get_adult_turtles,
    TurtlePond,
)

# def test_calculate_age_in_months() -> None:
#     assert calculate_age_in_months(2) == 24
#     assert calculate_age_in_months(0.5) == 6


# TODO: saddddddd face
def test_old_enough_for_booze():
    assert old_enough_for_booze(19) == True
    assert old_enough_for_booze(16) == False
    assert old_enough_for_booze(62) == False
    assert old_enough_for_booze(93) == True


# TODO: Brain expolodes
def test_add_five():
    assert add_five(3) == 8


# TODO: Implement this test
def test_calculate_age_in_months():
    # Write at least two assertions testing the calculate_age_in_months function
    # HINT: Test with both integer and float inputs
    pass


# TODO: Implement this test
def test_get_turtle_name_length():
    # Write at least two assertions testing the get_turtle_name_length function
    # HINT: Test with names of different lengths
    pass


# TODO: Implement this test
def test_add_turtle_to_pond():
    # Create a list of Turtle objects and test adding a new Turtle
    # HINT: Check both the length of the list and the presence of the new Turtle
    pass


# TODO: Implement this test
def test_get_adult_turtles():
    # Create a list of Turtle objects with various ages and test get_adult_turtles
    # HINT: Ensure your list has both adult and non-adult turtles
    pass


# TODO: Implement this test
def test_turtle_pond_operations():
    # Test multiple operations of the TurtlePond class
    # 1. Create a TurtlePond and add at least 3 turtles
    # 2. Test get_average_age
    # 3. Test get_fastest_turtle
    # 4. Test get_turtle_colors
    pass

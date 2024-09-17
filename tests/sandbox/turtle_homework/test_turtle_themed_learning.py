from typing import List
import pytest
from sandbox.turtle_homework.turtle_themed_learning import (
    Turtle,
    add_five,
    calculate_age_in_months,
    get_turtle_name_length,
    add_turtle_to_pond,
    get_adult_turtles,
    create_turtle,
    old_enough_for_booze,
    update_turtle_age,
    calculate_turtle_speed,
    TurtlePond,
)


def test_old_enough_for_booze():
    assert old_enough_for_booze(19) == True
    assert old_enough_for_booze(16) == False
    assert old_enough_for_booze(62) == False
    assert old_enough_for_booze(93) == True


# TODO: Brain expolodes
def test_add_five():
    num = 3
    assert add_five(num) == 8
    # assert num == 8
    # assert add_five(3) == 8
    assert add_five(5) == 10


# TODO: Implement this test
def test_peri_calculate_age_in_months():
    # Write at least two assertions testing the calculate_age_in_months function
    # HINT: Test with both integer and float inputs
    assert calculate_age_in_months(1.5) == 18
    # passed


# TODO: Implement this test
def test_peri_get_turtle_name_length():
    # Write at least two assertions testing the get_turtle_name_length function
    # HINT: Test with names of different lengths
    assert get_turtle_name_length("Tomley") == 6
    # passed


# TODO: Implement this test
def test_peri_add_turtle_to_pond():
    # Create a list of Turtle objects and test adding a new Turtle
    # HINT: Check both the length of the list and the presence of the new Turtle
    turtlepoop = Turtle("Poop", 5, "green", 3)
    turtlepop = Turtle("Pop", 20, "lavender", 35)
    turtleboop = Turtle("Boop", 55, "pink", 10)
    turtlesnot = Turtle("Snot", 14, "blue", 20)
    turtlist = [turtlepoop, turtlepop, turtlesnot]
    # turtlist.append(turtleboop)
    updated_list = add_turtle_to_pond(turtlist, turtleboop)

    assert turtleboop in turtlist
    assert turtleboop in updated_list

    # pass/fail


# TODO: Implement this test
def test_peri_get_adult_turtles():
    # Create a list of Turtle objects with various ages and test get_adult_turtles
    # HINT: Ensure your list has both adult and non-adult turtles
    pass


# TODO: Implement this test
def test_peri_turtle_pond_operations():
    # Test multiple operations of the TurtlePond class
    # 1. Create a TurtlePond and add at least 3 turtles
    # 2. Test get_average_age
    # 3. Test get_fastest_turtle
    # 4. Test get_turtle_colors
    pass


# u-bove is Quill's
# b-low is lilac


def test_calculate_age_in_months() -> None:
    assert calculate_age_in_months(2) == 24
    assert calculate_age_in_months(0.5) == 6


def test_get_turtle_name_length() -> None:
    assert get_turtle_name_length("Speedy") == 6
    assert get_turtle_name_length("Mr. Shell") == 9


def test_add_turtle_to_pond() -> None:
    pond: List[Turtle] = [
        Turtle("Speedy", 6, "green", 15),
        Turtle("Slowpoke", 4, "brown", 20),
    ]
    new_turtle = Turtle("Shelly", 5, "green", 18)
    updated_pond = add_turtle_to_pond(pond, new_turtle)
    assert len(updated_pond) == 3
    assert updated_pond[-1].name == "Shelly"


def test_get_adult_turtles() -> None:
    turtles: List[Turtle] = [
        Turtle("Speedy", 6, "green", 15),
        Turtle("Slow", 4, "brown", 20),
        Turtle("Old", 10, "gray", 25),
    ]
    adult_turtles = get_adult_turtles(turtles)
    assert len(adult_turtles) == 2
    assert all(turtle.age >= 5 for turtle in adult_turtles)


def test_create_turtle() -> None:
    turtle: Turtle = create_turtle("Speedy", 6, "green", 15)
    assert turtle.name == "Speedy"
    assert turtle.age == 6
    assert turtle.color == "green"
    assert turtle.weight == 15


def test_update_turtle_age() -> None:
    turtle = Turtle("Speedy", 6, "green", 15)
    updated_turtle = update_turtle_age(turtle, 7)
    assert updated_turtle.age == 7


def test_calculate_turtle_speed() -> None:
    turtle1 = Turtle("Speedy", 5, "green", 10)
    turtle2 = Turtle("Slow", 3, "brown", 15)
    assert calculate_turtle_speed(turtle1) == 9
    assert calculate_turtle_speed(turtle2) == 4.5


@pytest.fixture(name="pond")
def sample_pond() -> TurtlePond:
    pond = TurtlePond()
    pond.add_turtle(Turtle("Speedy", 6, "green", 15))
    pond.add_turtle(Turtle("Slow", 4, "brown", 20))
    pond.add_turtle(Turtle("Shelly", 5, "green", 18))
    return pond


def test_turtle_pond_add_turtle(pond: TurtlePond) -> None:
    assert len(pond.turtles) == 3
    assert pond.turtles[0].name == "Speedy"


def test_turtle_pond_average_age(pond: TurtlePond) -> None:
    assert pond.get_average_age() == 5


def test_turtle_pond_fastest_turtle(pond: TurtlePond) -> None:
    assert pond.get_fastest_turtle() == "Speedy"


def test_turtle_pond_turtle_colors(pond: TurtlePond) -> None:
    assert set(pond.get_turtle_colors()) == {"green", "brown"}

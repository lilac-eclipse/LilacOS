from typing import List
import pytest
from sandbox.turtle_homework.turtle_themed_learning import (
    Turtle,
    calculate_age_in_months,
    get_turtle_name_length,
    add_turtle_to_pond,
    get_adult_turtles,
    create_turtle,
    update_turtle_age,
    calculate_turtle_speed,
    TurtlePond,
)


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


@pytest.fixture
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

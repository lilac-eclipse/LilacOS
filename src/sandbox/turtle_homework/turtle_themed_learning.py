from typing import List
from dataclasses import dataclass


@dataclass
class Turtle:
    def __init__(self, name: str, age: int, color: str, weight: float) -> None:
        self.name = name
        self.age = age
        self.color = color
        self.weight = weight


# 0. New Function to make my brain explode
def add_five(number: float) -> float:

    add_v = number + 5
    return add_v


# 00. New Function, sadddddd face
# New function who's job is to determine if someone is of age to buy alcohol
# the input should be the person's age
# the output should be true, if of age, false otherwise
# should return a type bool (like float, string etc.) (bool apparently means something)
def old_enough_for_booze(age_in_years: int) -> bool:
    if age_in_years > 90:
        return True
    if age_in_years > 60:
        return False
    if age_in_years > 18:
        return True

    return False


# 1. Variables and basic operations
def calculate_age_in_months(age_in_years: float) -> float:
    """
    Convert age in years to months.
    """

    age_in_months = age_in_years * 12
    # TODO: Calculate and return the age in months
    return age_in_months


# 2. Strings and string methods
def get_turtle_name_length(name: str) -> int:
    """
    Return the length of the turtle's name.
    """
    # TODO: Return the length of the name
    return 0


# 3. Lists and list operations
def add_turtle_to_pond(pond: List[Turtle], turtle: Turtle) -> List[Turtle]:
    """
    Add a turtle to the pond list and return the updated list.
    """
    # TODO: Add the turtle to the pond list and return the updated list
    return []


# 4. List comprehension
def get_adult_turtles(turtles: List[Turtle]) -> List[Turtle]:
    """
    Return a list of turtles that are 5 years or older.
    """
    # TODO: Use list comprehension to return turtles 5 years or older
    return []


# 5. Creating objects
def create_turtle(name: str, age: int, color: str, weight: float) -> Turtle:
    """
    Create and return a Turtle object.
    """
    # TODO: Create and return a Turtle object with the given attributes
    return Turtle("", 0, "", 0)


# 6. Object operations
def update_turtle_age(turtle: Turtle, new_age: int) -> Turtle:
    """
    Update the age of the turtle and return the updated turtle.
    """
    # TODO: Update the age of the turtle and return it
    return Turtle("", 0, "", 0)


# 7. Functions with multiple parameters
def calculate_turtle_speed(turtle: Turtle) -> float:
    """
    Calculate turtle speed based on age and weight.
    Speed formula: (age * 2) - (weight / 10)
    """
    # TODO: Calculate and return the turtle's speed using the given formula
    return 0


# 8. Putting it all together: Turtle Pond Simulation
class TurtlePond:
    def __init__(self) -> None:
        self.turtles: List[Turtle] = []

    def add_turtle(self, turtle: Turtle) -> None:
        # TODO: Add the turtle to the turtles list
        pass

    def get_average_age(self) -> float:
        # TODO: Calculate and return the average age of all turtles in the pond
        return 0

    def get_fastest_turtle(self) -> str:
        # TODO: Find and return the name of the fastest turtle using the
        # calculate_turtle_speed function
        return ""

    def get_turtle_colors(self) -> List[str]:
        # TODO: Return a list of all unique turtle colors in the pond
        return []

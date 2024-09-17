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

    # add_v = number + 5
    number = number + 5
    return number


# What else


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
# notes: and pretend hints that are 90% of the answer... we shall see. len is important
# def main() -> None:
# print("do whatever your heart desires!")
# # print_tutorial()
# a = "dog"
# print(a)
# print(len(a))


def get_turtle_name_length(name: str) -> int:
    """
    Return the length of the turtle's name.
    """

    turtles_name_length = len(name)
    # TODO: Return the length of the name
    return turtles_name_length


# 3. Lists and list operations
def add_turtle_to_pond(pond: List[Turtle], turtle: Turtle) -> List[Turtle]:
    """
    Add a turtle to the pond list and return the updated list.
    """
    pond.append(turtle)
    # turtlist = pond
    # turt_name = turtle
    # turtlist.append(turtle)
    # TODO: Add the turtle to the pond list and return the updated list
    return pond


# 4. List comprehension
# adapt my learning from lines turtle name length, and add turtle to pond and
# good luck.....
# also check out sandbox craziness, then remember to Highlight part of the code,
# press shift + return, and enjoy the output
def get_adult_turtles(turtles: List[Turtle]) -> List[Turtle]:
    """
    Return a list of turtles that are 5 years or older.
    """
    # Taking in a list of turtle and transforming a list of turtle.... contents need
    #  to be different.

    # TODO: Use list comprehension to return turtles 5 years or older
    print(turtles)
    return []


# 5. Creating objects
# adapt my learning from lines turtle name length, and add turtle to pond and
# good luck.....
# also check out sandbox craziness, then remember to Highlight part of the code,
# press shift + return, and enjoy the output
def create_turtle(name: str, age: int, color: str, weight: float) -> Turtle:
    """
    Create and return a Turtle object.
    """
    # TODO: Create and return a Turtle object with the given attributes
    print(name)
    print(age)
    print(color)
    print(weight)
    return Turtle("", 0, "", 0)


# 6. Object operations
def update_turtle_age(turtle: Turtle, new_age: int) -> Turtle:
    """
    Update the age of the turtle and return the updated turtle.
    """
    # TODO: Update the age of the turtle and return it
    print(turtle)
    print(new_age)
    return Turtle("", 0, "", 0)


# 7. Functions with multiple parameters
def calculate_turtle_speed(turtle: Turtle) -> float:
    """
    Calculate turtle speed based on age and weight.
    Speed formula: (age * 2) - (weight / 10)
    """
    # TODO: Calculate and return the turtle's speed using the given formula
    print(turtle)
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

# pylint: disable=import-error
import inspect
from test_peri_turtle_themed_learning import (
    test_calculate_age_in_months,
    test_get_turtle_name_length,
    test_add_turtle_to_pond,
    test_get_adult_turtles,
    test_turtle_pond_operations,
)


def run_student_test(test_func):
    # pylint: disable=broad-exception-caught
    try:
        test_func()
        return True
    except AssertionError:
        return False
    except Exception as e:
        print(f"Error in {test_func.__name__}: {str(e)}")
        return False


def test_student_calculate_age_in_months():
    assert run_student_test(
        test_calculate_age_in_months
    ), "test_calculate_age_in_months is incorrect or incomplete"


def test_student_get_turtle_name_length():
    assert run_student_test(
        test_get_turtle_name_length
    ), "test_get_turtle_name_length is incorrect or incomplete"


def test_student_add_turtle_to_pond():
    assert run_student_test(
        test_add_turtle_to_pond
    ), "test_add_turtle_to_pond is incorrect or incomplete"


def test_student_get_adult_turtles():
    assert run_student_test(
        test_get_adult_turtles
    ), "test_get_adult_turtles is incorrect or incomplete"


def test_student_turtle_pond_operations():
    assert run_student_test(
        test_turtle_pond_operations
    ), "test_turtle_pond_operations is incorrect or incomplete"


def test_assertion_count():
    # Check if each test function has at least one assertion
    for test_func in [
        test_calculate_age_in_months,
        test_get_turtle_name_length,
        test_add_turtle_to_pond,
        test_get_adult_turtles,
        test_turtle_pond_operations,
    ]:
        func_source = inspect.getsource(test_func)
        assert (
            "assert" in func_source
        ), f"{test_func.__name__} doesn't contain any assertions"

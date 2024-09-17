def print_string_length() -> None:
    """
    Demonstrates printing a string and its length.
    """
    a = "dog"
    print(a)
    print(len(a))

    # Output:
    # dog
    # 3


def manipulate_list() -> None:
    """
    Demonstrates basic list operations and iteration.
    """
    llama = [3, 4, 7]
    print(llama)

    # Uncomment to add an element to the list
    # e = 4
    # llama.append(e)

    for x in llama:
        print(x)
        if x == 4:
            print("we found it")

    # Output:
    # [3, 4, 7]
    # 3
    # 4
    # we found it
    # 7


def create_incremented_list() -> None:
    """
    Creates a new list with each element incremented by 1.
    """
    llama = [3, 4, 7]
    better_llamas = []
    for x in llama:
        better_llamas.append(x + 1)
    print(better_llamas)

    # Output:
    # [4, 5, 8]


def modify_ages_in_place() -> None:
    """
    Modifies a list of ages in place, adding 5 to ages over 30.
    """
    ages = [23, 45, 67, 13, 14, 85, 20, 40]
    original_ages = ages.copy()  # Create a copy to preserve the original
    print("Original ages:", original_ages)

    for i, x in enumerate(ages):
        if x > 30:
            ages[i] = x + 5

    print("Modified ages:", ages)

    # Output:
    # Original ages: [23, 45, 67, 13, 14, 85, 20, 40]
    # Modified ages: [23, 50, 72, 13, 14, 90, 20, 45]


def create_modified_ages_list() -> None:
    """
    Creates a new list of ages, adding 5 to ages over 30.
    """
    ages = [23, 45, 67, 13, 14, 85, 20, 40]
    updated_ages = []
    for x in ages:
        if x > 30:
            updated_ages.append(x + 5)
        else:
            updated_ages.append(x)
    print("Original ages:", ages)
    print("Updated ages:", updated_ages)

    # Output:
    # Original ages: [23, 45, 67, 13, 14, 85, 20, 40]
    # Updated ages: [23, 50, 72, 13, 14, 90, 20, 45]


def demonstrate_modulo_operation() -> None:
    """
    Demonstrates the modulo operation with various numbers.
    """
    numbers = [2, 9, 20, 1, 2, 3, 4, 5, 6, 7, 8]
    for num in numbers:
        print(f"5 % {num} =", 5 % num)

    # Commented out to avoid ZeroDivisionError
    # print(5 % 0)

    # Output:
    # 5 % 2 = 1
    # 5 % 9 = 5
    # 5 % 20 = 5
    # 5 % 1 = 0
    # ...


def rotate_list() -> None:
    """
    Rotates a list of ages by one position to the right.
    """
    ages = [23, 45, 67, 13]
    new_ages = [0] * len(ages)
    for i, x in enumerate(ages):
        new_ages[(i + 1) % len(ages)] = x
    print("Original ages:", ages)
    print("Rotated ages:", new_ages)

    # Output:
    # Original ages: [23, 45, 67, 13]
    # Rotated ages: [13, 23, 45, 67]

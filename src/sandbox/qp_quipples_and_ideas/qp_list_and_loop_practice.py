def list_practice() -> None:
    print("do whatever your heart desires!")

    # a = "dog"
    # print(a)
    # print(len(a))

    llama = [3, 4, 7]

    # print(llama)
    # e = 4
    # llama.append(e)

    print(llama)
    for x in llama:
        print(x)
        if x == 4:
            print("we found it")

    better_llamas = []
    for x in llama:
        better_llamas.append(x + 1)
    print(better_llamas)

    print(".......................")

    ages = [23, 45, 67, 13, 14, 85, 20, 40]
    original_ages = ages
    print(original_ages)
    for i, x in enumerate(ages):
        if x > 30:
            ages[i] = x + 5
    print(ages)

    updated_ages = []
    for x in ages:
        if x > 30:
            updated_ages.append(x + 5)
        else:
            updated_ages.append(x)
    print(updated_ages)
    print(ages)
    print(original_ages)


def other() -> None:
    print(".......................>>>>>>>>>>>")
    print(5 % 2)
    print(5 % 9)
    print(5 % 20)
    print(5 % 1)
    print(5 % 2)
    print(5 % 3)
    print(5 % 4)
    print(5 % 5)
    print(5 % 6)
    print(5 % 7)
    print(5 % 8)
    print("yyyyyyyyyyyyyyyyyyyyyyyyyy")
    # print(5 % 0)
    print("bbbbbbbblllllllllaaaaaaahhhhhh")
    ages = [23, 45, 67, 13]
    # original_ages = ages
    # print(original_ages)
    new_ages = [0, 0, 0, 0]
    for i, x in enumerate(ages):
        # if x > 30:
        new_ages[(i + 1) % len(ages)] = x
    print(ages)
    print(new_ages)

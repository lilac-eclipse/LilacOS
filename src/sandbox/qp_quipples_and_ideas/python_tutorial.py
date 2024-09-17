from typing import List, Optional


def section_1_variables() -> None:
    a = "hi"
    b = 2
    c = 3
    print(10)
    print(a)
    print(b + c)
    d = b * c
    print(d)


def section_2_lists() -> None:
    llama = [3]
    e = 4
    llama.append(2)
    print(llama)
    llama.append(e)
    print(llama)
    llama.pop(1)
    print(llama)
    llama.insert(1, 10)
    print(llama)
    print(llama[2])


def section_3_maps() -> None:
    brand = {}
    brand[3] = "ie"
    print(brand)
    brand[100] = "jen"
    print(brand)
    print(brand[3])


def section_3_1_maps_2() -> None:
    phones = {"brandie": "505-123-4532", "jenn": "505-987-1452"}
    print(phones)
    print(phones["brandie"])
    phones["julie"] = "923-412-1522"
    print(phones)
    phones.pop("brandie")
    print(phones)


def section_4_conditionals() -> None:
    a = 3
    b = 2
    if a > b:
        print("great!!")
    else:
        print("not great...")
    l = [1, 2, 3]
    if a not in l:
        print("no no no")
    else:
        print("i see")


def section_5_loops() -> None:
    names = ["brandie", "jenn", "julie"]
    for n in names:
        print(n)
    for i, n in enumerate(names):
        print(str(i) + " -> " + n)
    m = {"b": "randie", "j": "enn"}
    for k, v in m.items():
        print(k + " -> " + v)


def section_6_classes() -> None:

    class Dog:  # pylint: disable=too-few-public-methods
        def __init__(self, name: str) -> None:
            self.my_name = name

        def speak(self) -> None:
            print("Hello. My name is " + self.my_name)

    j = Dog("Jedi")
    h = Dog("Harper")
    j.speak()
    h.speak()


def section_7_challenge() -> None:

    class Human:
        def __init__(self, name: str) -> None:
            self.name = name
            self.friends: List["Human"] = []
            self.best_friend: Optional["Human"] = None

        def add_friend(self, friend: "Human") -> None:
            self.friends.append(friend)

        def greet_friends(self) -> None:
            for f in self.friends:
                if f == self.best_friend:
                    print(f"{self.name}: bestie!!!!")
                else:
                    print(f"{self.name}: hello friend, {f.name}")
                f.respond(self)

        def respond(self, greeter: "Human") -> None:
            if greeter in self.friends:
                print(f"{self.name}: hiii")
            else:
                print(f"{self.name}: do i know you???")

        def set_best_friend(self, human: "Human") -> None:
            self.best_friend = human

    brandie = Human("brandie")
    jenn = Human("jenn")
    julie = Human("julie")
    m = Human("marques Mc Marco, the third (esquire)")
    ppl = {brandie: 0, jenn: 0, julie: 0, m: 1}
    for p1, _ in ppl.items():
        for p2, v2 in ppl.items():
            if p1 is not p2 and v2 < 1:
                p1.add_friend(p2)
    brandie.set_best_friend(julie)
    for p, _ in ppl.items():
        p.greet_friends()

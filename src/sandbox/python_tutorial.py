def print_section_header(section_number, section_name):
    print("=============")
    print(f"==Section {section_number}, {section_name} ==")
    print("=============")


def section_1_variables():
    print_section_header(1, "variables")
    a = "hi"
    b = 2
    c = 3
    print(10)
    print(a)
    print(b + c)
    d = b * c
    print(d)


def section_2_lists():
    print_section_header(2, "lists")
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


def section_3_maps():
    print_section_header(3, "maps")
    brand = {}
    brand[3] = "ie"
    print(brand)
    brand[100] = "jen"
    print(brand)
    print(brand[3])


def section_3_1_maps_2():
    print_section_header("3.1", "maps 2")
    phones = {"brandie": "505-123-4532", "jenn": "505-987-1452"}
    print(phones)
    print(phones["brandie"])
    phones["julie"] = "923-412-1522"
    print(phones)
    phones.pop("brandie")
    print(phones)


def section_4_conditionals():
    print_section_header(4, "conditionals")
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


def section_5_loops():
    print_section_header(5, "loops")
    names = ["brandie", "jenn", "julie"]
    for n in names:
        print(n)
    for i, n in enumerate(names):
        print(str(i) + " -> " + n)
    m = {"b": "randie", "j": "enn"}
    for k, v in m.items():
        print(k + " -> " + v)


def section_6_classes():
    print_section_header(6, "classes")

    class Dog:
        def __init__(self, name):
            self.my_name = name

        def speak(self):
            print("Hello. My name is " + self.my_name)

    j = Dog("Jedi")
    h = Dog("Harper")
    j.speak()
    h.speak()


def section_7_challenge():
    print_section_header(7, "challenge")

    class Human:
        def __init__(self, name):
            self.name = name
            self.friends = []
            self.best_friend = None

        def add_friend(self, friend):
            self.friends.append(friend)

        def greet_friends(self):
            for f in self.friends:
                if f == self.best_friend:
                    print(self.name + ": bestie!!!!")
                else:
                    print(self.name + ": hello friend, " + f.name)

                f.respond(self)

        def respond(self, greeter):
            if greeter in self.friends:
                print(self.name + ": hiii")
            else:
                print(self.name + ": do i know you???")

        def set_best_friend(self, human):
            self.best_friend = human

    brandie = Human("brandie")
    jenn = Human("jenn")
    julie = Human("julie")
    m = Human("marques Mc Marco, the third (esquire)")
    ppl = {brandie: 0, jenn: 0, julie: 0, m: 1}
    for p1, v1 in ppl.items():
        for p2, v2 in ppl.items():
            if p1 is not p2 and v2 < 1:
                p1.add_friend(p2)
    brandie.set_best_friend(julie)
    for p, _ in ppl.items():
        p.greet_friends()


def print_tutorial():
    section_1_variables()
    section_2_lists()
    section_3_maps()
    section_3_1_maps_2()
    section_4_conditionals()
    section_5_loops()
    section_6_classes()
    section_7_challenge()

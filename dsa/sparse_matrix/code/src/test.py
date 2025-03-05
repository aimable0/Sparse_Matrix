#!/usr/bin/python3


class Person:

    def __init__(self, first, last) -> None:
        self.first = first
        self.last = last

    def add(self, other):
        added_person = Person((self.first + other.first), (self.last + other.last))
        print(added_person)

    def __str__(self) -> str:
        return f"This is {self.first} {self.last}"

person1 = Person("Aim", "Nkurikiyi")
print(person1)
person2 = Person("able", "mana")
print(person2)

# both people added
person1.add(person2)
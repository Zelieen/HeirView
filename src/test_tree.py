import unittest

from tree import Tree
from node import Person, Event

class TestNode(unittest.TestCase):
    def test_creation_tree(self):
        t = Tree()
        self.assertEqual("A family tree with 0 persons in it.", str(t))
    def test_tree_add_person(self):
        t = Tree()
        p = Person("Luke", "Skywalker")
        t.add_person(p)
        self.assertEqual("A family tree with 1 persons in it.", str(t))
    def test_tree_find(self):
        t = Tree()
        p = Person("Luke", "Skywalker")
        t.add_person(p)
        self.assertEqual("This is Person #0: Luke SKYWALKER.", str(t.find_person(0)))
    def test_tree_add_child(self):
        t = Tree()
        p1 = Person("Anakin", "Skywalker")
        p2 = Person("Luke", "Skywalker")
        t.add_person(p1)
        t.add_person(p2)
        t.add_child(0, 1, False)
        self.assertEqual("This is Person #0: Anakin SKYWALKER.", str(t.find_person(t.find_person(1).father)))
    def test_tree_add_father(self):
        t = Tree()
        p1 = Person("Anakin", "Skywalker")
        p2 = Person("Luke", "Skywalker")
        t.add_person(p1)
        t.add_person(p2)
        t.add_father(1, 0)
        self.assertEqual("This is Person #0: Anakin SKYWALKER.", str(t.find_person(t.find_person(1).father)))
    def test_tree_add_partner(self):
        t = Tree()
        p1 = Person("Anakin", "Skywalker")
        p2 = Person("Padmé", "naberie")
        t.add_person(p1)
        t.add_person(p2)
        t.add_partnership(1, 0)
        self.assertEqual("This is Person #0: Anakin SKYWALKER.", str(t.find_person(t.find_person(1).partners[0]))) 

if __name__ == "__main__":
    unittest.main()
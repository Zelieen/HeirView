import unittest

from tree import Tree
from node import Person, Event

class TestNode(unittest.TestCase):
    def test_creation_tree(self):
        t = Tree()
        self.assertEqual("A family tree with 0 persons in it.", str(t))
    def test_tree_add_person(self):
        t = Tree()
        p = Person(None, "Luke", "Skywalker")
        t.add_person(p)
        self.assertEqual("A family tree with 1 persons in it.", str(t))
    def test_tree_find(self):
        t = Tree()
        p = Person(0, "Luke", "Skywalker")
        t.add_person(p)
        self.assertEqual("This is Person #0: Luke SKYWALKER.", str(t.find_person(0)))
    def test_tree_add_child(self):
        t = Tree()
        p1 = Person(0, "Anakin", "Skywalker")
        p2 = Person(1, "Luke", "Skywalker")
        t.add_person(p1)
        t.add_person(p2)
        t.add_child(0, 1, False)
        self.assertEqual("This is Person #0: Anakin SKYWALKER.", str(t.find_person(t.find_person(1).father)))
    def test_tree_add_father(self):
        t = Tree()
        p1 = Person(0, "Anakin", "Skywalker")
        p2 = Person(1, "Luke", "Skywalker")
        t.add_person(p1)
        t.add_person(p2)
        t.add_father(1, 0)
        self.assertEqual("This is Person #0: Anakin SKYWALKER.", str(t.find_person(t.find_person(1).father)))
    def test_tree_add_partner(self):
        t = Tree()
        p1 = Person(0,"Anakin", "Skywalker")
        p2 = Person(1, "Padmé", "naberrie")
        t.add_person(p1)
        t.add_person(p2)
        t.add_partnership(1, 0)
        self.assertEqual("This is Person #0: Anakin SKYWALKER.", str(t.find_person(t.find_person(1).partners[0]))) 

    def test_tree_get_free_IDs(self):
        t = Tree()
        p1 = Person(6,"Anakin", "Skywalker")
        p2 = Person(0, "Padmé", "naberrie")
        p3 = Person(4, "Luke", "Skywalker")
        t.add_person(p1)
        t.add_person(p2)
        t.add_person(p3)
        self.assertEqual([1, 2, 3, 5], t.get_all_free_IDs())

    def test_tree_get_next_free_ID(self):
        t = Tree()
        p1 = Person(3,"Anakin", "Skywalker")
        p2 = Person(0, "Padmé", "naberrie")
        t.add_person(p1)
        t.add_person(p2)
        self.assertEqual(1, t.get_next_free_ID())

    def test_tree_get_next_free_ID_add(self):
        t = Tree()
        p1 = Person(1,"Anakin", "Skywalker")
        p2 = Person(0, "Padmé", "naberrie")
        t.add_person(p1)
        t.add_person(p2)
        self.assertEqual(2, t.get_next_free_ID())

if __name__ == "__main__":
    unittest.main()
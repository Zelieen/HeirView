import unittest

from tree import Tree
from node import Person, Event
from chart import ChartID

tt = Tree()
tp1 = Person(6,"Anakin", "Skywalker")
tp2 = Person(0, "Padmé", "naberrie")
tp3 = Person(4, "Luke", "Skywalker")
tt.add_person(tp1)
tt.add_person(tp2)
tt.add_person(tp3)
tt.add_mother(4, 0)
tt.add_father(4, 6)

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
    def test_tree_get_direct_ancestors(self):
        #use test Tree() tt
        self.assertEqual([ChartID(0, 1), ChartID(6, 1)], tt.find_direct_ancestors(4))
    def test_tree_generation_renumbering(self):
        #use test Tree() tt
        chart_list = [ChartID(4, -1), ChartID(0, 0), ChartID(6, 0), ChartID(8, -1)]
        self.assertEqual([ChartID(4, 0), ChartID(0, 1), ChartID(6, 1), ChartID(8, 0)], tt.renumber_generations(chart_list))
    def test_tree_get_ancestors_for_chart(self):
        #use test Tree() tt
        t = tt
        p1 = Person(8, "Leia", "Skywalker")
        p2 = Person(10, "Jacen", "Solo")
        p3 = Person(9, "Han", "Solo")
        t.add_person(p1)
        t.add_person(p2)
        t.add_person(p3)
        t.add_father(8, 6)
        t.add_mother(8, 0)
        
        t.add_father(10, 9)
        t.add_mother(10, 8)
        self.assertEqual([ChartID(4, 1), ChartID(0, 2), ChartID(6, 2), ChartID(8, 1), ChartID(10, 0), ChartID(9, 1)], t.get_ancestors_for_chart(4, 2))

if __name__ == "__main__":
    unittest.main()
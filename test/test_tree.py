import unittest

from tree import Tree
from chart import ChartID, renumber_generations

tt = Tree()
tt.add_person("Anakin", "Skywalker", 6)
tt.add_person("Padmé", "naberrie", 0)
tt.add_person("Luke", "Skywalker", 4)
tt.add_mother(4, 0)
tt.add_father(4, 6)


class TestNode(unittest.TestCase):
    def test_creation_tree(self):
        t = Tree()
        self.assertEqual("A family tree with 0 persons in it.", str(t))

    def test_tree_add_person(self):
        t = Tree()
        t.add_person("Luke", "Skywalker")
        self.assertEqual("A family tree with 1 persons in it.", str(t))

    def test_tree_find(self):
        t = Tree()
        t.add_person("Luke", "Skywalker", 0)
        self.assertEqual("This is Person #0: Luke SKYWALKER.", str(t.find_person(0)))

    def test_tree_add_child(self):
        t = Tree()
        t.add_person("Anakin", "Skywalker", 0)
        t.add_person("Luke", "Skywalker", 1)
        t.add_child(0, 1, False)
        child = t.find_person(1)
        father = child.father if child else None
        self.assertEqual(
            "This is Person #0: Anakin SKYWALKER.",
            str(t.find_person(father)),
        )

    def test_tree_add_father(self):
        t = Tree()
        t.add_person("Anakin", "Skywalker", 0)
        t.add_person("Luke", "Skywalker", 1)
        t.add_father(1, 0)
        child = t.find_person(1)
        father = child.father if child else None
        self.assertEqual(
            "This is Person #0: Anakin SKYWALKER.",
            str(t.find_person(father)),
        )

    def test_tree_add_partner(self):
        t = Tree()
        t.add_person("Anakin", "Skywalker", 0)
        t.add_person("Padmé", "naberrie", 1)
        t.add_partnership(1, 0)
        person = t.find_person(1)
        partner = person.partners[0] if person else None
        self.assertEqual(
            "This is Person #0: Anakin SKYWALKER.",
            str(t.find_person(partner)),
        )

    def test_tree_get_free_IDs(self):
        t = Tree()
        t.add_person("Anakin", "Skywalker", 6)
        t.add_person("Padmé", "naberrie", 0)
        t.add_person("Luke", "Skywalker", 4)
        self.assertEqual([1, 2, 3, 5], t.get_all_free_IDs())

    def test_tree_get_next_free_ID(self):
        t = Tree()
        t.add_person("Anakin", "Skywalker", 3)
        t.add_person("Padmé", "naberrie", 0)
        self.assertEqual(1, t.get_next_free_ID())

    def test_tree_get_next_free_ID_add(self):
        t = Tree()
        t.add_person("Anakin", "Skywalker", 1)
        t.add_person("Padmé", "naberrie", 0)
        self.assertEqual(2, t.get_next_free_ID())

    def test_tree_get_direct_ancestors(self):
        # use test Tree() tt
        self.assertEqual([ChartID(0, 1), ChartID(6, 1)], tt.find_all_direct_ancestors(4))

    def test_tree_generation_renumbering(self):
        # use test Tree() tt
        chart_list = [ChartID(4, -1), ChartID(0, 0), ChartID(6, 0), ChartID(8, -1)]
        self.assertEqual(
            [ChartID(4, 0), ChartID(0, 1), ChartID(6, 1), ChartID(8, 0)],
            renumber_generations(chart_list),
        )

    def test_tree_get_ancestors_for_chart(self):
        # use test Tree() tt
        t = tt
        t.add_person("Leia", "Skywalker", 8)
        t.add_person("Jacen", "Solo", 10)
        t.add_person("Han", "Solo", 9)
        t.add_father(8, 6)
        t.add_mother(8, 0)

        t.add_father(10, 9)
        t.add_mother(10, 8)
        self.assertEqual(
            [
                ChartID(4, 1),
                ChartID(0, 2),
                ChartID(6, 2),
                ChartID(8, 1),
                ChartID(10, 0),
                ChartID(9, 1),
            ],
            t.get_ancestors_for_chart(4, 2),
        )

    def test_tree_get_ancestors_for_chart_bounce_many(self):
        # use test Tree() tt
        self.assertEqual(
            [
                ChartID(4, 1),
                ChartID(0, 2),
                ChartID(6, 2),
                ChartID(8, 1),
                ChartID(10, 0),
                ChartID(9, 1),
            ],
            tt.get_ancestors_for_chart(4, 7),
        )


if __name__ == "__main__":
    unittest.main()

import unittest

from chart import ChartID, Chart
from node import Person
from unit import Badge, Connector

class TestNode(unittest.TestCase):
    def test_ChartID_creation(self):
        ci = ChartID(5, 4)
        self.assertEqual(4, ci.gen)
    def test_ChartID_equality(self):
        ci1 = ChartID(5, 8)
        ci2 = ChartID(5, 4)
        self.assertEqual(ci1, ci2)

    def test_Chart_creation(self):
        c = Chart()
        self.assertEqual(0, c.pos_y)
    def test_Chart_add_badge(self):
        c = Chart()
        c.add_badge(Badge(1), 0)
        self.assertEqual(1, c.badge_col[0][0].person_ID)
    def test_Chart_add_badge2(self):
        c = Chart()
        c.add_badge(Badge(1), 0)
        c.add_badge(Badge(9), 0, 0)
        self.assertEqual(9, c.badge_col[0][0].person_ID)
    def test_Chart_add_badge_noGen(self):
        c = Chart()
        c.add_badge(Badge(1), 0)
        c.add_badge(Badge(9), -5, 0)
        self.assertEqual(1, len(c.badge_col[0]))
    def test_Chart_reverse(self):
        c = Chart()
        c.add_badge(Badge(1), 0)
        c.add_badge(Badge(9), 1)
        c.inverse_generations()
        self.assertEqual(9, c.badge_col[0][0].person_ID)
    def test_Chart_add_person(self):
        c = Chart()
        c.add_person(0, 5)
        self.assertEqual(1, len(c.badge_col))
    def test_Chart_add_persons(self):
        c = Chart()
        c.add_persons([ChartID(0, 5)])
        self.assertEqual(1, len(c.badge_col))
    def test_Chart_search_badge_ID_None(self):
        c = Chart()
        self.assertEqual(False, c.search_badge_place_by_ID(None))
    def test_Chart_search_badge_ID(self):
        c = Chart()
        c.add_person(0, 5)
        self.assertEqual((0, 0), c.search_badge_place_by_ID(0))
    def test_Chart_get_badge_by_place(self):
        c = Chart()
        c.add_person(4, 5)
        self.assertEqual(4, c.get_badge_by_place(0, 0).person_ID)
    def test_Chart_find_badge_ID(self):
        c = Chart()
        c.add_person(8, 5)
        self.assertEqual(8, c.find_badge_by_ID(8).person_ID)
    def test_Chart_make_connector(self):
        c = Chart()
        self.assertEqual(1, c.make_connector(1, 2, 3).to_left[0])
    def test_Chart_make_connector_father(self):
        c = Chart()
        self.assertEqual(3, c.make_connector(1, 2, 3).to_right[1])
    def test_Chart_add_connection_None(self):
        c = Chart()
        c.add_connection(1, 2, 3)
        self.assertEqual(0, len(c.connect_col))
    def test_Chart_add_to_connector_at(self):
        c = Chart()
        c.add_persons([ChartID(0, 0), ChartID(1, 1), ChartID(2, 1), ChartID(3, 0)])
        c.add_connection(0, 1, 2)
        c.add_connection(3, 1, 2)
        self.assertEqual([0, 3], c.connect_col[0][0].to_left)
    def test_Chart_add_connection(self):
        c = Chart()
        c.add_persons([ChartID(0, 0), ChartID(1, 1), ChartID(2, 1)])
        c.add_connection(0, 1, 2)
        self.assertEqual(1, len(c.connect_col[0]))

if __name__ == "__main__":
    unittest.main()
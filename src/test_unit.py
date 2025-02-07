import unittest

from unit import Unit, Badge, Connector

class TestNode(unittest.TestCase):
    def test_unit_create(self):
        u = Unit()
        self.assertEqual(0, u.pos_x)
    def test_unit_position(self):
        u = Unit()
        u.set_position(10, -4)
        self.assertEqual((10, -4), u.get_position())   
    def test_unit_size(self):
        u = Unit()
        u.set_size(0, 5)
        self.assertEqual((0, 5), u.get_size())

    def test_badge_size(self):
        u = Badge(3)
        self.assertEqual((50, 50), u.get_size())
    def test_badge_middle_point(self):
        u = Badge(4)
        self.assertEqual((25, 25), u.get_center())
    def test_badge_middle_right(self):
        u = Badge(2)
        self.assertEqual((50, 25), u.get_center("right"))

    def test_connector_size(self):
        c = Connector()
        self.assertEqual(10, c.spacer_length)

if __name__ == "__main__":
    unittest.main()
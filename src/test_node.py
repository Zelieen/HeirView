import unittest

from node import Person

class TestNode(unittest.TestCase):
    def test_creation(self):
        p = Person("Luke", "Skywalker")
        self.assertEqual("This is Person #None: Luke SKYWALKER.", str(p))

if __name__ == "__main__":
    unittest.main()
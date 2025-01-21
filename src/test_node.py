import unittest

from node import Person, Event

class TestNode(unittest.TestCase):
    def test_creation_person(self):
        p = Person(None, "Luke", "Skywalker")
        self.assertEqual("This is Person #None: Luke SKYWALKER.", str(p))
    def test_creation_person_None(self):
        p = Person(None)
        self.assertEqual("This is Person #None: name UNKNOWN.", str(p))
    def test_creation_event(self):
        p = Person(None)
        e = Event("Birth", p)
        self.assertEqual("This is an Event: birth happened None at None.", str(e))
    def test_creation_event_full(self):
        p = Person(None)
        e = Event("Death", p, "18 JAN 2025", "Where?!")
        self.assertEqual("This is an Event: death happened 18 JAN 2025 at Where?!.", str(e))
    def test_person_event(self):
        p = Person(3)
        p.add_event("death", None, "18 JAN 2025", "Where?!")
        self.assertEqual("This is an Event: death happened 18 JAN 2025 at Where?!.", str(p.death))
    def test_person_marriage(self):
        p = Person(3)
        p.add_event("marriage", [3, 4], "18 JAN 2025", "Where?!")
        self.assertEqual("This is an Event: marriage happened 18 JAN 2025 at Where?!.", str(p.events[0]))
    def test_person_marriage_persons(self):
        p = Person(3)
        p.add_event("marriage", [3, 4], "18 JAN 2025", "Where?!")
        self.assertEqual([3, 4], p.events[0].persons)


if __name__ == "__main__":
    unittest.main()
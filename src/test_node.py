import unittest

from node import Person, Event, UNKNOWN_NAME, UNKNOWN_SURNAME


class TestNode(unittest.TestCase):
    def test_creation_person(self):
        p = Person(12, "Luke", "Skywalker")
        self.assertEqual("This is Person #12: Luke SKYWALKER.", str(p))

    def test_creation_person_unknown(self):
        p = Person(-5)
        self.assertEqual(f"This is Person #-5: {UNKNOWN_NAME} {UNKNOWN_SURNAME}.", str(p))

    def test_creation_event(self):
        p = Person(0)
        e = Event("Birth")
        self.assertEqual("This is an Event: birth happened  at .", str(e))

    def test_creation_event_full(self):
        p = Person(None)
        e = Event("Death", [], "18 JAN 2025", "Where?!")
        self.assertEqual(
            "This is an Event: death happened 18 JAN 2025 at Where?!.", str(e)
        )

    def test_person_event(self):
        p = Person(3)
        p.add_event("death", [], "18 JAN 2025", "Where?!")
        self.assertEqual(
            "This is an Event: death happened 18 JAN 2025 at Where?!.", str(p.death)
        )

    def test_person_marriage(self):
        p = Person(3)
        p.add_event("marriage", [3, 4], "18 JAN 2025", "Where?!")
        self.assertEqual(
            "This is an Event: marriage happened 18 JAN 2025 at Where?!.",
            str(p.events[0]),
        )

    def test_person_marriage_persons(self):
        p = Person(3)
        p.add_event("marriage", [3, 4], "18 JAN 2025", "Where?!")
        self.assertEqual([3, 4], p.events[0].persons)


if __name__ == "__main__":
    unittest.main()

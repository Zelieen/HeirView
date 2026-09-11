from datetime import datetime


class Person:
    """Represents a person in Heirview."""

    def __init__(
        self,
        ID: int,
        given_name: str = "",
        surname: str = "",
    ):
        self._ID: int = ID  # family tree ID
        self.given_name: str = given_name
        self.surname: str = surname.upper()

        self.birth: Event | None = None
        self.death: Event | None = None
        self.events: list[Event] = []  # other life events

        self.father: int | None = None  # family tree ID
        self.mother: int | None = None  # family tree ID

        self.children: list[int] = []  # list of family tree IDs
        self.partnerslist: list[int] = []  # list of family tree IDs

        if self.given_name == "" and self.surname == "":
            self.given_name = "name is"
            self.surname = "UNKNOWN"

    def __str__(self):
        return f"This is Person #{self._ID}: {self.given_name} {self.surname}."

    def __repr__(self):
        return f"Person({self._ID}, {self.given_name}, {self.surname})"

    def add_event(
        self,
        typ: str,
        person_list: list[int] | None = None,
        date: datetime | str | None = None,
        place: str = "",
    ):
        if typ.lower() == "birth":
            self.birth = Event(typ, [self._ID], date=date, place=place)
            return
        if typ.lower() == "death":
            self.death = Event(typ, [self._ID], date=date, place=place)
            return

        new_set = {self._ID}
        if person_list != None:
            new_set.update(person_list)  # avoid duplicate persons
        new_list = list(new_set)

        if typ.lower() == "marriage":
            self.events.append(Event(typ, new_list, date=date, place=place))
            return
        else:
            print(f"Unknown event type: {typ}")


class Event:
    def __init__(
        self,
        typ: str,
        person_list: list[int] = [],
        date: datetime | str | None = None,
        place: str = "",
    ):
        self.type = typ.lower()  # a string like "birth", "death", "marriage"
        self.date = date  # a date object or simple string
        self.place = place  # a string for the name of the place
        self.persons = person_list  # a list of family tree IDs

    def __str__(self):
        return f"This is an Event: {self.type} happened {self.date} at {self.place}."

    def __repr__(self):
        return f"Event({self.type}, {self.persons}, {self.date}, {self.place})"


class Family:
    def __init__(
        self,
        mother_ID: int | None = None,
        father_ID: int | None = None,
        child_IDs: list[int] = [],
        marr_date: datetime | str | None = None,
        marr_place: str = "",
    ):
        self.mother = mother_ID
        self.father = father_ID
        self.children = child_IDs
        self.marr = Event(
            "marriage",
            [p for p in [self.mother, self.father] if p],
            marr_date,
            marr_place,
        )

    def __str__(self):
        return f"This is a family: wife #{self.mother} and husband #{self.father} with {len(self.children)} children."

    def __repr__(self):
        return f"Family({self.mother}, {self.father}, {self.children}, {self.marr.date}, {self.marr.place})"

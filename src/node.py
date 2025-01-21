class Person:
    def __init__(self, given_name=None, surname=None):
        self._ID = None #the ID in the family tree
        self.given_name = ""
        self.surname = ""

        self.birth = None # Event
        self.death = None # Event
        self.events = [] # a list of other life events

        self.father = None # family tree ID
        self.mother = None # family tree ID

        self.children = [] # list of family tree IDs
        self.partners = [] # list of family tree IDs
        
        if given_name != None:
            self.given_name = given_name
        
        if surname != None:
            self.surname = surname.upper()

        if self.given_name == "" and self.surname == "":
            self.given_name = "name"
            self.surname = "UNKNOWN"

    def __str__(self):
        return f"This is Person #{str(self._ID)}: {self.given_name} {self.surname}."
    
    def __repr__(self):
        return f"Person({self.given_name}, {self.surname})"

    def add_event(self, typ, person_list=None, date=None, place=None ):
        if typ.lower() == "birth":
            self.birth = Event(typ, [self._ID], date=date, place=place)
            return
        if typ.lower() == "death":
            self.death = Event(typ, [self._ID], date=date, place=place)
            return
        
        new_set = {self._ID}
        if person_list != None:
            new_set.update(person_list) # avoid duplicate persons
        new_list = list(new_set)

        if typ.lower() == "marriage":
            self.events.append(Event(typ, new_list, date=date, place=place))
            return
        else:
            print(f"Unknown event type: {typ}")


class Event:
    def __init__(self, typ, person_list, date=None, place=None):
        self.type = typ.lower() # a string like "birth", "death", "marriage"
        self.date = date # a date object or simple string
        self.place = place # a string for the name of the place
        self.persons = person_list # a list of family tree IDs

    def __str__(self):
        return f"This is an Event: {str(self.type)} happened {self.date} at {self.place}."
    
    def __repr__(self):
        return f"Event({self.type}, {self.persons}, {self.date}, {self.place})"
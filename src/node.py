class Person:
    def __init__(self, given_name=None, surname=None):
        self._ID = None #the ID in the family tree
        self.birth = None # Event
        self.death = None # Event

        self.father = None # family tree ID
        self.mother = None # family tree ID

        self.children = [] # list of family tree IDs
        self.partner = [] # list of family tree IDs
        
        if given_name == None and surname == None:
            self.surname == "UNKNOWN"
        else:
            self.given_name = given_name
            self.surname = surname.upper()

    def __str__(self):
        return f"This is Person #{str(self._ID)}: {self.given_name} {self.surname}."
    
    def __repr__(self):
        return f"Person(\'{self.given_name}\', {self.surname})"

class Event:
    def __init__(self, type, date=None, place=None):
        self.type = type
        self.date = date
        self.place = place
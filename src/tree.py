from node import Person

class Tree:
    def __init__(self):
        self._ID_count = None
        self.root_ID = None
        self.persons = {}
    
    def add_person(self, person):
        new_person = person
        if self._ID_count == None: # first person in the tree
            self.root_ID = 0
            self._ID_count = 0
        else:
            self._ID_count += 1
        new_person._ID = self._ID_count
        self.persons[new_person._ID] = new_person
        return self.persons[new_person._ID]

    def find_person(self, ID):
        found = None
        if ID in self.persons:
            found = self.persons[ID]
        return found

    def add_child(self, person, child, as_mother):
        if not self.find_person(person):
            print (f"person #{person} not found")
            return
        the_person = self.find_person(person)
        if self.find_person(child):
            the_child = self.find_person(child)
        else: 
            the_child = self.add_person(child)
        the_person.children.append(the_child._ID)
        if as_mother:
            the_child.mother = the_person._ID
        else:
            the_child.father = the_person._ID

    def add_parent(self, child, parent, as_mother):
        if not self.find_person(child):
            print (f"person #{child} not found")
            return
        the_child = self.find_person(child)
        if self.find_person(parent):
            the_parent = self.find_person(parent)
        else: 
            the_parent = self.add_person(parent)
        the_parent.children.append(the_child._ID)
        if as_mother:
            the_child.mother = the_parent._ID
        else:
            the_child.father = the_parent._ID

    def add_father(self, child, father):
        self.add_parent(child, father, as_mother=True)

    def add_mother(self, child, mother):
        self.add_parent(child, mother, as_mother=True)

    def add_his_child(self, person, child):
        self.add_child(person, child, as_mother=False)

    def add_her_child(self, person, child):
        self.add_child(person, child, as_mother=True)
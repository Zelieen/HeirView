from node import Person, Event
from importer import import_file

class Tree:
    def __init__(self): # contains all persons in the family tree in a dictionary, the root person's ID and the ID count in the tree.
        self._ID_count = 0 # should equal next free ID
        self.root_ID = None
        self.persons = {}

    def __str__(self):
        return f"A family tree with {str(self._ID_count)} persons in it."
    
    def __repr__(self):
        return f"Tree()"
    
    def add_person(self, person):
        new_person = person # a Person()
        if new_person._ID == None:
            new_person._ID = self.get_next_free_ID()
        if self._ID_count == 0: # first person in the tree
            self.root_ID = new_person._ID
        self._ID_count += 1
        if new_person._ID in self.persons:
            print("ID is already in use")
            #maybe add information to existing person later
            return            
        self.persons[new_person._ID] = new_person # add person to tree's dictionary
        return self.persons[new_person._ID]

    def find_person(self, ID):
        found = None
        if ID in self.persons:
            found = self.persons[ID]
        return found

    def add_child(self, person, child=-1, as_mother=True):
        if not self.find_person(person):
            print (f"person #{person} not found")
            return
        the_person = self.find_person(person)
        if self.find_person(child):
            the_child = self.find_person(child)
        else: 
            print (f"person #{child} not found")
            return
            #the_child = self.add_person(child) # adding a new person needs a name preferably.
        the_person.children.append(the_child._ID)
        if as_mother:
            the_child.mother = the_person._ID
        else:
            the_child.father = the_person._ID

    def add_parent(self, child, parent=-1, as_mother=True):
        if not self.find_person(child):
            print (f"person #{child} not found")
            return
        the_child = self.find_person(child)
        if self.find_person(parent):
            the_parent = self.find_person(parent)
        else: 
            print (f"person #{parent} not found")
            return
            #the_parent = self.add_person(parent) # adding a new person needs a name preferably.
        the_parent.children.append(the_child._ID)
        if as_mother:
            the_child.mother = the_parent._ID
        else:
            the_child.father = the_parent._ID

    def add_father(self, child, father=-1):
        self.add_parent(child, father, as_mother=False)

    def add_mother(self, child, mother=-1):
        self.add_parent(child, mother, as_mother=True)

    def add_his_child(self, person, child=-1):
        self.add_child(person, child, as_mother=False)

    def add_her_child(self, person, child=-1):
        self.add_child(person, child, as_mother=True)

    def add_partnership(self, person1, person2):
        if not self.find_person(person1):
            print(f"person1 #{person1} not found")
            return
        if not self.find_person(person2):
            print(f"person2 #{person2} not found")
            return
        p1 = self.find_person(person1)
        p2 = self.find_person(person2)

        p1.partners.append(p2._ID)
        p2.partners.append(p1._ID)

    def add_event_to_person(self, person, event):
        if not self.find_person(person):
            print(f"person #{person} not found")
            return
        if not type(event) == type(Event("test", [])):
            print(f"That was not a proper Event()")
            return
        p = self.find_person(person)
        p.events.append(event)

    def add_family(self, family):
        if family.mother and family.father:
            self.add_partnership(family.mother, family.father)
            if family.marr:
                self.add_event_to_person(family.mother, family.marr)
                self.add_event_to_person(family.father, family.marr)
        if len(family.children) > 0:
            for child in family.children:
                if family.mother:
                    self.add_mother(child, family.mother)
                if family.father:
                    self.add_father(child, family.father)

    def get_all_free_IDs(self):
        index_list = sorted(list(self.persons.keys()))
        free_IDs = []
        x = 0 # keep track of position in index_list
        for i in range(index_list[-1]):
            if index_list[x] > i:
                free_IDs.append(i)
            else:
                x += 1
        return free_IDs
    
    def get_next_free_ID(self):
        free_ID = None
        index_list = sorted(list(self.persons.keys()))
        for i in range(len(index_list)):
            if i < index_list[i]:
                free_ID = i
                break

        if not free_ID:
            free_ID = self._ID_count
        return free_ID

    def import_from_file(self, directory):
        persons, families = import_file(directory)

        for person in persons:
            self.add_person(person)
        for family in families:
            self.add_family(family)
        
        print(f"imported {len(persons)} persons and {len(families)} families")
        return

#--------to be done------
    # incomplete function, do not use
    def set_new_ID(self, person, new_ID, force=False): # use with caution: tree performance relies on continuous IDs
        if not self.find_person(person):
            print(f"no such person with #{person} found")
            return
        if self.find_person(new_ID):
            print(f"caution: #{new_ID} is already in use")
            if not force:
                return
            else:
                print(f"was forced to have doubly used IDs! If deleting persons, this is expected to happen in the process.")
        p = self.find_person(person)
        # to be continued
    
    def swap_IDs(self, person1, person2): # incomplete function, do not use
        if not self.find_person(person1):
            print(f"person1 #{person1} not found")
            return
        if not self.find_person(person2):
            print(f"person2 #{person2} not found")
            return
        p1 = self.find_person(person1)
        p2 = self.find_person(person2)

        # swap all relations via set_new_ID, use a temporary ID
        # to be continued
    
    def remove_person(self, person): # incomplete function, do not use
        if not self.find_person(person):
            print(f"no such person with #{person} found")
            return
        to_remove = self.find_person(person)
        
        # remove all relations to other persons
        if to_remove.mother: # remove person from mother's children
            mother = self.find_person(to_remove.mother)
            for child in mother.children:
                if child == to_remove:
                    mother.children.pop(child)
        
        if to_remove.father: # remove person from father's children
            father = self.find_person(to_remove.father)
            for child in father.children:
                if child == to_remove:
                    father.children.pop(child)

        if len(to_remove.children) > 0: # remove person as mother and/or father from its children
            for child in to_remove.children:
                orphan = self.find_person(child)
                if orphan.mother == to_remove:
                    orphan.mother = None
                if orphan.father == to_remove:
                    orphan.father = None

        if len(to_remove.partners) > 0: # remove person as partner from its partners
            for partner in to_remove.partners:
                loner = self.find_person(partner)
                loner.partners.pop(to_remove)

         # part were person needs to be removed from shared events.
        if len(to_remove.events) > 0:
            for event in to_remove.events:
                # go through person_list. For every other person except to_remove: alter (or delete if only other person) this event on the other person as well
                if len(event.persons) > 1:
                    for person in event.persons:
                        other = self.find_person(person)
                        if other != to_remove: # on other person
                            for o_event in other.events: # find event
                                if o_event.type == event.type:
                                    o_event.persons.pop(to_remove) # remove to_remove from other person's event
                                    if len(o_event.persons) == 1: #and o_event.type == "marriage":#
                                        other.events.pop(o_event) # delete event from other person
        # remove person itself from family tree

    ## tidy_up_IDs:
    ## fill unused IDs with the highest IDs, to keep IDs in the tree continuous    
    #replace ID from dictionary self.persons with highest ID person <-- keep ID count continuous and small
    #replace highest ID with removed ID --> keep the internal ID count as low as possible
    #lower self._ID_count by 1

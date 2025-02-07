from node import Person, Event
from importer import import_file
from chart import ChartID

class Tree:
    def __init__(self): # contains all persons in the family tree in a dictionary, the root person's ID and the ID count in the tree.
        self._ID_count = 0 # should equal next free ID
        self.root_ID = None
        self.persons = {} # Person() keyed by their ID

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

    def find_direct_ancestors(self, person_0):
        ancestor_list = []
        ancestor_list.extend(self.find_ancestors_r(person_0, 0))
        return ancestor_list

    def find_ancestors_r(self, child, child_generation):
        ancestors = []
        child_person = self.find_person(child)
        if child_person == None:
            return ancestors
        else:
            next_gen = child_generation + 1
            mother = child_person.mother
            father = child_person.father

            if mother != None:
                ancestors.append(ChartID(mother, next_gen))
                ancestors.extend(self.find_ancestors_r(mother, next_gen))
            if father != None:
                ancestors.append(ChartID(father, next_gen))
                ancestors.extend(self.find_ancestors_r(father, next_gen))

        return ancestors

    def find_direct_descendants(self, ancestor):
        descendant_list = []
        descendant_list.extend(self.find_descendants_r(ancestor, 0))
        self.renumber_generations(descendant_list)
        return descendant_list
        
    def find_descendants_r(self, ancestor, ancestor_generation):
        descendants = []
        parent_person = self.find_person(ancestor)
        if parent_person == None:
            return descendants
        else:
            prev_gen = ancestor_generation - 1
            children_ids = parent_person.children
            if children_ids != []:
                for child_id in children_ids:
                    descendants.append(ChartID(child_id, prev_gen))
                    descendants.extend(self.find_descendants_r(child_id, prev_gen))
        return descendants

    def renumber_generations(self, chart_id_list):
        gen_set = set()
        for chart_id in chart_id_list:
            gen_set.add(chart_id.gen)
        
        lowest_gen = min(list(gen_set))
        highest_gen = max(list(gen_set))
        
        gen_dict = {}
        
        for gen in range(lowest_gen, highest_gen + 1):
            new_gen = gen - lowest_gen
            gen_dict[gen] = new_gen

        for i in range(len(chart_id_list)):
            person_id, old_gen = chart_id_list[i].person_ID, chart_id_list[i].gen
            chart_id_list[i] = ChartID(person_id, gen_dict[old_gen])
        
        return chart_id_list # has been 're-generationed' in place to start at generation 0 until max generation

    def get_ancestors_for_chart(self, start_person, bounces=0):
        persons_chart_list = [ChartID(start_person, 0)]
        persons_chart_list.extend(self.find_direct_ancestors(start_person))

        if bounces > 0:
            # make a list of persons, who did not YET have their children / ancestors checked
            #not yet done: remove double ancestors, if they appear on different generations: keep oldest generation
            person_list = persons_chart_list.copy()
            new_persons = []
            for bounce in range(1, bounces + 1):
                if bounce % 2 != 0: # uneven bounce #
                    #print(f"bouncing down from {person_list}")
                    for chartID in person_list:
                        found_persons = self.find_descendants_r(chartID.person_ID, chartID.gen)
                        new_persons.extend(self.add_to_chart_list(persons_chart_list, found_persons))
                    person_list = new_persons
                    #print(f"new descendants: {new_persons}")
                    new_persons = []
                else: # even bounce #
                    #print(f"bouncing up from {person_list}")
                    for chartID in person_list:
                        found_persons = self.find_ancestors_r(chartID.person_ID, chartID.gen)
                        new_persons.extend(self.add_to_chart_list(persons_chart_list, found_persons))
                    person_list = new_persons
                    #print(f"new ancestors: {new_persons}")
                    new_persons = []
        self.renumber_generations(persons_chart_list)
        print(f"found {len(persons_chart_list)} persons for the chart")
        return persons_chart_list
    
    def add_to_chart_list(self, chart_list, to_add):
        '''
        if there is a duplicate, only keep the highest generation
        '''
        new_persons = []
        for chartID in to_add:
            found = False
            for i in range(len(chart_list)):
                if chartID == chart_list[i]:
                    max_gen = max(chart_list[i].gen, chartID.gen)
                    chart_list[i] = ChartID(chart_list[i].person_ID, max_gen)
                    found = True
                    break
            
            if found == False:
                chart_list.append(chartID)
                new_persons.append(chartID)
        return new_persons



#--------to be done------not necessarily in scope for just reading in gedcom files
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
    
    # incomplete function, do not use
    def swap_IDs(self, person1, person2):
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
    
    # incomplete function, do not use
    def remove_person(self, person):
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

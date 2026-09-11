from node import Person, Event, Family
from importer import import_file
from chart import ChartID, renumber_generations, new_on_chart_list


class Tree:
    """
    Holds a family tree with all persons and their relations.
    
    There is also the root person's ID and the ID count in the tree.
    """

    def __init__(
        self,
    ):
        self._ID_count: int = 0  # should equal next free ID
        self.root_ID: int | None = None
        self.persons: dict[int, Person] = {}  # Person() keyed by their ID

    def __str__(self):
        return f"A family tree with {str(self._ID_count)} persons in it."

    def __repr__(self):
        return f"Tree()"

    def add_person(self, given_name: str = "", surname: str = "", ID: int | None = None) -> Person:
        """Adds a person to the tree."""
        # check ID:
        if ID in self.persons:
            print("ID is already in use for:")
            return self.persons[ID]
        if ID == None:
            ID = self.get_next_free_ID()

        # add person to tree's dictionary
        new_person = Person(ID, given_name, surname)
        self.persons[ID] = new_person

        # check own ID count
        if self._ID_count == 0:  # first person in the tree
            self.root_ID = new_person._ID
        self._ID_count += 1

        return self.persons[ID]

    def find_person(self, ID: int | None) -> Person | None:
        """Returns a person from the tree."""
        return self.persons[ID] if ID in self.persons else None

    def add_child(self, parent: int, child: int, as_mother: bool = True) -> None:
        """Adds a parent-child relation by IDs."""
        the_person = self.find_person(parent)
        if not the_person:
            print(f"person #{parent} not found")
            return
        the_child = self.find_person(child)
        if not the_child:
            print(f"person's child #{child} not found")
            return
            # the_child = self.add_person(child) # adding a new person needs a name preferably.
        the_person.children.append(the_child._ID)
        if as_mother:
            the_child.mother = the_person._ID
        else:
            the_child.father = the_person._ID

    def add_parent(self, child: int, parent: int, as_mother: bool = True) -> None:
        """Adds a parent-child relation by IDs."""
        self.add_child(parent, child, as_mother)

    def add_father(self, child: int, father: int) -> None:
        """Wraps add_parent()."""
        self.add_parent(child, father, as_mother=False)

    def add_mother(self, child: int, mother: int) -> None:
        """Wraps add_parent()."""
        self.add_parent(child, mother, as_mother=True)

    def add_his_child(self, parent: int, child: int) -> None:
        """Wraps add_child()."""
        self.add_child(parent, child, as_mother=False)

    def add_her_child(self, parent: int, child: int) -> None:
        """Wraps add_child()."""
        self.add_child(parent, child, as_mother=True)

    def add_partnership(self, person1: int, person2: int) -> None:
        """Adds a partner relationship by ID."""
        p1 = self.find_person(person1)
        p2 = self.find_person(person2)
        if not p1:
            print(f"person1 #{person1} not found")
            return
        if not p2:
            print(f"person2 #{person2} not found")
            return

        p1.partners.append(p2._ID)
        p2.partners.append(p1._ID)

    def add_event_to_person(self, person: int, event: Event):
        """Adds an event to that person by ID."""
        p = self.find_person(person)
        if not p:
            print(f"person #{person} not found")
            return
        if not isinstance(event, Event):
            print(f"That was not a proper Event()")
            return
        p.events.append(event)

    def add_family(self, family: Family) -> None:
        """Adds all relations from a family to the persons in the tree."""
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

    def get_all_free_IDs(self) -> list[int]:
        """Returns free IDs between lowest and highest ID in the tree."""
        index_list = sorted(list(self.persons.keys()))
        free_IDs = []
        x = 0  # keep track of position in index_list
        for i in range(index_list[-1]):
            if index_list[x] > i:
                free_IDs.append(i)
            else:
                x += 1
        return free_IDs

    def get_next_free_ID(self) -> int:
        """Returns a free ID or the next highest ID."""
        free_ID = None
        index_list = sorted(list(self.persons.keys()))
        for i in range(len(index_list)):
            if i < index_list[i]:
                free_ID = i
                break

        return free_ID if free_ID else self._ID_count

    def fill_from_file(self, directory) -> None:
        """Creates persons and relations from a .gedcom file."""
        file_tuple = import_file(directory)
        if not file_tuple:
            print(f"Could not import from file: {directory}")
            return
        persons, families = file_tuple

        for person in persons:
            self.add_person(person)
        for family in families:
            self.add_family(family)

        print(f"imported {len(persons)} persons and {len(families)} families")

    def find_all_direct_ancestors(self, person_0: int) -> list[ChartID]:
        """Grabs all linked ancestors by ID."""
        ancestors = []
        ancestors.extend(self._find_ancestors_r(person_0, 0))
        return ancestors

    def _find_ancestors_r(self, child: int, child_generation: int) -> list[ChartID]:
        """Grabs ancestors recursively."""
        ancestors = []
        child_person = self.find_person(child)
        if not child_person:
            return ancestors
        else:
            next_gen = child_generation + 1
            mother = child_person.mother
            father = child_person.father

            if mother != None:
                ancestors.append(ChartID(mother, next_gen))
                ancestors.extend(self._find_ancestors_r(mother, next_gen))
            if father != None:
                ancestors.append(ChartID(father, next_gen))
                ancestors.extend(self._find_ancestors_r(father, next_gen))

        return ancestors

    def find_all_direct_descendants(self, ancestor: int) -> list[ChartID]:
        """Grabs all linked descendants by ID."""
        descendants = []
        descendants.extend(self._find_descendants_r(ancestor, 0))
        return descendants

    def _find_descendants_r(self, ancestor: int, ancestor_generation: int) -> list[ChartID]:
        """Grabs descendants recursively."""
        descendants = []
        parent_person = self.find_person(ancestor)
        if parent_person == None:
            return descendants
        else:
            prev_gen = ancestor_generation - 1
            children_ids = parent_person.children
            if children_ids:
                for child_id in children_ids:
                    descendants.append(ChartID(child_id, prev_gen))
                    descendants.extend(self._find_descendants_r(child_id, prev_gen))
        return descendants

    def get_ancestors_for_chart(self, start_person: int = -1, bounces: int = 0) -> list[ChartID]:
        """
        Gets all the ancestors by ID and their generation.

        Bounces decide how distantly related persons are included:
        0 bounces include only parents and direct ancestors
        1 bounce adds all ancestor's descendants: siblings
        2 bounces include also in-laws and their direct ancestors
        """
        if start_person < 0 and self.root_ID != None:
            start_person = self.root_ID
        if start_person not in self.persons:
            return []
        
        persons_chart_list = [ChartID(start_person, 0)]
        persons_chart_list.extend(self.find_all_direct_ancestors(start_person))

        if bounces > 0:
            # make a list of persons, who did not YET have their children / ancestors checked
            person_list = persons_chart_list.copy()
            new_persons = []
            for bounce in range(1, bounces + 1):
                if (
                    person_list == []
                ):  # return right away, no need to bounce any further
                    renumber_generations(persons_chart_list)
                    print(
                        f"found {len(persons_chart_list)} persons for the chart after only {bounce - 1} bounces"
                    )
                    return persons_chart_list
                for chartID in person_list:
                    if bounce % 2 != 0:  # uneven bounce #
                        found_persons = self._find_descendants_r(
                            chartID.person_ID, chartID.gen
                        )
                    else:  # even bounce #
                        found_persons = self._find_ancestors_r(
                            chartID.person_ID, chartID.gen
                        )
                    new_persons.extend(
                        new_on_chart_list(persons_chart_list, found_persons)
                    )  # adds new persons to chart_list and also returns new persons
                person_list = new_persons
                new_persons = []
        renumber_generations(persons_chart_list)
        print(f"found {len(persons_chart_list)} persons for the chart")
        return persons_chart_list

    def get_connections_for_chart(self, list_chartIDs: list[ChartID]) -> list[tuple[int, int | None, int | None]]:
        """Builds connected persons list."""
        connection_list = []
        for chartID in list_chartIDs:
            # find ID as child
            child = self.find_person(chartID.person_ID)
            if child != None:
                # get mother and father ID
                mother_ID = child.mother
                father_ID = child.father
                connection_list.append((child._ID, mother_ID, father_ID))
        print(f"found {len(connection_list)} connections for the chart")
        return connection_list  # list_childID_motherID_fatherID of tuples

    # --------to be done------not necessarily in scope for just reading in gedcom files
    # incomplete function, do not use
    def set_new_ID(
        self, person, new_ID, force=False
    ):  # use with caution: tree performance relies on continuous IDs
        if not self.find_person(person):
            print(f"no such person with #{person} found")
            return
        if self.find_person(new_ID):
            print(f"caution: #{new_ID} is already in use")
            if not force:
                return
            else:
                print(
                    f"was forced to have doubly used IDs! If deleting persons, this is expected to happen in the process."
                )
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
        to_remove = self.find_person(person)
        if not to_remove:
            print(f"no such person with #{person} found")
            return

        # remove all relations to other persons
        if to_remove.mother:  # remove person from mother's children
            mother = self.find_person(to_remove.mother)
            if mother:
                for child in mother.children:
                    if child == to_remove:
                        mother.children.pop(child)

        if to_remove.father:  # remove person from father's children
            father = self.find_person(to_remove.father)
            if father:
                for child in father.children:
                    if child == to_remove:
                        father.children.pop(child)

        if (
            len(to_remove.children) > 0
        ):  # remove person as mother and/or father from its children
            for child in to_remove.children:
                orphan = self.find_person(child)
                if orphan:
                    if orphan.mother == to_remove:
                        orphan.mother = None
                    if orphan.father == to_remove:
                        orphan.father = None

        if len(to_remove.partners) > 0:  # remove person as partner from its partners
            for partner in to_remove.partners:
                loner = self.find_person(partner)
                if loner:
                    loner.partners.pop(to_remove._ID)

        # part were person needs to be removed from shared events.
        if len(to_remove.events) > 0:
            for event in to_remove.events:
                # go through person_list. For every other person except to_remove: alter (or delete if only other person) this event on the other person as well
                if len(event.persons) > 1:
                    for person in event.persons:
                        other = self.find_person(person)
                        if other and other != to_remove:  # on other person
                            for index, o_event in enumerate(other.events):  # find event
                                if o_event.type == event.type:
                                    o_event.persons.pop(
                                        to_remove._ID
                                    )  # remove to_remove from other person's event
                                    if (
                                        len(o_event.persons) == 1
                                    ):  # and o_event.type == "marriage":#
                                        other.events.pop(
                                            index
                                        )  # delete event from other person
        # remove person itself from family tree

    ## tidy_up_IDs:
    ## fill unused IDs with the highest IDs, to keep IDs in the tree continuous
    # replace ID from dictionary self.persons with highest ID person <-- keep ID count continuous and small
    # replace highest ID with removed ID --> keep the internal ID count as low as possible
    # lower self._ID_count by 1

from unit import *

class ChartID:
    def __init__(self, person_ID, generation):
        self.person_ID = person_ID
        self.gen = generation
    
    def __str__(self):
        return f"A ChartID of person # {str(self.person_ID)} at generation {str(self.gen)}."
    
    def __repr__(self):
        return f"ChartID({self.person_ID}, {self.gen})"
    
    def __eq__(self, other):
        return self.person_ID == other.person_ID

class Chart:
    def __init__(self):
        self.badge_col = [] #a list of lists: generation columns of badges
        self.connect_col = [] #a list of lists: columns of connectors between badge columns
        self.pos_x = 0
        self.pos_y = 0

    def inverse_generations(self):
        self.badge_col.reverse()
        self.connect_col.reverse()

    def add_person(self, person, generation):
        badge = self.make_badge(person._ID)
        self.add_badge(badge, generation)

    def add_persons(self, list_person_generation):
        for person, generation in list_person_generation:
            self.add_person(person, generation)

    def sort_ranks(self):
        '''
        sort the badges for 'optimal' order that minimises sibling distance (and then partner distance)
        '''
        pass

    def fill_badges(self):
        '''
        fill the badges with the info from the persons they represent
        '''
        pass

# --- all about badges ---
    def make_badge(self, person_ID):
        new_badge = Badge(person_ID)
        return new_badge

    def add_badge(self, badge, generation, rank=-1):
        if generation < 0:
            return
        if generation < len(self.badge_col):
            if rank in range(len(self.badge_col[generation])):
                self.badge_col[generation].insert(rank, badge)
            else:
                self.badge_col[generation].append(badge)
        else:
            self.badge_col.append([])
            self.badge_col[-1].append(badge)

    def search_badge_place_by_ID(self, ID):
        for c in range(len(self.badge_col)):
            for r in range(len(self.badge_col[c])):
                if self.badge_col[c][r].person_ID == ID:
                    return c, r
        #print("ID not found in chart")
        return False
    
    def find_badge_by_ID(self, ID):
        badge = Badge(None)
        place = self.search_badge_place_by_ID(ID)
        if place != False:
            badge = self.get_badge_by_place(*place)
        return badge
    
    def get_badge_by_place(self, gen, rank):
        return self.badge_col[gen][rank]
    
# --- all about connectors ---    
    def make_connector(self, child_ID, mother_ID, father_ID):
        new_connector = Connector()
        new_connector.to_left.append(child_ID)
        new_connector.to_right.extend([mother_ID, father_ID])
        return new_connector
    
    def add_connection(self, child_ID, mother_ID, father_ID):
        if not self.search_badge_place_by_ID(child_ID):
            return
        child_gen = self.search_badge_place_by_ID(child_ID)[0]
        connector_index = self.search_connector_index(mother_ID, father_ID, child_gen)
        if type(connector_index) == type(False):
            connector = self.make_connector(child_ID, mother_ID, father_ID)
            self.add_new_connector(connector, child_gen)
        else:
            self.add_to_connector_at(child_gen, connector_index, child_ID)

    def add_new_connector(self, connector, child_gen):
        # order does not matter here
        if child_gen < 0:
            return
        if child_gen < len(self.connect_col):
            self.connect_col[child_gen].append(connector)
        else:
            self.connect_col.append([])
            self.connect_col[-1].append(connector)

    def add_to_connector_at(self, child_gen, index, child_ID):
        self.connect_col[child_gen][index].to_left.append(child_ID)
    
    def search_connector_index(self, mother_ID, father_ID, child_gen):
        found_index = False
        if child_gen in range(len(self.connect_col)):
            for i in range(len(self.connect_col[child_gen])):
                connector = self.connect_col[child_gen][i]
                for person_ID in connector.to_right:
                    if person_ID == mother_ID:
                        #found same mother
                        for person_ID in connector.to_right:
                            if person_ID == father_ID:
                                #found same father
                                found_index = i
                                return found_index #and break the loop
        return found_index

# --- all about pixel position ---
    def get_required_size(self):
        pass # for maximum needed space on picture

    def calculate_connector_width(self):
        '''
        set a minimum width
        if # space requirement above: increase width for all per column
        '''
        pass
    
    def calculate_badge_positions(self):
        '''
        first pass: cram them together per column, person 0 as anchor
        second pass: from max # badge column spread other columns out by connectors
        '''
        pass
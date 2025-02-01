from badge import *

class Chart:
    def __init__(self):
        self.badge_col = [] #a list of lists: generation columns of badges
        self.pos_x = 0
        self.pos_y = 0

    def get_required_size(self):
        pass

    def add_badge(self, badge, generation, rank):
        if generation < len(self.badge_col):
            if rank < len(self.badge_col[generation]):
                self.badge_col[generation].insert(rank, badge)
            else:
                self.badge_col[generation].append(badge)
        else:
            self.badge_col.append([]) #fix ambiguity, if generation != last index
            self.badge_col[generation].append(badge)
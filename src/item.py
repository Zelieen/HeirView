class Item:
    def __init__(self):
        self.pos_x = None
        self.pos_y = None
        self.height = 50
        self.width = 50

    def set_position(self, x, y):
        self.pos_x = x
        self.pos_y = y

    def get_position(self):
        return self.pos_x, self.pos_y
    
    def set_size(self, height, width):
        self.height = height
        self.width = width

    def get_size(self):
        return self.height, self.width

class Badge(Item):
    def __init__(self, person_ID):
        super().__init__()
        self.person_ID = person_ID
    
    def get_center(self, side=None):
        if side == "right":
            return self.pos_x + self.width, self.pos_y + self.height // 2
        if side == "left":
            return self.pos_x, self.pos_y + self.height // 2
        if side == "up":
            return self.pos_x + self.width // 2, self.pos_y
        if side == "down":
            return self.pos_x + self.width // 2, self.pos_y + self.height
        else:
            return self.pos_x + self.width // 2, self.pos_y + self.height // 2 #middle

class Connector(Item):
    def __init__(self):
        super().__init__()
        self.left_anchor = None
        self.right_anchor = None
        self.spacer_length = 10

        self.to_left = [] #list of badges
        self.to_right = [] #list of badges

        '''
        Draw connecting lines between the badges in to_left and to_right
        
        - comb for all to_left badges
            - from center of badge ("right") a horizontal spacer
            - connect spacer ends vertically

        - comb for all to_right badges
            - from center of badge ("left") a horizontal spacer
            - connect spacer ends vertically

        - the actual connector line
            - horizontal from middle of to_left spacer ends to left_anchor (>= 0)
            - horizontal from middle of to_right spacer ends to right_anchor (>=0)
            - vertical at left_anchor from  middle of spacer ends to_left and to_right
        '''
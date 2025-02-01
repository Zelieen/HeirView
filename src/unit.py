class Unit:
    def __init__(self):
        self.pos_x = 0
        self.pos_y = 0
        self.height = 0
        self.width = 0

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

class Badge(Unit):
    def __init__(self, person_ID):
        super().__init__()
        self.person_ID = person_ID

        self.set_size(50, 50)
    
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

class Connector(Unit):
    def __init__(self):
        super().__init__()
        self.left_anchor = None
        self.right_anchor = None
        self.spacer_length = 10

        self.to_left = [] #list of IDs (children)
        self.to_right = [] #list of IDs (parents)

        '''
        Draw connecting lines between the badges in to_left and to_right
        
        - 'comb' for all to_left badges
            - from center of badge ("right") a horizontal spacer to the right (+x)
            - connect spacer ends vertically <- cave-at if badges are not in the same generation

        - 'comb' for all to_right badges
            - from center of badge ("left") a horizontal spacer to the left (-x)
            - connect spacer ends vertically <- cave-at if badges are not in the same generation

        - the actual connector line, watch out if any list of to_right or to_left is empty!
            - horizontal from middle of to_left spacer ends to left_anchor (>= 0)
            - horizontal from middle of to_right spacer ends to right_anchor (>=0)
            - vertical at left_anchor from  middle of spacer ends to_left and to_right
        '''
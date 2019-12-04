class Room:
    def __init__(self, building, name, cap, classroom=False, room=False, lab=False):
        # self.id = id
        self.building = building
        self.name = name
        self.cap = cap
        self.classroom = classroom
        self.room = room
        self.lab = lab

class Room:
    def __init__(self, building, name, cap, classroom=False, lab=False, room=False, id=None):
        self.building = building
        self.name = name
        self.cap = cap
        self.classroom = classroom
        self.room = room
        self.lab = lab
        self.id = id
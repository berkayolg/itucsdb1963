class Classroom:
    def __init__(self, id, building, type, availability = True, conditioner = False, board_type = "MIXED"):
        self.id = id
        self.building = building
        self.type = type
        self.availability = availability
        self.conditioner = conditioner
        self.board_type = board_type
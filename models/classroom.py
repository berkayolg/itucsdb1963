class Classroom:
    def __init__(self, id, name, building, type, restoration_date, cap, availability=True, conditioner=False, board_type="MIXED"):
        self.id =id
        self.name = name
        self.building = building
        self.type = type
        self.restoration_date = restoration_date
        self.cap = cap
        self.availability = availability
        self.conditioner = conditioner
        self.board_type = board_type

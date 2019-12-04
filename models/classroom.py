class Classroom:
    def __init__(self, id, building, type, restoration_date, availability=True, conditioner=False, board_type="MIXED"):
        self.id = id
        self.building = building
        self.type = type
        self.restoration_date = restoration_date
        self.availability = availability
        self.conditioner = conditioner
        self.board_type = board_type

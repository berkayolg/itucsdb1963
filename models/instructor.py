class Instructor:
    def __init__(self, name, department, lecture_id, room, lab = None):
        self.name = name
        self.department = department
        self.lecture_id = lecture_id
        self.room = room
        self.lab = lab
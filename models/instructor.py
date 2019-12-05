class Instructor:
    def __init__(self, instructor_id, name, bachelors, masters, doctorates, department, lecture_id, room, lab=None):
        self.bachelors = bachelors
        self.masters = masters
        self.doctorates = doctorates
        self.instructor_id = instructor_id
        self.name = name
        self.department = department
        self.lecture_id = lecture_id
        self.room = room
        self.lab = lab

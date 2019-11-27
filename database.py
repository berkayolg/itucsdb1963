from instructor import Instructor

class Database:

    def __init__(self):
        self.instructors = {}
        self._last_inst_key = 0

    def add_instructor(self, instructor):
        self._last_inst_key += 1
        self.instructors[self._last_inst_key] = instructor
        return self._last_inst_key

    def delete_instructor(self, instructor_key):
        if instructor_key in self.instructors:
            del self.instructors[instructor_key]

    def get_instructor(self, instructor_key):
        instructor = self.instructors.get(instructor_key)
        if instructor is None:
            return None
        instructor_ = Instructor(instructor.name, instructor.department, instructor.lecture_id, instructor.room, instructor.lab)
        return instructor_
        
    def get_instructors(self):
        instructors = []
        for instructor_key, instructor in self.instructors.items():
            instructor_ = Instructor(instructor.name, instructor.department, instructor.lecture_id, instructor.room, instructor.lab)
            instructors.append((instructor_key, instructor_))
        return instructors
import os
import sys
import copy

import psycopg2 as dbapi2

from models.room import Room
from models.classroom import Classroom
from models.instructor import Instructor
from models.student import Student
from models.people import People


class Database:

    def __init__(self):
        self.rooms = {}
        self.classrooms = {}
        self.instructors = {}
        self.students = {}
        self.people = {}

        self._last_room_key = 0
        self._last_classroom_key = 0
        self._last_inst_key = 0
        self._last_stu_key = 0
        self._last_people_key = 0

        self.url = os.getenv("DATABASE_URL")
        if not self.url:
            self.url = "postgres://iaksomyxyzootw:d9a1a786933ba99327d701e93ac741a5242fa801abf686cfce029df4fa887f68@ec2-54-225-115-177.compute-1.amazonaws.com:5432/daq4rhn32jb4v7"

    ############# ROOMS ###############

    def add_room(self, room):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "INSERT INTO ROOMS (BUILDING, ROOM_NAME, CAP, CLASS, LAB, ROOM) VALUES (%s, %s, %s, %s, %s, %s)"
                data = [room.building, room.name, room.cap, room.classroom, room.lab, room.room]
                cursor.execute(statement, data)
                cursor.close()
        except Exception as err:
            print("Error while adding room: ", err)
        return room

    def delete_room(self, room_key):
        if room_key in self.rooms:
            del self.rooms[room_key]

    def get_room(self, room_key):
        room = self.rooms.get(room_key)
        if room is None:
            return None
        room_ = Room(room.building, room.name, room.cap, room.classroom, room.room, room.lab)
        return room_

    def get_rooms(self):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT * FROM ROOMS"
                cursor.execute(statement)
                datas = cursor.fetchall()
                cursor.close()
                return datas
        except Exception as err:
            print("DB Error while getting rooms: ", err)

        return None

    ############# CLASSROOMS ###############

    def add_classroom(self, classroom):
        self._last_classroom_key += 1
        self.classrooms[self._last_classroom_key] = classroom
        return self._last_classroom_key

    def delete_classroom(self, classroom_key):
        if classroom_key in self.classrooms:
            del self.classrooms[classroom_key]

    def get_classroom(self, classroom_key):
        classroom = self.classrooms.get(classroom_key)
        if classroom is None:
            return None
        classroom_ = Classroom(classroom.id, classroom.building, classroom.type, classroom.restoration_date,
                               classroom.availability, classroom.conditioner, classroom.board_type)
        return classroom_

    def get_classrooms(self):
        classrooms = []
        for classroom_key, classroom in self.classrooms.items():
            classroom_ = Classroom(classroom.id, classroom.building, classroom.type, classroom.restoration_date,
                                   classroom.availability, classroom.conditioner, classroom.board_type)
            classrooms.append((classroom_key, classroom_))
        return classrooms

    ############# INSTRUCTORS ###############

    def add_instructor(self, instructor):
        person_obj = People(instructor.name)
        person = self.add_person(person_obj)

        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()

                statement = "INSERT INTO INSTRUCTORS (INS_ID, BACHELORS, MASTERS, DOCTORATES, DEPARTMENT, ROOM, LAB) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                data = [person.id, instructor.bachelors, instructor.masters, instructor.doctorates, instructor.department, instructor.room, instructor.lab]
                cursor.execute(statement, data)
                cursor.close()
        except Exception as err:
            print("Error while adding instructor: ", err)
        return instructor

    def delete_instructor(self, instructor_key):
        if instructor_key in self.instructors:
            del self.instructors[instructor_key]

    def get_instructor(self, instructor_key):
        instructor = self.instructors.get(instructor_key)
        if instructor is None:
            return None
        instructor_ = Instructor(instructor.name, instructor.department, instructor.lecture_id, instructor.room,
                                 instructor.lab)
        return instructor_

    def get_instructors(self):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT * FROM INSTRUCTORS"
                cursor.execute(statement)
                datas = cursor.fetchall()
                cursor.close()
                return datas
        except Exception as err:
            print("DB Error while getting instructors: ", err)

        return None

    ############# PEOPLE   ###############

    def add_person(self, person):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "INSERT INTO PEOPLE (NAME, EMAIL, PHOTO, PASSWORD) VALUES (%s, %s, %s, %s)"
                data = [person.name, person.mail, person.photo, person.password]
                cursor.execute(statement, data)
                print(data)
                statement = "SELECT P_ID FROM PEOPLE WHERE EMAIL = %s"
                data = [person.mail]
                cursor.execute(statement, data)
                value = cursor.fetchall()
                person.id = value[0]
                cursor.close()
        except Exception as err:
            print("Error while adding person: ", err)

        return person

    def get_person(self, p_id):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT * FROM PEOPLE WHERE P_ID = %s"
                data = [p_id]
                cursor.execute(statement, data)
                value = cursor.fetchone()
                cursor.close()
                if not value:
                    return None
                person = People(value[0], value[1], value[2], value[3])
                return person
        except Exception as err:
            print("Error: ", err)

        return None

    def get_person_by_mail(self, mail):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT * FROM PEOPLE WHERE EMAIL = %s"
                data = [mail]
                cursor.execute(statement, data)
                value = cursor.fetchone()
                cursor.close()
                if not value:
                    return None
                person = People(value[0], value[1], value[2], value[3], value[4])
                return person
        except Exception as err:
            print("Error while getting person: ", err)

        return None


    def get_people(self):
        if not len(self.people):
            try:
                with dbapi2.connect(self.url) as connection:
                    cursor = connection.cursor()
                    statement = "SELECT * FROM PEOPLE"
                    cursor.execute(statement)
                    datas = cursor.fetchall()
                    return datas
                    cursor.close()
            except Exception as err:
                print("Error while getting people: ", err)

        return None

    ############# STUDENTS ###############

    def add_student(self, student):
        person_obj = People(student.name)
        person = self.add_person(person_obj)

        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()

                statement = "INSERT INTO STUDENTS (STU_ID, NUMBER, EARNED_CREDITS, DEPARTMENT, FACULTY, CLUB, LAB) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                data = [person.id, student.number, student.cred, student.depart, student.facu, student.club,
                        student.lab]
                cursor.execute(statement, data)
                cursor.close()
        except Exception as err:
            print("Error: ", err)

    def get_student(self, stu_id):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT * FROM STUDENTS WHERE STU_ID = %s"
                data = [stu_id]
                print(data)
                cursor.execute(statement, data)
                datas = cursor.fetchall()
                cursor.close()
                return datas
        except Exception as err:
            print("DB Error: ", err)

        return None

    def get_students(self):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT * FROM STUDENTS JOIN PEOPLE ON (STUDENTS.STU_ID = PEOPLE.P_ID)"
                cursor.execute(statement)
                datas = cursor.fetchall()
                cursor.close()
                retval = []
                for data in datas:
                    val = {
                        "Name": data[8],
                        "Number": data[1]
                    }
                    retval.append(val)
                return retval
        except Exception as err:
            print("DB Error: ", err)

        return None

    def delete_student(self, student_key):
        student = self.students.get(student_key)
        if student:
            try:
                with dbapi2.connect(self.url) as connection:
                    cursor = connection.cursor()
                    statement = "DELETE FROM STUDENTS WHERE number = %s"
                    values = [student.number]
                    cursor.execute(statement, values)
                    cursor.close()
            except Exception as err:
                print("Error: ", err)

    def update_student(self, student_key, attrs, values):
        student = self.students.get(student_key)
        attrs_lookup_table = {
            "id": "STU_ID",
            "number": "NUMBER",
            "cred": "EARNED_CREDITS",
            "depart": "DEPARTMENT",
            "facu": "FACULTY",
            "club": "CLUB",
            "lab": "LAB"
        }
        if student:
            try:
                with dbapi2.connect(self.url) as connection:
                    cursor = connection.cursor()
                    statement = "UPDATE STUDENTS SET "
                    for attr in attrs:
                        statement += attrs_lookup_table[attr] + " = %s "
                    statement += " WHERE number = %s"
                    values.append(student.number)
                    cursor.execute(statement, values)
                    cursor.close()
                    del self.students[student_key]
            except Exception as err:
                print("Error: ", err)

    ############# FACULTIES ###############

    # Create
    def add_faculty(self, faculty):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                data = [faculty.name, faculty.building, faculty.dean, faculty.assistant_dean_1]
                if faculty.assistant_dean_2 is not None:
                    data.append(faculty.assistant_dean_2)
                    statement = "INSERT INTO FACULTIES (FAC_NAME, FAC_BUILDING, DEAN, DEAN_ASST_1, DEAN_ASST_2) VALUES (%s, %s, %s, %s, %s)"
                    cursor.execute(statement, data)
                else:
                    statement = "INSERT INTO FACULTIES (FAC_NAME, FAC_BUILDING, DEAN, DEAN_ASST_1) VALUES (%s, %s, %s, %s)"
                    cursor.execute(statement, data)
                cursor.close()
        except Exception as err:
            print("Error: ", err)

    # Read
    def get_faculty(self, fac_id):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT * FROM FACULTIES WHERE FAC_ID = %s"
                data = [fac_id]
                print(data)
                cursor.execute(statement, data)
                datas = cursor.fetchall()
                cursor.close()
                return datas
        except Exception as err:
            print("DB Error: ", err)

        return None

    # Delete
    def delete_faculty(self, fac_id):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "DELETE FROM FACULTIES WHERE fac_id = %s"
                values = [fac_id]
                cursor.execute(statement, values)
                cursor.close()
        except Exception as err:
            print("Error: ", err)

    # Update
    def update_faculty(self, fac_id, attrs, values):
        attrs_lookup_table = {
            "name": "FAC_NAME",
            "cred": "FAC_BUILDING",
            "dean": "DEAN",
            "vdean_1": "DEAN_ASST_1",
            "vdean_2": "DEAN_ASST_2",
        }

        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "UPDATE FACULTIES SET "
                for i in range(len(attrs) - 1):
                    statement += attrs_lookup_table[attrs[i]] + " = %s ,"
                statement += attrs_lookup_table[attrs[-1]] + " = %s WHERE FAC_ID = %s"
                values.append(fac_id)
                cursor.execute(statement, values)
                cursor.close()

        except Exception as err:
            print("Error: ", err)

    ############# ASSISTANTS ###############

    ############# LABS ###############

    # Create
    def add_lab(self, lab):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                data = [lab.name, lab.department, lab.faculty, lab.building, lab.room, lab.investigator]
                statement = "INSERT INTO LABS (LAB_NAME, DEPARTMENT, FACULTY, BUILDING, ROOM, INVESTIGATOR) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(statement, data)
                cursor.close()
        except Exception as err:
            print("Error: ", err)

    # Read
    def get_lab(self, lab_id):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT * FROM LABS WHERE LAB_ID = %s"
                data = [lab_id]
                print(data)
                cursor.execute(statement, data)
                datas = cursor.fetchall()
                cursor.close()
                return datas
        except Exception as err:
            print("DB Error: ", err)

        return None

    # Delete
    def delete_lab(self, lab_id):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "DELETE FROM LABS WHERE lab_id = %s"
                values = [lab_id]
                cursor.execute(statement, values)
                cursor.close()
        except Exception as err:
            print("Error: ", err)

    # Update
    def update_faculty(self, lab_id, attrs, values):
        attrs_lookup_table = {
            "name": "LAB_NAME",
            "department": "DEPARTMENT",
            "faculty": "FACULTY",
            "building": "BUILDING",
            "room": "ROOM",
            "investigator": "INVESTIGATOR"
        }

        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "UPDATE LABS SET "
                for i in range(len(attrs) - 1):
                    statement += attrs_lookup_table[attrs[i]] + " = %s ,"
                statement += attrs_lookup_table[attrs[-1]] + " = %s WHERE LAB_ID = %s"
                values.append(lab_id)
                cursor.execute(statement, values)
                cursor.close()

        except Exception as err:
            print("Error: ", err)

    ############# DEPARTMENTS ###############

    # Create
    def add_department(self, department):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                data = [department.name, department.faculty, department.building, department.dean]
                statement = "INSERT INTO DEPARTMENTS (DEP_NAME, FACULTY, BUILDING, DEAN) VALUES (%s, %s, %s, %s)"
                cursor.execute(statement, data)
                cursor.close()
        except Exception as err:
            print("Error: ", err)

    # Read
    def get_department(self, dep_id):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT * FROM DEPARTMENTS WHERE DEP_ID = %s"
                data = [dep_id]
                print(data)
                cursor.execute(statement, data)
                datas = cursor.fetchall()
                cursor.close()
                return datas
        except Exception as err:
            print("DB Error: ", err)

        return None

    # Delete
    def delete_department(self, dep_id):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "DELETE FROM DEPARTMENTS WHERE dep_id = %s"
                values = [dep_id]
                cursor.execute(statement, values)
                cursor.close()
        except Exception as err:
            print("Error: ", err)

    # Update
    def update_department(self, dep_id, attrs, values):
        attrs_lookup_table = {
            "name": "LAB_NAME",
            "faculty": "DEPARTMENT",
            "building": "FACULTY",
            "dean": "BUILDING"
        }

        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "UPDATE DEPARTMENTS SET "
                for i in range(len(attrs) - 1):
                    statement += attrs_lookup_table[attrs[i]] + " = %s ,"
                statement += attrs_lookup_table[attrs[-1]] + " = %s WHERE DEP_ID = %s"
                values.append(dep_id)
                cursor.execute(statement, values)
                cursor.close()

        except Exception as err:
            print("Error: ", err)

    ############# PAPERS ###############

    ############# BUILDINGS ###############

    ############# CLUBS ###############

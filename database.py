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
        self.students = {}
        self.people = {}

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
                statement = "INSERT INTO ROOMS (BUILDING, ROOM_NAME, AVAILABLE, CLASS, LAB, ROOM) VALUES (%s, %s, %s, %s, %s, %s)"
                data = [room.building, room.name, room.availability, room.classroom, room.lab, room.room]
                cursor.execute(statement, data)
                statement = "SELECT ROOM_ID FROM ROOMS WHERE ROOM_NAME = %s"
                data = [room.name]
                cursor.execute(statement, data)
                value = cursor.fetchall()
                room.id = value[0]
                cursor.close()
        except Exception as err:
            print("Add Room Error: ", err)
        return room

    def get_room(self, room_id):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT ROOM_ID, BUILDING, ROOM_NAME, CLASS, LAB, ROOM, AVAILABLE FROM ROOMS WHERE room_id = %s"
                data = [room_id]
                cursor.execute(statement, data)
                value = cursor.fetchone()
                cursor.close()
                if not value:
                    return None
                room = Room(value[1], value[2], value[6], value[3], value[4], value[5], value[0])
                return room
        except Exception as err:
            print("Get Room Error: ", err)

        return None

    def get_rooms(self):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT ROOM_ID, BU_NAME, ROOM_NAME FROM ROOMS JOIN BUILDINGS ON(ROOMS.BUILDING = BUILDINGS.BU_ID)"
                cursor.execute(statement)
                datas = cursor.fetchall()
                cursor.close()
                retval = []
                for data in datas:
                    val = {
                        "ID": data[0],
                        "Name": data[2],
                        "Building": data[1]  
                    }
                    retval.append(val)
                return retval
        except Exception as err:
            print("Get Rooms Error: ", err)

        return None

    def delete_room(self, room_id):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "DELETE FROM ROOMS WHERE room_id = %s"
                values = [room_id]
                cursor.execute(statement, values)
                cursor.close()
        except Exception as err:
            print("Delete Room Error: ", err)

    def update_rooms(self, room_id, attrs, values):
        attrs_lookup_table = {
            "building": "BUILDING",
            "room_name": "ROOM_NAME",
            "cap": "CAP",
            "class": "CLASS",
            "lab": "LAB",
            "room": "ROOM",
            "available":"AVAILABLE"
        }

        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "UPDATE ROOMS SET "
                for i in range(len(attrs) - 1):
                    statement += attrs_lookup_table[attrs[i]] + " = %s ,"
                statement += attrs_lookup_table[attrs[-1]] + " = %s WHERE ROOM_ID = %s"
                values.append(room_id)
                cursor.execute(statement, values)
                cursor.close()

        except Exception as err:
            print("Update Rooms Error: ", err)

    ############# CLASSROOMS ###############

    def add_classroom(self, classroom):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "INSERT INTO CLASSES (CL_ID, TYPE, AIR_CONDITIONER, LAST_RESTORATION, BOARD_TYPE, CAP) VALUES (%s, %s, %s, %s, %s, %s)"
                data = [classroom.id, classroom.type, classroom.conditioner, classroom.restoration_date, classroom.board_type, classroom.cap]
                cursor.execute(statement, data)
                cursor.close()
        except Exception as err:
            print("Add Classroom Error: ", err)
        return classroom

    def delete_classroom(self, cl_id):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "DELETE FROM CLASSES WHERE CL_ID = %s"
                values = [cl_id]
                cursor.execute(statement, values)
                cursor.close()
        except Exception as err:
            print("Delete Classroom Error: ", err)

    def get_classroom(self, cl_id):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT CL_ID, TYPE, AIR_CONDITIONER, LAST_RESTORATION, BOARD_TPE, CAP FROM CLASSSES WHERE cl_id = %s"
                data = [cl_id]
                cursor.execute(statement, data)
                value = cursor.fetchone()
                statement = "SELECT ROOM_NAME, BUILDING, AVAILABLE FROM ROOMS WHERE ROOM_ID = %s"
                data = [cl_id]
                cursor.execute(statement, data)
                room_attrs = cursor.fetchone()
                cursor.close()
                if not value:
                    return None
                classroom = Classroom(value[0], room_attrs[0], room_attrs[1], value[1], value[3], value[5], room_attrs[3], value[2], value[4])
                return classroom
        except Exception as err:
            print("Get Classroom Error: ", err)

        return None

    def get_classrooms(self):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT CLASSES.CL_ID, ROOMS.ROOM_NAME, CLASSES.CAP, CLASSES.TYPE, BUILDINGS.BU_NAME FROM CLASSES JOIN ROOMS ON CL_ID = ROOM_ID JOIN BUILDINGS ON BUILDINGS.BU_ID = ROOMS.BUILDING"
                cursor.execute(statement)
                datas = cursor.fetchall()
                cursor.close()
                retval = []
                for data in datas:
                    val = {
                        "ID":data[0],
                        "Name": data[1],
                        "Capacity": data[2],
                        "Class Type": data[3],
                        "Building Name": data[4],
                    }
                    retval.append(val)
                return retval
        except Exception as err:
            print("Get Classrooms Error: ", err)

        return None

    ############# INSTRUCTORS ###############

    def add_instructor(self, instructor):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "INSERT INTO INSTRUCTORS (INS_ID, BACHELORS, MASTERS, DOCTORATES, DEPARTMENT, ROOM, LAB) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                data = [instructor.instructor_id, instructor.bachelors, instructor.masters, instructor.doctorates,
                        instructor.department, instructor.room, instructor.lab]
                cursor.execute(statement, data)
                cursor.close()
        except Exception as err:
            print("Add Instructor Error: ", err)
        return instructor

    def get_instructor(self, ins_id):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT NAME, BACHELORS,MASTERS, DOCTORATES, DEPARTMENT, ROOM, LAB FROM INSTRUCTORS JOIN PEOPLE ON INS_ID = P_ID WHERE INS_ID = %s"
                data = [ins_id]
                cursor.execute(statement, data)
                value = cursor.fetchone()
                cursor.close()
                if not value:
                    return None
                instructor = Instructor(ins_id, value[0], value[1], value[2], value[3], value[4], value[5], value[6])
                return instructor
        except Exception as err:
            print("Get Instructor Error: ", err)

        return None

    def get_instructors(self):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT P_ID, NAME, ROOM, LAB, BACHELORS, MASTERS, DOCTORATES FROM INSTRUCTORS JOIN PEOPLE ON (INSTRUCTORS.INS_ID = PEOPLE.P_ID)"
                cursor.execute(statement)
                datas = cursor.fetchall()
                cursor.close()
                retval = []
                for data in datas:
                    val = {
                        "ID":data[0],
                        "Name": data[1],
                        "Room": data[2],
                        "Lab": data[3],
                        "Bachelors": data[4],
                        "Masters": data[5],
                        "Doctorates": data[6]
                    }
                    retval.append(val)
                return retval
        except Exception as err:
            print("Get Instructors Error: ", err)

        return None

    def delete_instructor(self, ins_id):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "DELETE FROM INSTRUCTORS WHERE INS_ID = %s"
                values = [ins_id]
                cursor.execute(statement, values)
                cursor.close()
        except Exception as err:
            print("Delete Instructor Error: ", err)

    def update_instructor(self, ins_id, attrs, values):
        attrs_lookup_table = {
            "department": "DEPARTMENT",
            "room": "ROOM",
            "lab": "LAB",
            "bachelors": "BACHELORS",
            "masters": "MASTERS",
            "doctorates": "DOCTORATES"
        }

        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "UPDATE INSTRUCTORS SET "
                for i in range(len(attrs) - 1):
                    print(attrs_lookup_table[attrs[i]] + " = %s ,")
                    statement += attrs_lookup_table[attrs[i]] + " = %s ,"
                statement += attrs_lookup_table[attrs[-1]] + " = %s WHERE INS_ID = %s"
                values.append(ins_id)
                cursor.execute(statement, values)
                cursor.close()

        except Exception as err:
            print("Update Instructors Error: ", err)

    ############# PEOPLE   ###############

    def add_person(self, person):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "INSERT INTO PEOPLE (NAME, EMAIL, PHOTO, PASSWORD, TYPE) VALUES (%s, %s, %s, %s, %s)"
                data = [person.name, person.mail, person.photo, person.password, person.type]
                cursor.execute(statement, data)
                statement = "SELECT P_ID FROM PEOPLE WHERE EMAIL = %s"
                data = [person.mail]
                cursor.execute(statement, data)
                value = cursor.fetchone()
                person.id = value[0]
                cursor.close()
        except Exception as err:
            print("Add Person Error : ", err)

        return person

    def person_exists(self, person):
        return self.get_person_by_mail(person.mail)

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
                person = People(value[1], value[0], value[2], value[3], value[4], value[5])
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
        person = self.add_person(student.get_person_obj())

        print(person.id, " PERSON.ID ")

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
                        "ID": data[0],
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
            print("Add faculty Error: ", err)

    # Read
    def get_faculty(self, fac_id):
        """
        Gets faculty id as an input, returns query results.
        By: Uğur Ali Kaplan"""
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
            print("Get Faculty DB Error: ", err)

        return None

    def get_faculties(self):
        """
        Joins faculty and buildings table, returns relevant columns as a dictionary.
        :return: 
        
        By: Uğur Ali Kaplan
        """
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT * FROM faculties INNER JOIN buildings ON faculties.fac_id = bu_id"
                cursor.execute(statement)
                data = cursor.fetchall()
                cursor.close()
                retval = []
                for datum in data:
                    val = {
                        "ID": datum[0],
                        "Name": datum[1],
                        "Building Name": datum[4],
                        "Building Code": datum[5]
                    }
                    retval.append(val)
                return retval
        except Exception as err:
            print("Get Faculties DB Error: ", err)


    # Delete
    def delete_faculty(self, fac_id):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "DELETE FROM FACULTIES WHERE FAC_ID = %s"
                values = [fac_id]
                cursor.execute(statement, values)
                cursor.close()
        except Exception as err:
            print("Delete Faculty Error: ", err)

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
            print("Update Faculty Error: ", err)

    def get_all_faculties(self):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT * FROM FACULTIES"
                cursor.execute(statement)
                data = cursor.fetchall()
                cursor.close()
                return data

        except Exception as err:
            print("Fetch Faculties Error: ", err)

        return None


    ############# ASSISTANTS ###############

    def add_assistant(self, assistant):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                data = [assistant.person, assistant.lab, assistant.degree, assistant.department, assistant.faculty]
                statement = "INSERT INTO ASSISTANTS (AS_PERSON, LAB, DEGREE, DEPARTMENT, FACULTY) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(statement, data)
                cursor.close()
        except Exception as err:
            print("Add assistant Error: ", err)

    def get_assistant(self, as_id):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT * FROM ASSISTANTS WHERE AS_ID = %s"
                data = [as_id]
                print(data)
                cursor.execute(statement, data)
                datas = cursor.fetchall()
                cursor.close()
                return datas
        except Exception as err:
            print("Get assistant DB Error: ", err)

        return None

    def delete_assistant(self, as_id):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "DELETE FROM ASSISTANTS WHERE AS_ID = %s"
                values = [as_id]
                cursor.execute(statement, values)
                cursor.close()
        except Exception as err:
            print("Delete assistant Error: ", err)

    def update_lab(self, lab_id, attrs, values):
        attrs_lookup_table = {
            "person": "AS_PERSON",
            "lab": "LAB",
            "degree": "DEGREE",
            "department": "DEPARTMENT",
            "faculty": "FACULTY",
        }

        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "UPDATE ASSISTANTS SET "
                for i in range(len(attrs) - 1):
                    statement += attrs_lookup_table[attrs[i]] + " = %s ,"
                statement += attrs_lookup_table[attrs[-1]] + " = %s WHERE AS_ID = %s"
                values.append(lab_id)
                cursor.execute(statement, values)
                cursor.close()

        except Exception as err:
            print("Update assistant Error: ", err)

    ############# LABS ###############

    def add_lab(self, lab):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                data = [lab.name, lab.department, lab.faculty, lab.building, lab.room, lab.investigator]
                statement = "INSERT INTO LABS (LAB_NAME, DEPARTMENT, FACULTY, BUILDING, ROOM, INVESTIGATOR) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(statement, data)
                cursor.close()
        except Exception as err:
            print("Add lab Error: ", err)

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
            print("Get Lab DB Error: ", err)

        return None

    def delete_lab(self, lab_id):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "DELETE FROM LABS WHERE LAB_ID = %s"
                values = [lab_id]
                cursor.execute(statement, values)
                cursor.close()
        except Exception as err:
            print("Delete lab Error: ", err)

    def update_lab(self, lab_id, attrs, values):
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
            print("Update lab Error: ", err)

    def get_all_labs(self):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT * FROM LABS"
                cursor.execute(statement)
                data = cursor.fetchall()
                cursor.close()
                return data
        except Exception as err:
            print("Delete lab Error: ", err)

        return None

    ############# DEPARTMENTS ###############

    def add_department(self, department):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                data = [department.name, department.faculty, department.building, department.dean]
                statement = "INSERT INTO DEPARTMENTS (DEP_NAME, FACULTY, BUILDING, DEAN) VALUES (%s, %s, %s, %s)"
                cursor.execute(statement, data)
                cursor.close()
        except Exception as err:
            print(" Add department Error: ", err)

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
            print("Get department DB Error: ", err)

        return None

    def delete_department(self, dep_id):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "DELETE FROM DEPARTMENTS WHERE DEP_ID = %s"
                values = [dep_id]
                cursor.execute(statement, values)
                cursor.close()
        except Exception as err:
            print("Delete Department Error: ", err)

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
            print("Update Department Error: ", err)

    def get_all_departments(self):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT * FROM DEPARTMENTS"
                cursor.execute(statement)
                data = cursor.fetchall()
                cursor.close()
                return data
        except Exception as err:
            print("Fetching Departments Error: ", err)

        return None

    def get_departments_text(self):
        """

        :return: Information as dictionary.
        """
        data = []
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT * FROM departments INNER JOIN faculties ON departments.faculty = faculties.fac_id INNER JOIN buildings ON departments.building = buildings.bu_id INNER JOIN people ON departments.dean = people.p_id"
                cursor.execute(statement)
                data = cursor.fetchall()
                cursor.close()
                retval = []
                for datum in data:
                    val = {
                        "ID": datum[0],
                        "Name": datum[1],
                        "Faculty": datum[6],
                        "Building": datum[9],
                        "Dean": datum[12]
                    }
                    retval.append(val)
                return retval
        except Exception as err:
            print("Get Departments(All Text) DB Error: ", err)

    ############# PAPERS ###############

    def add_paper(self, paper):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                data = [paper.title, paper.platform, paper.citation, paper.author, paper.isConference]
                statement = "INSERT INTO PAPERS (TITLE, PLAT, CITATION_COUNT, AUTHOR, CONFERENCE) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(statement, data)
                cursor.close()
        except Exception as err:
            print("Add Paper Error: ", err)

    def get_paper(self, paper_id):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT * FROM PAPERS WHERE PAPER_ID = %s"
                data = [paper_id]
                print(data)
                cursor.execute(statement, data)
                datas = cursor.fetchall()
                cursor.close()
                return datas
        except Exception as err:
            print("Get paper DB Error: ", err)

        return None

    def delete_paper(self, paper_id):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "DELETE FROM PAPERS WHERE PAPER_ID = %s"
                values = [paper_id]
                cursor.execute(statement, values)
                cursor.close()
        except Exception as err:
            print("Delete paper error: ", err)

    def update_paper(self, paper_id, attrs, values):
        attrs_lookup_table = {
            "title": "TITLE",
            "platform": "PLAT",
            "citation": "CITATION_COUNT",
            "author": "AUTHOR",
            "isConference": "CONFERENCE"
        }

        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "UPDATE PAPERS SET "
                for i in range(len(attrs) - 1):
                    statement += attrs_lookup_table[attrs[i]] + " = %s ,"
                statement += attrs_lookup_table[attrs[-1]] + " = %s WHERE PAPER_ID = %s"
                values.append(paper_id)
                cursor.execute(statement, values)
                cursor.close()

        except Exception as err:
            print("Update Paper Error: ", err)

    ############# BUILDINGS ###############

    def add_building(self, building):
        """

        :param building: A building object
        :return:
        """
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                data = [building.name, building.code, building.campus]
                statement = "INSERT INTO BUILDINGS (BU_NAME, BU_CODE, CAMPUS) VALUES (%s, %s, %s)"
                cursor.execute(statement, data)
                cursor.close()
        except Exception as err:
            print("Add Building Error: ", err)

    def get_building(self, bu_id):
        """

        :param bu_id: ID of the building in the database
        :return:
        """
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT * FROM BUILDINGS WHERE BU_ID = %s"
                data = [bu_id]
                print(data)
                cursor.execute(statement, data)
                datas = cursor.fetchall()
                cursor.close()
                return datas
        except Exception as err:
            print("Get building DB Error: ", err)

        return None

    def get_buildings(self):
        """

        :return: Information as dictionary.
        """
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT * FROM buildings"
                cursor.execute(statement)
                data = cursor.fetchall()
                cursor.close()
                retval = []
                for datum in data:
                    val = {
                        "ID": datum[0],
                        "Name": datum[1],
                        "Code": datum[2]
                    }
                    retval.append(val)
                return retval
        except Exception as err:
            print("Get Faculties DB Error: ", err)

    def delete_building(self, bu_id):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "DELETE FROM BUILDINGS WHERE BU_ID = %s"
                values = [bu_id]
                cursor.execute(statement, values)
                cursor.close()
        except Exception as err:
            print("Delete building error: ", err)

    def update_building(self, bu_id, attrs, values):
        attrs_lookup_table = {
            "name": "BU_NAME",
            "code": "BU_CODE",
            "campus": "CAMPUS"
        }

        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "UPDATE BUILDINGS SET "
                for i in range(len(attrs) - 1):
                    statement += attrs_lookup_table[attrs[i]] + " = %s ,"
                statement += attrs_lookup_table[attrs[-1]] + " = %s WHERE BU_ID = %s"
                values.append(bu_id)
                cursor.execute(statement, values)
                cursor.close()

        except Exception as err:
            print("Update Department Error: ", err)

    ############# CLUBS ###############

    def add_club(self, club):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                data = [club.name, club.faculty, club.advisor, club.chairman, club.vice_1, club.vice_2]
                statement = "INSERT INTO CLUBS (NAME, FACULTY, ADVISOR, CHAIRMAN, V_CHAIRMAN_1, V_CHAIRMAN_2) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(statement, data)
                cursor.close()
        except Exception as err:
            print("Add Club Error: ", err)

    def get_club(self, club_id):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT * FROM CLUBS WHERE CLUB_ID = %s"
                data = [club_id]
                print(data)
                cursor.execute(statement, data)
                datas = cursor.fetchall()
                cursor.close()
                return datas
        except Exception as err:
            print("Get club DB Error: ", err)

        return None

    def delete_club(self, club_id):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "DELETE FROM CLUBS WHERE CLUB_ID = %s"
                values = [club_id]
                cursor.execute(statement, values)
                cursor.close()
        except Exception as err:
            print("Delete club error: ", err)

    def update_club(self, club_id, attrs, values):
        attrs_lookup_table = {
            "name": "NAME",
            "faculty": "FACULTY",
            "advisor": "ADVISOR",
            "chairman": "CHAIRMAN",
            "vice_1": "V_CHAIRMAN_1",
            "vice_2": "V_CHAIRMAN_2"
        }

        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "UPDATE CLUBS SET "
                for i in range(len(attrs) - 1):
                    statement += attrs_lookup_table[attrs[i]] + " = %s ,"
                statement += attrs_lookup_table[attrs[-1]] + " = %s WHERE CLUB_ID = %s"
                values.append(club_id)
                cursor.execute(statement, values)
                cursor.close()

        except Exception as err:
            print("Update Club Error: ", err)

    def get_all_clubs(self):
        try:
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                statement = "SELECT * FROM CLUBS"
                cursor.execute(statement)
                data = cursor.fetchall()
                cursor.close()
                return data

        except Exception as err:
            print("Update Club Error: ", err)        

        return None

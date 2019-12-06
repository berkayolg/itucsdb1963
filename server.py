from flask import Flask, render_template, request, redirect, url_for, current_app, session
from datetime import datetime

from database import Database, Instructor
from models.student import Student
from models.room import Room
from models.classroom import Classroom
from models.people import People

import hashlib
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'betterthanoriginalsis'

@app.route("/")
def home_page():
    """
    This is the first page users get. We will have a login form here.

    :return:
    """
    return render_template("home.html", 
        authenticated = session.get("logged_in"),
        username = "anon" if not session.get("logged_in") else session["person"]["name"],
        person = session.get("person")
        )


@app.route("/add_course")
def add_course():
    """
    This is for professors to add a new course and relevant information about it e.g. date, TA's etc.
    :return:
    """
    return render_template("add_course.html")


@app.route("/grades")
def grades():
    """
    This webpage is intended for all users.
    Students -> Will be able to see their grades
    Assistants -> Will be able to see their grades(for grad level courses) and enter grades for courses they are TA'ing
    Professors -> Will be able to enter grades (choose a course, get a list of students)
    :return:
    """
    return render_template("grades.html")


@app.route("/courses")
def courses():
    """
    This page is common for users.

    If user is student, she will see the courses she is registered to.
    If user is an assistant, she will see the courses she is registered to and she is TA'ing.
    If user is a professor, she will see the courses she is giving.

    :return:
    """
    return render_template("courses.html")


@app.route("/settings")
def user_settings():
    """
    Users will be able to update their profile pictures, phone number etc.

    :return:
    """
    return render_template("settings.html")


@app.route("/schedule")
def schedule():
    """
    This is a common page. Users will be able to see their schedules according to courses
    they are registered to/they are giving.

    :return:
    """
    return render_template("schedule.html")


@app.route("/exams")
def exams():
    """
    In this page we will show the exam dates for students.
    Same for assistants.

    Professors will see exam dates of their courses and they will be able to update the exam date if it is not
    colliding with another exam date.

    :return:
    """
    return render_template("exams.html")


@app.route("/su", methods = ["GET", "POST"])
def admin_page():
    """
    God mode.
    :return:
    """
    db = Database()
    faculty_list = db.get_faculty(0)
    prof_list = db.get_instructors()

    if request.method == "GET":
        #print(session.get("person").get("admin"), "asdadsd")
        if session.get("person")["admin"]:
            return render_template("admin_page.html", faculty_list=faculty_list, prof_list=prof_list, student_list=db.get_students())
        else:
            return redirect(url_for("home_page"))
    return render_template("admin_page.html")

@app.route("/rooms_list", methods = ["GET", "POST"])
def rooms_page():
    '''
    In this page we will show the rooms
    :return:
    '''
    db = Database()
    rooms = db.get_rooms()
    return render_template("rooms_list.html", rooms = rooms)

@app.route("/room_create", methods= ["POST", "GET"])
def room_create():
    db = Database()
    data = request.form
    is_class = 'FALSE'
    is_room = 'FALSE'
    is_lab = 'FALSE'
    if data["type"] == "class":
        is_class = 'TRUE'
    elif data["type"] == "room":
        is_room = 'TRUE'
    elif data["type"] == "lab":
        is_lab = 'TRUE'
    room = Room(data["building"], data["name"], data["capacity"], is_class, is_room, is_lab)
    key = db.add_room(room)
    return redirect(url_for("admin_page"))

@app.route("/classrooms_list", methods = ["GET", "POST"])
def classrooms_page():
    '''
    In this page we will show the classrooms
    :return:
    '''
    db = current_app.config["db"]
    if request.method == "GET":
        return render_template("classrooms_list.html", classrooms = db.get_classrooms())
    else:
        form_classroom_keys = request.form.getlist("classroom_keys")
        for form_classroom_key in form_classroom_keys:
            db.delete_classroom(int(form_classroom_key))
        return redirect(url_for("classrooms_page"))

@app.route("/instructors", methods = ["GET", "POST"])
def instructors_page():
    '''
    In this page we will show the instructors
    :return:
    '''
    db = Database()
    instructors = db.get_instructors()

    return render_template("instructors.html", instructors = instructors)

@app.route("/instructor_create", methods= ["POST", "GET"])
def instructor_create():
    db = Database()
    data = request.form
    password = hashlib.md5(data["password"].encode())
    person = People(name=data["name"], password=password.hexdigest(), mail=data["mail"])
    db.add_person(person) 
    instructor = Instructor(person.id, data["name"], data["bachelors"], data["masters"], data["doctorates"], data["department"], data["room"], data["lab"])
    key = db.add_instructor(instructor)
    return redirect(url_for("admin_page"))

@app.route("/student_create", methods= ["POST", "GET"])
def student_create():
    db = Database()
    data = request.form
    student = Student(data["name"], data["number"], data["cred"], data["depart"], data["facu"])
    key = db.add_student(student)
    return redirect(url_for("admin_page"))

@app.route("/student_list", methods = ["GET", ])
def students_list():
    #db = current_app.config["db"]
    #students = db.get_students().values()
    db = Database()
    students = db.get_students()

    return render_template("students_list.html", name = students[0]["Name"], students = students)


@app.route("/login", methods = ["GET", ])
def login_page():
    return render_template("login_page.html")

@app.route("/login_action", methods = ["POST", ])
def login_action():
    data = request.form
    
    db = Database()
    person = db.get_person_by_mail(data["mail"])

    attempted_hashed_passw = hashlib.md5(data["password"].encode()).hexdigest()

    if not person or person.password != attempted_hashed_passw:
        return redirect(url_for("login_page"))

    session["logged_in"] = 1
    session["person"] = vars(person)
    return redirect(url_for("home_page"))

@app.route("/signup", methods = ["GET", ])
def signup_page():
    return render_template("signup_page.html")

@app.route("/signup_action", methods = ["POST", ])
def signup_action():
    data = request.form 
    
    password = hashlib.md5(data["password"].encode())
    
    person = People(name=data["name"], password=password.hexdigest(), mail=data["mail"])
    db = Database()
    db.add_person(person)

    session["logged_in"] = 1
    session["person"] = vars(person)

    return redirect(url_for("home_page"))


@app.route("/logout", methods = ["GET", ])
def logout():
    if session["logged_in"]:
        session["logged_in"] = 0
        session["person"] = None

    return redirect(url_for("home_page"))

if __name__ == "__main__":
    app.run(debug=True)

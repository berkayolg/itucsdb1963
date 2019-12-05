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


@app.route("/")
def home_page():
    """
    This is the first page users get. We will have a login form here.

    :return:
    """

    return render_template("home.html", 
        authenticated = session["logged_in"],
        username = "anon" if not session["logged_in"] else session["user_name"]
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
    if request.method == "GET":
        return render_template("admin_page.html")
    else:
        if "instructor" in request.form:
            form_name = request.form["name"]
            form_department = request.form["department"]
            form_lecture_id = request.form["lecture_id"]
            form_room = request.form["room"]
            form_lab = request.form["lab"]
            instructor = Instructor(form_name, form_department, form_lecture_id, form_room, form_lab)
            db = current_app.config["db"]
            instructor_key = db.add_instructor(instructor)
            return redirect(url_for("instructors_page"))
        elif "room" in request.form:
            form_name = request.form["name"]
            form_building = request.form["building"]
            form_capacity = request.form["capacity"]
            form_is_class = request.form["type"] == "class"
            form_is_lab = request.form["type"] == "lab"
            form_is_room = request.form["type"] == "room"
            room = Room(form_building, form_name, form_capacity, form_is_class, form_is_room, form_is_lab)
            db = current_app.config["db"]
            room_key = db.add_room(room)
            return redirect(url_for("rooms_page"))
        elif "classroom" in request.form:
            form_id = request.form["id"]
            form_type = request.form["type"]
            form_board_type = request.form["board_type"]
            form_building = request.form["building"]
            form_restoration_date = request.form["restoration_date"]
            form_board_type = request.form["board_type"]
            form_availability = request.form["availability"] == "available"
            form_conditioner = request.form["conditioner"] == "yes"

            classroom = Classroom(form_id, form_building, form_type, form_restoration_date, form_availability, form_conditioner, form_board_type)
            db = current_app.config["db"]
            classroom_key = db.add_classroom(classroom)
            return redirect(url_for("classrooms_page"))
        return render_template("admin_page.html")

@app.route("/rooms_list", methods = ["GET", "POST"])
def rooms_page():
    '''
    In this page we will show the rooms
    :return:
    '''
    db = current_app.config["db"]
    if request.method == "GET":
        return render_template("rooms_list.html", rooms = db.get_rooms())
    else:
        form_room_keys = request.form.getlist("room_keys")
        for form_room_key in form_room_keys:
            db.delete_room(int(form_room_key))
        return redirect(url_for("rooms_page"))

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
    db = current_app.config["db"]
    if request.method == "GET":
        return render_template("instructors.html", instructors = db.get_instructors())
    else:
        form_inst_keys = request.form.getlist("instructor_keys")
        for form_inst_key in form_inst_keys:
            db.delete_instructor(int(form_inst_key))
        return redirect(url_for("instructors_page"))

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

    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac(
        'sha256', # The hash digest algorithm for HMAC
        data["password"].encode('utf-8'), # Convert the password to bytes
        salt, # Provide the salt
        100000 # It is recommended to use at least 100,000 iterations of SHA-256 
    )

    username = data["name"]
    password = salt + key

    person = db.get_person_by_un_passw(username = data["name"], password = password)
    print(person)
    if not person:
        return redirect(url_for("login_page"))
    session["logged_in"] = 1
    session["name"] = person.name
    return redirect(url_for("home_page"))

@app.route("/signup", methods = ["GET", ])
def signup_page():
    return render_template("signup_page.html")

@app.route("/signup_action", methods = ["POST", ])
def signup_action():
    data = request.form 
    
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac(
        'sha256', # The hash digest algorithm for HMAC
        data["password"].encode('utf-8'), # Convert the password to bytes
        salt, # Provide the salt
        100000 # It is recommended to use at least 100,000 iterations of SHA-256 
    )
    
    person = People(name=data["name"], password=salt+key, mail=data["mail"])
    db = Database()
    db.add_person(person)

    session["logged_in"] = 1
    session["user_name"]= data["name"]
    session["user_mail"] = data["mail"]

    print("user_name")

    return redirect(url_for("home_page"))


@app.route("/logout", methods = ["GET", ])
def logout():
    if session["logged_in"]:
        session["logged_in"] = 0
        session["user_name"] = None

    return redirect(url_for("home_page"))

if __name__ == "__main__":
    app.config['SECRET_KEY'] = 'betterthanoriginalsis'
    app.run(debug=True)

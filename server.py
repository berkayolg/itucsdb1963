from flask import Flask, render_template, request, redirect, url_for, current_app
from datetime import datetime

from database import Database, Instructor
from models.student import Student
from models.room import Room
from models.classroom import Classroom

app = Flask(__name__)


@app.route("/")
def home_page():
    """
    This is the first page users get. We will have a login form here.

    :return:
    """
    return render_template("home.html")


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
    db = current_app.config["db"]
    data = request.form
    print(data["name"])
    student = Student(data["name"], data["number"], data["cred"], data["depart"], data["facu"], data["club"], data["lab"])
    key = db.add_student(student)
    #print(db.get_student(key).number)
    return redirect(url_for("admin_page"))

@app.route("/students_list", methods = ["GET", ])
def students_list():
    db = current_app.config["db"]
    students = db.get_students().values()
    return render_template("students_list.html", students = students)

if __name__ == "__main__":
    app.config["db"] = Database()
    app.run(debug=True)

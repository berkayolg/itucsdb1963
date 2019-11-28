from flask import Flask, render_template, request, redirect, url_for, current_app
from datetime import datetime

from database import Database, Instructor
from models.student import Student

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
        return render_template("admin_page.html")

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
    student = Student(1, data["number"], data["cred"], data["depart"], data["facu"], data["club"], data["lab"])
    key = db.add_student(student)
    print(db.get_student(key).number)
    return redirect(url_for("admin_page"))

@app.route("/students_list", methods = ["GET", ])
def students_list():
    db = current_app.config["db"]
    students = db.get_students().values()
    return render_template("students_list.html", students = students)

if __name__ == "__main__":
    app.config["db"] = Database()
    app.run(debug=True)

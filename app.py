from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


def get_db_connection():
    connection = sqlite3.connect("students.db")
    connection.row_factory = sqlite3.Row
    return connection


@app.route("/")
def index():
    connection = get_db_connection()
    students = connection.execute(
        "SELECT * FROM students"
    ).fetchall()
    connection.close()

    return render_template("index.html", students=students)


@app.route("/add", methods=("GET", "POST"))
def add_student():
    if request.method == "POST":
        name = request.form["name"]
        course = request.form["course"]
        year_level = request.form["year_level"]

        connection = get_db_connection()
        connection.execute(
            "INSERT INTO students (name, course, year_level) VALUES (?, ?, ?)",
            (name, course, year_level)
        )
        connection.commit()
        connection.close()

        return redirect("/")

    return render_template("add_student.html")


@app.route("/edit/<int:id>", methods=("GET", "POST"))
def edit_student(id):
    connection = get_db_connection()

    student = connection.execute(
        "SELECT * FROM students WHERE id = ?",
        (id,)
    ).fetchone()

    if request.method == "POST":
        name = request.form["name"]
        course = request.form["course"]
        year_level = request.form["year_level"]

        connection.execute(
            """
            UPDATE students
            SET name = ?, course = ?, year_level = ?
            WHERE id = ?
            """,
            (name, course, year_level, id)
        )

        connection.commit()
        connection.close()

        return redirect("/")

    connection.close()

    return render_template("edit_student.html", student=student)


@app.route("/delete/<int:id>")
def delete_student(id):
    connection = get_db_connection()

    connection.execute(
        "DELETE FROM students WHERE id = ?",
        (id,)
    )

    connection.commit()
    connection.close()

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
# Import the required modules
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import csv
import io
from datetime import date
from flask import Flask, render_template, request, redirect, url_for, make_response, session

# Create the Flask application
app = Flask(__name__)

app.secret_key = "EduTrack@2026!Mashood#Flask$123"


# -------------------------------
# Create the database and students table
# -------------------------------
def create_database():

    connection = sqlite3.connect("database/edutrack.db")
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS learners(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT NOT NULL,

        email TEXT UNIQUE NOT NULL,

        password TEXT NOT NULL,

        date_of_birth TEXT NOT NULL,

        skill TEXT NOT NULL,

        level TEXT NOT NULL,

        points INTEGER DEFAULT 0,

        joined_date TEXT NOT NULL

    )
    """)

    connection.commit()
    connection.close()


# -------------------------------
# Home Page (Dashboard)
# -------------------------------

@app.route("/")
def home():
    return render_template("landing.html")


@app.route("/admin/dashboard")
def admin_dashboard():

    connection = sqlite3.connect("database/edutrack.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    search_query = request.args.get("search")

    if search_query:
        cursor.execute("""
            SELECT * FROM learners
            WHERE name LIKE ?
               OR skill LIKE ?
               OR email LIKE ?
        """, (
            f"%{search_query}%",
            f"%{search_query}%",
            f"%{search_query}%"
        ))
    else:
        cursor.execute("SELECT * FROM learners")

    learners = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM learners")
    total_learners = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(DISTINCT skill) FROM learners")
    total_skills = cursor.fetchone()[0]

    cursor.execute("SELECT MAX(points) FROM learners")
    highest_points = cursor.fetchone()[0]

    if highest_points is None:
        highest_points = 0

    connection.close()

    return render_template(
        "admin_dashboard.html",
        learners=learners,
        search_query=search_query,
        total_learners=total_learners,
        total_skills=total_skills,
        highest_points=highest_points
    )


# -------------------------------
# Register Learner
# -------------------------------

@app.route("/register", methods=["GET", "POST"])
def register_learner():

    if request.method == "POST":

        learner_name = request.form["learner_name"]
        learner_email = request.form["learner_email"]
        learner_password = generate_password_hash(
            request.form["learner_password"]
        )
        learner_dob = request.form["learner_dob"]
        learner_skill = request.form["learner_skill"]
        learner_level = request.form["learner_level"]

        joined_date = date.today().isoformat()
        points = 0

        connection = sqlite3.connect("database/edutrack.db")
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO learners
            (name, email, password, date_of_birth, skill, level, points, joined_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            learner_name,
            learner_email,
            learner_password,
            learner_dob,
            learner_skill,
            learner_level,
            points,
            joined_date
        ))

        connection.commit()
        connection.close()

        return redirect(url_for("learner_login"))

    return render_template("register.html")


# -------------------------------
# Edit Learner
# -------------------------------
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_learner(id):

    connection = sqlite3.connect("database/edutrack.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    # Fetch learner details
    cursor.execute("SELECT * FROM learners WHERE id = ?", (id,))
    learner = cursor.fetchone()

    if request.method == "POST":

        learner_name = request.form["learner_name"]
        learner_email = request.form["learner_email"]
        learner_dob = request.form["learner_dob"]
        learner_skill = request.form["learner_skill"]
        learner_level = request.form["learner_level"]

        cursor.execute("""
            UPDATE learners
            SET name = ?,
                email = ?,
                date_of_birth = ?,
                skill = ?,
                level = ?
            WHERE id = ?
        """, (
            learner_name,
            learner_email,
            learner_dob,
            learner_skill,
            learner_level,
            id
        ))

        connection.commit()
        connection.close()

        return redirect(url_for("admin_dashboard"))

    connection.close()

    return render_template("edit.html", learner=learner)

# -------------------------------
# Delete Learner
# -------------------------------
@app.route("/delete/<int:id>")
def delete_learner(id):

    # Connect to the EduTrack database
    connection = sqlite3.connect("database/edutrack.db")

    # Create a cursor
    cursor = connection.cursor()

    # Delete the selected learner
    cursor.execute(
        "DELETE FROM learners WHERE id = ?",
        (id,)
    )

    # Save changes
    connection.commit()

    # Close the connection
    connection.close()

    # Return to the dashboard
    return redirect(url_for("admin_dashboard"))

# --------------------------------
# Exports CSV File
# --------------------------------

@app.route("/export")
def export_csv():

    # Connect to the EduTrack database
    connection = sqlite3.connect("database/edutrack.db")
    cursor = connection.cursor()

    # Fetch learner details
    cursor.execute("""
        SELECT
            name,
            email,
            date_of_birth,
            skill,
            level,
            points,
            joined_date
        FROM learners
    """)

    learners = cursor.fetchall()

    connection.close()

    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)

    # CSV Header
    writer.writerow([
        "Name",
        "Email",
        "Date of Birth",
        "Learning Path",
        "Level",
        "Points",
        "Joined Date"
    ])

    # CSV Data
    writer.writerows(learners)

    # Create response
    response = make_response(output.getvalue())

    response.headers["Content-Disposition"] = "attachment; filename=learners.csv"
    response.headers["Content-Type"] = "text/csv"

    return response


# -------------------------------
# Learner Login
# -------------------------------

@app.route("/learner/login", methods=["GET", "POST"])
def learner_login():

    if request.method == "POST":

        learner_email = request.form["learner_email"]
        learner_password = request.form["learner_password"]

        connection = sqlite3.connect("database/edutrack.db")
        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM learners WHERE email = ?",
            (learner_email,)
        )

        learner = cursor.fetchone()
        connection.close()

        if learner and check_password_hash(learner[3], learner_password):

            session["learner_id"] = learner[0]
            session["learner_name"] = learner[1]

            return redirect(url_for("learner_dashboard"))

        return render_template(
            "learner_login.html",
            error="Invalid email or password."
        )

    return render_template("learner_login.html")

# -------------------------------
# Learner Dashboard
# -------------------------------

@app.route("/learner/dashboard")
def learner_dashboard():

    if "learner_id" not in session:
        return redirect(url_for("learner_login"))

    connection = sqlite3.connect("database/edutrack.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM learners WHERE id = ?",
        (session["learner_id"],)
    )

    learner = cursor.fetchone()

    connection.close()

    return render_template(
        "learner_dashboard.html",
        learner=learner
    )
    
@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("home"))

# -------------------------------
# Start the Flask application
# -------------------------------
if __name__ == "__main__":

    # Create the database and table before starting the server
    create_database()

    # Run the Flask development server
    app.run(debug=True)
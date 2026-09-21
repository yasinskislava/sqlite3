from functools import wraps
import sqlite3
from flask import Flask, redirect, render_template, request, session, url_for, flash

app = Flask(__name__)
app.secret_key = "super_secret_key"


def get_db_connection():
    conn = sqlite3.connect("school.db")
    conn.row_factory = sqlite3.Row
    return conn


# --- Authentication & Access Control Helpers ---


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return decorated_function


def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if session.get("role") not in roles:
                return "Access Denied: Insufficient Permissions", 403
            return f(*args, **kwargs)

        return decorated_function

    return decorator


@app.context_processor
def inject_user():
    if "user_id" in session:
        return {
            "current_user": {
                "is_authenticated": True,
                "first_name": session.get("first_name"),
                "role": session.get("role"),
            }
        }
    return {"current_user": {"is_authenticated": False}}


# --- Routes ---


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM Users WHERE email = ?", (email,)
        ).fetchone()
        conn.close()

        if user:
            session["user_id"] = user["userID"]
            session["first_name"] = user["first_name"]
            session["role"] = user["role"]
            return redirect(url_for("account"))

        return "Invalid email address", 401
    return '<form method="post"><input type="email" name="email" placeholder="Email" required><button type="submit">Login</button></form>'


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


@app.route("/library")
def library():
    conn = get_db_connection()
    books = conn.execute("SELECT * FROM Books").fetchall()
    conn.close()
    return render_template("library.html", books=books)


@app.route("/account")
@login_required
def account():
    conn = get_db_connection()
    user_id = session["user_id"]
    role = session["role"]

    user = conn.execute(
        "SELECT * FROM Users WHERE userID = ?", (user_id,)
    ).fetchone()

    performance = None
    courses = []
    children = []

    if role == "student":
        performance = conn.execute(
            "SELECT * FROM Performance WHERE userID = ?", (user_id,)
        ).fetchone()
        courses = conn.execute(
            """
            SELECT c.name FROM Courses c
            JOIN Enrollment e ON c.courseID = e.courseID
            WHERE e.userID = ?
        """,
            (user_id,),
        ).fetchall()

    elif role == "parent":
        child_rows = conn.execute(
            """
            SELECT u.first_name, u.last_name, p.status, p.attendance, p.grade
            FROM ParentStudent ps
            JOIN Users u ON ps.studentID = u.userID
            LEFT JOIN Performance p ON u.userID = p.userID
            WHERE ps.parentID = ?
        """,
            (user_id,),
        ).fetchall()

        for row in child_rows:
            children.append({
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "performance": {
                    "status": row["status"],
                    "attendance": row["attendance"],
                    "grade": row["grade"],
                },
            })

    conn.close()
    return render_template(
        "account.html",
        user=user,
        performance=performance,
        courses=courses,
        children=children,
    )


@app.route("/borrowed")
@login_required
@role_required("student", "teacher")
def borrowed():
    conn = get_db_connection()
    records = conn.execute(
        """
        SELECT b.title, b.author, r.borrow_date, r.due_date, r.return_date, r.status
        FROM Records r
        JOIN Books b ON r.bID = b.bID
        WHERE r.userID = ?
    """,
        (session["user_id"],),
    ).fetchall()
    conn.close()
    return render_template("borrowed.html", records=records)


@app.route("/students")
@login_required
@role_required("teacher", "admin")
def students():
    conn = get_db_connection()

    students_data = conn.execute("""
        SELECT 
            s.userID, s.first_name, s.last_name, s.email, s.mobile,
            p.first_name AS parent_first, p.last_name AS parent_last, p.mobile AS parent_mobile
        FROM Users s
        LEFT JOIN ParentStudent ps ON s.userID = ps.studentID
        LEFT JOIN Users p ON ps.parentID = p.userID
        WHERE s.role = 'student'
    """).fetchall()

    students_list = []
    for s in students_data:
        courses_data = conn.execute(
            """
            SELECT c.name FROM Courses c
            JOIN Enrollment e ON c.courseID = e.courseID
            WHERE e.userID = ?
        """,
            (s["userID"],),
        ).fetchall()

        courses = [c["name"] for c in courses_data]

        students_list.append({
            "first_name": s["first_name"],
            "last_name": s["last_name"],
            "email": s["email"],
            "mobile": s["mobile"],
            "parent_name": f"{s['parent_first']} {s['parent_last']}"
            if s["parent_first"]
            else "N/A",
            "parent_mobile": s["parent_mobile"] if s["parent_mobile"] else "N/A",
            "courses": courses,
        })

    conn.close()
    return render_template("students.html", students=students_list)


if __name__ == "__main__":
    app.run(debug=True)
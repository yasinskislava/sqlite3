import sqlite3

conn = sqlite3.connect("school.db")
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")

# 1. Re-create Schema
cursor.executescript("""
DROP TABLE IF EXISTS ParentStudent;
DROP TABLE IF EXISTS Records;
DROP TABLE IF EXISTS Enrollment;
DROP TABLE IF EXISTS Courses;
DROP TABLE IF EXISTS Performance;
DROP TABLE IF EXISTS Books;
DROP TABLE IF EXISTS Users;

CREATE TABLE Users (
    userID INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    dob TEXT,
    email TEXT NOT NULL UNIQUE,
    mobile TEXT,
    role TEXT CHECK(role IN ('student', 'teacher', 'admin', 'parent')) NOT NULL
);

CREATE TABLE ParentStudent (
    parentID INTEGER NOT NULL,
    studentID INTEGER NOT NULL,
    PRIMARY KEY (parentID, studentID),
    FOREIGN KEY (parentID) REFERENCES Users(userID) ON DELETE CASCADE,
    FOREIGN KEY (studentID) REFERENCES Users(userID) ON DELETE CASCADE
);

CREATE TABLE Books (
    bID INTEGER PRIMARY KEY AUTOINCREMENT,
    ISBN TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    pub_year INTEGER,
    author TEXT
);

CREATE TABLE Records (
    userID INTEGER NOT NULL,
    bID INTEGER NOT NULL,
    borrow_date TEXT NOT NULL,
    due_date TEXT NOT NULL,
    return_date TEXT,
    status TEXT CHECK(status IN ('ON_TIME', 'LATE', 'OVERDUE', 'BORROWED')),
    PRIMARY KEY (userID, bID, borrow_date),
    FOREIGN KEY (userID) REFERENCES Users(userID) ON DELETE CASCADE,
    FOREIGN KEY (bID) REFERENCES Books(bID) ON DELETE CASCADE
);

CREATE TABLE Courses (
    courseID INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    userID INTEGER,
    FOREIGN KEY (userID) REFERENCES Users(userID) ON DELETE SET NULL
);

CREATE TABLE Enrollment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    courseID INTEGER NOT NULL,
    userID INTEGER NOT NULL,
    FOREIGN KEY (courseID) REFERENCES Courses(courseID) ON DELETE CASCADE,
    FOREIGN KEY (userID) REFERENCES Users(userID) ON DELETE CASCADE
);

CREATE TABLE Performance (
    userID INTEGER PRIMARY KEY,
    status TEXT,
    attendance TEXT,
    grade REAL,
    FOREIGN KEY (userID) REFERENCES Users(userID) ON DELETE CASCADE
);
""")

# 2. Add Role Triggers (Including Student-Only Check for Performance)
cursor.executescript("""
CREATE TRIGGER check_teacher_role
BEFORE INSERT ON Courses
FOR EACH ROW
WHEN NEW.userID IS NOT NULL
BEGIN
    SELECT CASE 
        WHEN (SELECT role FROM Users WHERE userID = NEW.userID) != 'teacher'
        THEN RAISE(ABORT, 'Only users with role "teacher" can be assigned to courses.')
    END;
END;

CREATE TRIGGER check_student_role
BEFORE INSERT ON Enrollment
FOR EACH ROW
BEGIN
    SELECT CASE 
        WHEN (SELECT role FROM Users WHERE userID = NEW.userID) != 'student'
        THEN RAISE(ABORT, 'Only users with role "student" can be enrolled in courses.')
    END;
END;

CREATE TRIGGER check_performance_student_role
BEFORE INSERT ON Performance
FOR EACH ROW
BEGIN
    SELECT CASE 
        WHEN (SELECT role FROM Users WHERE userID = NEW.userID) != 'student'
        THEN RAISE(ABORT, 'Only users with role "student" can have performance records.')
    END;
END;

CREATE TRIGGER check_parent_student_roles
BEFORE INSERT ON ParentStudent
FOR EACH ROW
BEGIN
    SELECT CASE 
        WHEN (SELECT role FROM Users WHERE userID = NEW.parentID) != 'parent'
        THEN RAISE(ABORT, 'parentID must belong to a user with role "parent".')
        WHEN (SELECT role FROM Users WHERE userID = NEW.studentID) != 'student'
        THEN RAISE(ABORT, 'studentID must belong to a user with role "student".')
    END;
END;

CREATE TRIGGER check_library_borrower_role
BEFORE INSERT ON Records
FOR EACH ROW
BEGIN
    SELECT CASE 
        WHEN (SELECT role FROM Users WHERE userID = NEW.userID) NOT IN ('student', 'teacher')
        THEN RAISE(ABORT, 'Only students and teachers can borrow library books.')
    END;
END;
""")

# 3. Populate Users (IDs 1-3: Non-students, IDs 4-10: Students, IDs 11-15: Parents)
users = [
    (
        "Eleanor",
        "Vane",
        "1980-05-12",
        "e.vane@school.ac.uk",
        "07111222333",
        "teacher",
    ),  # 1
    (
        "Marcus",
        "Brodie",
        "1975-09-24",
        "m.brodie@school.ac.uk",
        "07111222444",
        "teacher",
    ),  # 2
    (
        "Sarah",
        "Connor",
        "1985-08-19",
        "s.connor@school.ac.uk",
        "07999000111",
        "admin",
    ),  # 3
    (
        "Liam",
        "Gallagher",
        "2003-11-20",
        "liam.g@student.ac.uk",
        "07444555666",
        "student",
    ),  # 4
    (
        "Sophia",
        "Chen",
        "2004-02-15",
        "sophia.c@student.ac.uk",
        "07777888999",
        "student",
    ),  # 5
    (
        "Oliver",
        "Smith",
        "2003-06-10",
        "oliver.s@student.ac.uk",
        "07555666777",
        "student",
    ),  # 6
    (
        "Amara",
        "Okonkwo",
        "2004-01-30",
        "amara.o@student.ac.uk",
        "07888999000",
        "student",
    ),  # 7
    (
        "James",
        "Wilson",
        "2003-12-05",
        "j.wilson@student.ac.uk",
        "07666777888",
        "student",
    ),  # 8
    (
        "Emma",
        "Watson",
        "2004-04-15",
        "e.watson@student.ac.uk",
        "07123123123",
        "student",
    ),  # 9
    (
        "Lucas",
        "Moura",
        "2003-08-12",
        "l.moura@student.ac.uk",
        "07321321321",
        "student",
    ),  # 10
    (
        "David",
        "Gallagher",
        "1978-03-14",
        "david.g@parent.ac.uk",
        "07222333444",
        "parent",
    ),  # 11
    (
        "Helen",
        "Chen",
        "1981-11-02",
        "helen.c@parent.ac.uk",
        "07333444555",
        "parent",
    ),  # 12
    (
        "Robert",
        "Smith",
        "1972-01-09",
        "r.smith@parent.ac.uk",
        "07444111222",
        "parent",
    ),  # 13
    (
        "Grace",
        "Okonkwo",
        "1979-07-22",
        "g.okonkwo@parent.ac.uk",
        "07555222333",
        "parent",
    ),  # 14
    (
        "Alan",
        "Wilson",
        "1970-10-10",
        "a.wilson@parent.ac.uk",
        "07666333444",
        "parent",
    ),  # 15
]
cursor.executemany(
    "INSERT INTO Users (first_name, last_name, dob, email, mobile, role)"
    " VALUES (?, ?, ?, ?, ?, ?);",
    users,
)

# 4. Populate ParentStudent Links
parent_students = [
    (11, 4),
    (12, 5),
    (13, 6),
    (14, 7),
    (15, 8),
    (11, 9),
    (12, 10),
    (13, 4),
    (14, 5),
    (15, 6),
]
cursor.executemany(
    "INSERT INTO ParentStudent (parentID, studentID) VALUES (?, ?);",
    parent_students,
)

# 5. Populate Books
books = [
    ("978-0141439518", "Pride and Prejudice", 1813, "Jane Austen"),
    ("978-0451524935", "1984", 1949, "George Orwell"),
    ("978-0061120084", "To Kill a Mockingbird", 1960, "Harper Lee"),
    ("978-0743273565", "The Great Gatsby", 1925, "F. Scott Fitzgerald"),
    ("978-0345806789", "The Hobbit", 1937, "J.R.R. Tolkien"),
    ("978-0140283333", "Fahrenheit 451", 1953, "Ray Bradbury"),
    ("978-0547928227", "The Fellowship of the Ring", 1954, "J.R.R. Tolkien"),
    ("978-0316769488", "The Catcher in the Rye", 1951, "J.D. Salinger"),
    ("978-0143127741", "Brave New World", 1932, "Aldous Huxley"),
    ("978-0060850524", "Brave New World Revisited", 1958, "Aldous Huxley"),
]
cursor.executemany(
    "INSERT INTO Books (ISBN, title, pub_year, author) VALUES (?, ?, ?, ?);",
    books,
)

# 6. Populate Library Records
records = [
    (1, 1, "2026-08-01", "2026-08-15", "2026-08-10", "ON_TIME"),
    (2, 2, "2026-08-01", "2026-08-15", "2026-08-20", "LATE"),
    (4, 3, "2026-09-01", "2026-09-15", None, "BORROWED"),
    (5, 4, "2026-08-10", "2026-08-24", "2026-08-22", "ON_TIME"),
    (6, 5, "2026-09-05", "2026-09-19", None, "BORROWED"),
    (7, 6, "2026-07-15", "2026-07-29", "2026-08-05", "LATE"),
    (8, 7, "2026-09-10", "2026-09-24", None, "BORROWED"),
    (9, 8, "2026-08-20", "2026-09-03", "2026-09-01", "ON_TIME"),
    (10, 9, "2026-09-12", "2026-09-26", None, "BORROWED"),
    (4, 10, "2026-09-01", "2026-09-15", "2026-09-14", "ON_TIME"),
]
cursor.executemany(
    "INSERT INTO Records (userID, bID, borrow_date, due_date, return_date,"
    " status) VALUES (?, ?, ?, ?, ?, ?);",
    records,
)

# 7. Populate Courses & Enrollments
courses = [
    ("Database Management Systems", 1),
    ("Introduction to Python", 1),
    ("Advanced Mathematics", 2),
    ("World History", 2),
    ("English Literature", 1),
    ("Physics I", 2),
    ("Chemistry Basics", 1),
    ("Art & Design", 2),
    ("Physical Education", 1),
    ("Computer Networks", 2),
]
cursor.executemany(
    "INSERT INTO Courses (name, userID) VALUES (?, ?);", courses
)

enrollments = [
    (1, 4),
    (1, 5),
    (2, 6),
    (2, 7),
    (3, 8),
    (3, 9),
    (4, 10),
    (5, 4),
    (6, 5),
    (7, 6),
]
cursor.executemany(
    "INSERT INTO Enrollment (courseID, userID) VALUES (?, ?);", enrollments
)

# 8. Populate Performance (Restricted strictly to Student User IDs 4-10)
performances = [
    (4, "PASS", "92%", 78.5),
    (5, "EXCELLENT", "98%", 94.0),
    (6, "PASS", "88%", 72.0),
    (7, "EXCELLENT", "95%", 89.5),
    (8, "WARNING", "75%", 58.0),
    (9, "PASS", "91%", 81.0),
    (10, "PASS", "85%", 74.5),
]
cursor.executemany(
    "INSERT INTO Performance (userID, status, attendance, grade) VALUES (?, ?,"
    " ?, ?);",
    performances,
)

conn.commit()
conn.close()

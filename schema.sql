BEGIN TRANSACTION;
CREATE TABLE Books (
    bID INTEGER PRIMARY KEY AUTOINCREMENT,
    ISBN TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    pub_year INTEGER,
    author TEXT
);
INSERT INTO "Books" VALUES(1,'978-0141439518','Pride and Prejudice',1813,'Jane Austen');
INSERT INTO "Books" VALUES(2,'978-0451524935','1984',1949,'George Orwell');
INSERT INTO "Books" VALUES(3,'978-0061120084','To Kill a Mockingbird',1960,'Harper Lee');
INSERT INTO "Books" VALUES(4,'978-0743273565','The Great Gatsby',1925,'F. Scott Fitzgerald');
INSERT INTO "Books" VALUES(5,'978-0345806789','The Hobbit',1937,'J.R.R. Tolkien');
INSERT INTO "Books" VALUES(6,'978-0140283333','Fahrenheit 451',1953,'Ray Bradbury');
INSERT INTO "Books" VALUES(7,'978-0547928227','The Fellowship of the Ring',1954,'J.R.R. Tolkien');
INSERT INTO "Books" VALUES(8,'978-0316769488','The Catcher in the Rye',1951,'J.D. Salinger');
INSERT INTO "Books" VALUES(9,'978-0143127741','Brave New World',1932,'Aldous Huxley');
INSERT INTO "Books" VALUES(10,'978-0060850524','Brave New World Revisited',1958,'Aldous Huxley');
CREATE TABLE Courses (
    courseID INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    userID INTEGER,
    FOREIGN KEY (userID) REFERENCES Users(userID) ON DELETE SET NULL
);
INSERT INTO "Courses" VALUES(1,'Database Management Systems',1);
INSERT INTO "Courses" VALUES(2,'Introduction to Python',1);
INSERT INTO "Courses" VALUES(3,'Advanced Mathematics',2);
INSERT INTO "Courses" VALUES(4,'World History',2);
INSERT INTO "Courses" VALUES(5,'English Literature',1);
INSERT INTO "Courses" VALUES(6,'Physics I',2);
INSERT INTO "Courses" VALUES(7,'Chemistry Basics',1);
INSERT INTO "Courses" VALUES(8,'Art & Design',2);
INSERT INTO "Courses" VALUES(9,'Physical Education',1);
INSERT INTO "Courses" VALUES(10,'Computer Networks',2);
CREATE TABLE Enrollment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    courseID INTEGER NOT NULL,
    userID INTEGER NOT NULL,
    FOREIGN KEY (courseID) REFERENCES Courses(courseID) ON DELETE CASCADE,
    FOREIGN KEY (userID) REFERENCES Users(userID) ON DELETE CASCADE
);
INSERT INTO "Enrollment" VALUES(1,1,4);
INSERT INTO "Enrollment" VALUES(2,1,5);
INSERT INTO "Enrollment" VALUES(3,2,6);
INSERT INTO "Enrollment" VALUES(4,2,7);
INSERT INTO "Enrollment" VALUES(5,3,8);
INSERT INTO "Enrollment" VALUES(6,3,9);
INSERT INTO "Enrollment" VALUES(7,4,10);
INSERT INTO "Enrollment" VALUES(8,5,4);
INSERT INTO "Enrollment" VALUES(9,6,5);
INSERT INTO "Enrollment" VALUES(10,7,6);
CREATE TABLE ParentStudent (
    parentID INTEGER NOT NULL,
    studentID INTEGER NOT NULL,
    PRIMARY KEY (parentID, studentID),
    FOREIGN KEY (parentID) REFERENCES Users(userID) ON DELETE CASCADE,
    FOREIGN KEY (studentID) REFERENCES Users(userID) ON DELETE CASCADE
);
INSERT INTO "ParentStudent" VALUES(11,4);
INSERT INTO "ParentStudent" VALUES(12,5);
INSERT INTO "ParentStudent" VALUES(13,6);
INSERT INTO "ParentStudent" VALUES(14,7);
INSERT INTO "ParentStudent" VALUES(15,8);
INSERT INTO "ParentStudent" VALUES(11,9);
INSERT INTO "ParentStudent" VALUES(12,10);
INSERT INTO "ParentStudent" VALUES(13,4);
INSERT INTO "ParentStudent" VALUES(14,5);
INSERT INTO "ParentStudent" VALUES(15,6);
CREATE TABLE Performance (
    userID INTEGER PRIMARY KEY,
    status TEXT,
    attendance TEXT,
    grade REAL,
    FOREIGN KEY (userID) REFERENCES Users(userID) ON DELETE CASCADE
);
INSERT INTO "Performance" VALUES(4,'PASS','92%',78.5);
INSERT INTO "Performance" VALUES(5,'EXCELLENT','98%',94.0);
INSERT INTO "Performance" VALUES(6,'PASS','88%',72.0);
INSERT INTO "Performance" VALUES(7,'EXCELLENT','95%',89.5);
INSERT INTO "Performance" VALUES(8,'WARNING','75%',58.0);
INSERT INTO "Performance" VALUES(9,'PASS','91%',81.0);
INSERT INTO "Performance" VALUES(10,'PASS','85%',74.5);
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
INSERT INTO "Records" VALUES(1,1,'2026-08-01','2026-08-15','2026-08-10','ON_TIME');
INSERT INTO "Records" VALUES(2,2,'2026-08-01','2026-08-15','2026-08-20','LATE');
INSERT INTO "Records" VALUES(4,3,'2026-09-01','2026-09-15',NULL,'BORROWED');
INSERT INTO "Records" VALUES(5,4,'2026-08-10','2026-08-24','2026-08-22','ON_TIME');
INSERT INTO "Records" VALUES(6,5,'2026-09-05','2026-09-19',NULL,'BORROWED');
INSERT INTO "Records" VALUES(7,6,'2026-07-15','2026-07-29','2026-08-05','LATE');
INSERT INTO "Records" VALUES(8,7,'2026-09-10','2026-09-24',NULL,'BORROWED');
INSERT INTO "Records" VALUES(9,8,'2026-08-20','2026-09-03','2026-09-01','ON_TIME');
INSERT INTO "Records" VALUES(10,9,'2026-09-12','2026-09-26',NULL,'BORROWED');
INSERT INTO "Records" VALUES(4,10,'2026-09-01','2026-09-15','2026-09-14','ON_TIME');
CREATE TABLE Users (
    userID INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    dob TEXT,
    email TEXT NOT NULL UNIQUE,
    mobile TEXT,
    role TEXT CHECK(role IN ('student', 'teacher', 'admin', 'parent')) NOT NULL
);
INSERT INTO "Users" VALUES(1,'Eleanor','Vane','1980-05-12','e.vane@school.ac.uk','07111222333','teacher');
INSERT INTO "Users" VALUES(2,'Marcus','Brodie','1975-09-24','m.brodie@school.ac.uk','07111222444','teacher');
INSERT INTO "Users" VALUES(3,'Sarah','Connor','1985-08-19','s.connor@school.ac.uk','07999000111','admin');
INSERT INTO "Users" VALUES(4,'Liam','Gallagher','2003-11-20','liam.g@student.ac.uk','07444555666','student');
INSERT INTO "Users" VALUES(5,'Sophia','Chen','2004-02-15','sophia.c@student.ac.uk','07777888999','student');
INSERT INTO "Users" VALUES(6,'Oliver','Smith','2003-06-10','oliver.s@student.ac.uk','07555666777','student');
INSERT INTO "Users" VALUES(7,'Amara','Okonkwo','2004-01-30','amara.o@student.ac.uk','07888999000','student');
INSERT INTO "Users" VALUES(8,'James','Wilson','2003-12-05','j.wilson@student.ac.uk','07666777888','student');
INSERT INTO "Users" VALUES(9,'Emma','Watson','2004-04-15','e.watson@student.ac.uk','07123123123','student');
INSERT INTO "Users" VALUES(10,'Lucas','Moura','2003-08-12','l.moura@student.ac.uk','07321321321','student');
INSERT INTO "Users" VALUES(11,'David','Gallagher','1978-03-14','david.g@parent.ac.uk','07222333444','parent');
INSERT INTO "Users" VALUES(12,'Helen','Chen','1981-11-02','helen.c@parent.ac.uk','07333444555','parent');
INSERT INTO "Users" VALUES(13,'Robert','Smith','1972-01-09','r.smith@parent.ac.uk','07444111222','parent');
INSERT INTO "Users" VALUES(14,'Grace','Okonkwo','1979-07-22','g.okonkwo@parent.ac.uk','07555222333','parent');
INSERT INTO "Users" VALUES(15,'Alan','Wilson','1970-10-10','a.wilson@parent.ac.uk','07666333444','parent');
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
DELETE FROM "sqlite_sequence";
INSERT INTO "sqlite_sequence" VALUES('Users',15);
INSERT INTO "sqlite_sequence" VALUES('Books',10);
INSERT INTO "sqlite_sequence" VALUES('Courses',10);
INSERT INTO "sqlite_sequence" VALUES('Enrollment',10);
COMMIT;

import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()


def _connect():
    """
    Opens a new connection using .env variables.
    PGOPTIONS defaults to forcing search_path=Part1 so we don't need to SET it.
    """
    return psycopg2.connect(
        host=os.getenv("PGHOST", "localhost"),
        port=os.getenv("PGPORT", "5432"),
        user=os.getenv("PGUSER", "postgres"),
        password=os.getenv("PGPASSWORD", "postgres"),
        dbname=os.getenv("PGDATABASE", "postgres"),
        options=os.getenv("PGOPTIONS", "-c search_path=Part1"),
        cursor_factory=RealDictCursor,
    )

def getAllStudents():
    """
    Returns a list of student dicts.
    Tries the DB function get_all_students(); if missing, falls back to SELECT.
    """
    with _connect() as conn, conn.cursor() as cur:
        try:
            cur.execute("SELECT * FROM get_all_students()")
        except errors.UndefinedFunction:
            # Fallback if you didn't load functions.sql
            cur.execute("SELECT * FROM students ORDER BY student_id")
        return cur.fetchall()

def addStudent(first_name: str, last_name: str, email: str, enrollment_date: date | str):
    """
    Inserts a student and returns the inserted row as a dict.
    Prefers add_student(...); falls back to INSERT ... RETURNING *.
    """
    with _connect() as conn, conn.cursor() as cur:
        try:
            cur.execute(
                "SELECT * FROM add_student(%s,%s,%s,%s)",
                (first_name, last_name, email, enrollment_date),
            )
        except errors.UndefinedFunction:
            cur.execute(
                """
                INSERT INTO students (first_name, last_name, email, enrollment_date)
                VALUES (%s,%s,%s,%s)
                RETURNING *;
                """,
                (first_name, last_name, email, enrollment_date),
            )
        row = cur.fetchone()
        conn.commit()
        return row

def updateStudentEmail(student_id: int, new_email: str):
    """
    Updates a student's email and returns the updated row as a dict.
    Prefers update_student_email(id,email); falls back to UPDATE ... RETURNING *.
    """
    with _connect() as conn, conn.cursor() as cur:
        try:
            cur.execute(
                "SELECT * FROM update_student_email(%s,%s)",
                (student_id, new_email),
            )
        except errors.UndefinedFunction:
            cur.execute(
                """
                UPDATE students
                SET email = %s
                WHERE student_id = %s
                RETURNING *;
                """,
                (new_email, student_id),
            )
        row = cur.fetchone()
        if row is None:
            raise ValueError(f"Student with id {student_id} not found")
        conn.commit()
        return row

def deleteStudent(student_id: int):
    """
    Deletes a student and returns the deleted row as a dict.
    Prefers delete_student(id); falls back to DELETE ... RETURNING *.
    """
    with _connect() as conn, conn.cursor() as cur:
        try:
            cur.execute("SELECT * FROM delete_student(%s)", (student_id,))
        except errors.UndefinedFunction:
            cur.execute(
                "DELETE FROM students WHERE student_id = %s RETURNING *;",
                (student_id,),
            )
        row = cur.fetchone()
        if row is None:
            raise ValueError(f"Student with id {student_id} not found")
        conn.commit()
        return row

# ---------------------------
# Demo (optional)
# ---------------------------
if __name__ == "__main__":
    print("Initial:", getAllStudents())
    print("Insert :", addStudent("Ada", "Lovelace", "ada@example.com", "2024-09-01"))
    print("Update :", updateStudentEmail(1, "johnny.doe@example.com"))  # adjust id if needed
    print("Delete :", deleteStudent(2))                                  # adjust id if needed
    print("Final  :", getAllStudents())
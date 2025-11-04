import os
import psycopg2
from dotenv import load_dotenv
load_dotenv()

def get_connection():
    return psycopg2.connect(
        host=os.getenv("PGHOST"),
        port=os.getenv("PGPORT"),
        database=os.getenv("PGDATABASE"),
        user=os.getenv("PGUSER"),
        password=os.getenv("PGPASSWORD")
    )

def getAllStudents():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM "Part1"."getAllStudents"()')
            return cur.fetchall()

def addStudent(first_name, last_name, email, enrollment_date):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                'SELECT * FROM "Part1"."addStudent"(%s, %s, %s, %s)',
                (first_name, last_name, email, enrollment_date),
            )
            row = cur.fetchone()
            conn.commit()
            return row

def updateStudentEmail(student_id, new_email):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                'SELECT * FROM "Part1"."updateStudentEmail"(%s, %s)',
                (student_id, new_email),
            )
            row = cur.fetchone()
            conn.commit()
            return row

def deleteStudent(student_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM "Part1"."deleteStudent"(%s)', (student_id,))
            row = cur.fetchone()
            conn.commit()
            return row

if __name__ == "__main__":
    print("Initial:", getAllStudents())
    print("Insert :", addStudent("Ada", "Lovelace", "ada@example.com", "2024-09-01"))
    print("Update :", updateStudentEmail(1, "johnny.doe@example.com"))  # adjust ID if needed
    print("Delete :", deleteStudent(2))                                  # adjust ID if needed
    print("Final  :", getAllStudents())
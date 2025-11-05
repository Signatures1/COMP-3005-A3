import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from pprint import pprint
load_dotenv()

def get_connection():
    """
    Set connection to database 
    """
    return psycopg2.connect(
        host=os.getenv("PGHOST"),           #database address 
        port=os.getenv("PGPORT"),           #database port (5432)
        database=os.getenv("PGDATABASE"),   #database (postgres)
        user=os.getenv("PGUSER"),           #username for database
        password=os.getenv("PGPASSWORD")    #password for databse
    )

def getAllStudents():
    """
    Get all students from the database
    """
    with get_connection() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:   #open database
        cur.execute('SELECT * FROM "Part1".getallstudents()')                           #execute the pre-exisiting function
        return cur.fetchall()                                                           #return the function call

def addStudent(first_name, last_name, email, enrollment_date=None):
    """
    Add a new student to database
    Parameters:
        first_name:         first name
        last_name:          last name
        email:              email 
        enrollment_date:    Date of enrollment
    Returns:
        new student
    """
    with get_connection() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:   #open database
        cur.execute(
            'SELECT * FROM "Part1".addstudent(%s, %s, %s, %s)',                         
            (first_name, last_name, email, enrollment_date),                            #input parameter values that we want to pass in
        )                                                                               #execute the pre-exisiting function
        row = cur.fetchone()                                                            #fetch new row
        conn.commit()                                                                   #solidify new addition
        return row                                                                      #return new student

def updateStudentEmail(student_id, new_email):
    """
    Update existing student email address by id
    Parameters:
        student_id : ID of student update
        new_email  : New email address
    Returns:
        Updated student(with email changed)
    """
    with get_connection() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:   #open databse
        cur.execute(
            'SELECT * FROM "Part1".updatestudentemail(%s, %s)',
            (student_id, new_email),                                                    #input parameter values that we want to pass in
        )                                                                               #execute the pre-exisiting function
        row = cur.fetchone()                                                            #updated student
        conn.commit()                                                                   #solidify change
        return row                                                                      #return the updated student

def deleteStudent(student_id):
    """
    Delete student database by id
    Parameters:
        student_id: ID student to delete
    Returns:
        deleted student
    """
    with get_connection() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:   #open database
        cur.execute(
            'SELECT * FROM "Part1".deletestudent(%s)', 
            (student_id,)                                                               #input parameter values that we want to pass in
        )                                                                               #execute pre-exisiting function
        row = cur.fetchone()                                                            #deleted student
        conn.commit()                                                                   #solidify change
        return row                                                                      #return deleted student

if __name__ == "__main__":
    """
    TESTING AREA — readable, toggleable, and safe
    """

    # ---- Toggle tests here (True/False) ----
    RUN_LIST_BEFORE   = True
    RUN_ADD_TEMP      = True
    RUN_UPDATE_TEMP   = True
    RUN_DELETE_TEMP   = True
    RUN_DUP_EMAIL_ERR = True   # expect error (uses seeded john.doe@example.com)
    RUN_BAD_ID_UPD    = True   # expect error
    RUN_BAD_ID_DEL    = True   # expect error
    RUN_LIST_AFTER    = True

    # ---- Helpers ----
    def banner(title: str):
        print("\n" + "=" * 70)
        print(title)
        print("=" * 70)
    def show_rows(title: str, rows):
        banner(title)
        for r in rows:
            pprint(dict(r))
    def call_and_show(title: str, fn, *args):
        banner(title)
        res = fn(*args)
        if isinstance(res, list):
            for r in res:
                pprint(dict(r))
        else:
            pprint(dict(res))
        return res
    def expect_db_error(title: str, fn, *args):
        banner(f"{title} (expecting error)")
        try:
            res = fn(*args)
            print("Expected an error but got:", res)
        except psycopg2.Error as e:
            print("Caught expected DB error:")
            print(e.pgerror or str(e))
        except Exception as e:
            print("Caught expected error (non-DB):", e)
    temp_row = None 

    try:
        conn = get_connection()
        print("Success")
        conn.close()

        if RUN_LIST_BEFORE:
            show_rows("Initial students", getAllStudents())

        #1 add temp student
        if RUN_ADD_TEMP:
            temp_row = call_and_show(
                "Add temp student",
                addStudent, "Temp", "User", "temp.user@example.com", None)
            
            show_rows("Updated(ADD) students", getAllStudents()) #show table update

        #2 update temp student email (uses returned ID)
        if RUN_UPDATE_TEMP:
            call_and_show(
                "Update temp email",
                updateStudentEmail, temp_row["student_id"], "updated@update.com"
            )
            show_rows("Updated(update-email) students", getAllStudents()) #show table update

        #3 delete temp student
        if RUN_DELETE_TEMP:
            call_and_show(
                "Delete temp student",
                deleteStudent, temp_row["student_id"])
            show_rows("Updated(DELETE) students", getAllStudents()) #show table update
        temp_row = None  

        #4 TEST CASE: duplicate email insert
        if RUN_DUP_EMAIL_ERR:
            expect_db_error(
                "Duplicate email insert",
                addStudent, "John", "Clone", "john.doe@example.com", None
            )

        #5 TEST CASE: update non-existing ID
        if RUN_BAD_ID_UPD:
            expect_db_error(
                "Update non-existent ID",
                updateStudentEmail, 999, "nobody@example.com"
            )

        #6 TEST CASE: delete non-existing ID
        if RUN_BAD_ID_DEL:
            expect_db_error(
                "Delete non-existent ID",
                deleteStudent, 999)

        #7 AFTER ALL TESTS
        if RUN_LIST_AFTER:
            show_rows("Final students", getAllStudents())
        
        print("PROGRAM")
    except psycopg2.Error as e:
        print(f"Error connecting to database: {e}")
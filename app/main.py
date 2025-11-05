import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
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
    TESTING AREA
    """
    try:
        conn = get_connection()             #VERIFY CONNECTION
        print("Success")                

        print(getAllStudents())             #TEST PRINT (RUN THIS FIRST)

        #TEST 1 ADD STUDENT(UNCOMMENT THE TWO PRINTS UNDER THIS COMMENT TO TEST)  
        #print(addStudent("firstname", "lastname", "firstnamelastname@gmail.com", "2025-11-05"))
        #print(getAllStudents())

        #TEST 2 EDIT STUDENT EMAIL(UNCOMMENT THE TWO PRINTS UNDER THIS COMMENT TO TEST)
        #print(updateStudentEmail(2, "testing@gmail.com"))
        #print(getAllStudents())

        #TEST 3 DELETE STUDENT(UNCOMMENT THE TWO PRINTS UNDER THIS COMMENT TO TEST)
        #print(deleteStudent(1))
        #print(getAllStudents())

        #TEST 4 FOR PRE-EXISTING EMAIL(UNCOMMENT THE TWO PRINTS UNDER THIS COMMENT TO TEST)
        #print(addStudent("firstname", "lastname", "firstnamelastname@gmail.com", "2025-11-05"))
        #print(getAllStudents())

        #TEST 5 SAME EMAIL EDIT(UNCOMMENT THE TWO PRINTS UNDER THIS COMMENT TO TEST)
        #print(updateStudentEmail(2, "testing@gmail.com"))
        #print(getAllStudents())

        #TEST 6 ID DOESNT EXIST EMAIL EDIT(UNCOMMENT THE TWO PRINTS UNDER THIS COMMENT TO TEST)
        #print(updateStudentEmail(10, "testing@gmail.com"))
        #print(getAllStudents())

        #TEST 7 DELETE STUDENT ID DOESNT EXIST(UNCOMMENT THE TWO PRINTS UNDER THIS COMMENT TO TEST)
        #print(deleteStudent(20))
        #print(getAllStudents())

        conn.close()                        #TERMINATE CONNECTION AT END
        print("Connection closed.")
    except psycopg2.Error as e:             #PROGRAM FAILED
        print(f"❌ Error connecting to database: {e}")
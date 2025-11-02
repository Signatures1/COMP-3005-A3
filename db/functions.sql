-- Ensure we’re operating in the right schema
SET search_path TO "Part1";

-- Clean re-run: drop any old versions (unquoted names are stored lowercase)
DROP FUNCTION IF EXISTS get_all_students();
DROP FUNCTION IF EXISTS add_student(text, text, text, date);
DROP FUNCTION IF EXISTS update_student_email(integer, text);
DROP FUNCTION IF EXISTS delete_student(integer);

--GET ALL STUDENTS FUNCTION--
CREATE OR REPLACE FUNCTION getAllStudents()
RETURNS SETOF students
LANGUAGE plpgsql
AS $$
  BEGIN
    --SELECT full table--
    RETURN QUERY
    SELECT *
    FROM students
    ORDER BY student_id;
  END;
$$;

--ADD STUDENT FUNCTION--
CREATE OR REPLACE FUNCTION addStudent(
  n_first_name      TEXT, 
  n_last_name       TEXT, 
  n_email           TEXT, 
  n_enrollment_date DATE DEFAULT CURRENT_DATE
)
RETURNS SETOF students
LANGUAGE plpgsql
AS $$
  BEGIN
    --CHECK IF EMAIL EXISTS--
    IF EXISTS(SELECT 1 FROM students WHERE email = n_email) THEN 
      RAISE EXCEPTION 'Email % already exists', n_email;
    END IF;

    --ADDING student--
    RETURN QUERY
    INSERT INTO students (first_name, last_name, email, enrollment_date)
    VALUES (n_first_name, n_last_name, n_email, n_enrollment_date)
    RETURNING *;
  END;
$$;

--UPDATE STUDENT EMAIL FUNCTION--
CREATE OR REPLACE FUNCTION updateStudentEmail(
  n_student_id    INT, 
  n_new_email     TEXT
)
RETURNS SETOF students
LANGUAGE plpgsql
AS $$
  BEGIN
    --CHECK if student exists--
    IF NOT EXISTS (SELECT 1 FROM students WHERE student_id = n_student_id) THEN 
      RAISE EXCEPTION 'Student with ID % does not exist', n_student_id;
    END IF;

    --CHECK if email exists for another student--
    IF EXISTS (SELECT 1 FROM students WHERE email = n_new_email AND student_id != n_student_id) THEN
      RAISE EXCEPTION 'Email % already in use for another student', n_new_email;
    END IF;

    --UPDATE email--
    RETURN QUERY
    UPDATE students
    SET email = n_new_email
    WHERE student_id = n_student_id
    RETURNING *;
  END;
$$;

--DELETE STUDENT FUNCTION--
CREATE OR REPLACE FUNCTION deleteStudent(
  n_student_id  INT
)
RETURNS SETOF students
LANGUAGE plpgsql
AS $$
  BEGIN
    --CHECK if student exists--
    IF NOT EXISTS (SELECT 1 FROM students WHERE student_id = n_student_id) THEN
      RAISE EXCEPTION 'Student with ID % does not exist', n_student_id;
    END IF;

    --DELETING student--
    RETURN QUERY
    DELETE FROM students
    WHERE student_id = n_student_id
    RETURNING *;
  END;
$$;
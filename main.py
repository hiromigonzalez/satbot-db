import psycopg2
import bcrypt
from getpass import getpass

# Database connection parameters
db_params = {
    'dbname': 'postgres',
    'user': 'postgres.jswvecjagqmromsmvpsc',
    'password': 'hiromiandjay2024',
    'host': 'aws-0-us-west-1.pooler.supabase.com'
}

def connect_db(params):
    try:
        conn = psycopg2.connect(**params)
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

def verify_admin(email, password):
    conn = connect_db(db_params)
    if conn is not None:
        with conn.cursor() as cur:
            cur.execute("SELECT password, role FROM users WHERE email = %s", (email,))
            user_data = cur.fetchone()
            if user_data and user_data[0] == password:
                return user_data[1] == 'p'  # Returns True if the user is an admin
    return False

def admin_operations(conn):  # Add 'conn' as a parameter to accept the database connection
    print("1. Add User\n2. Add Course\n3. Add Intent\n4. Add Document\n5. View Chat Logs\n6. Exit")
    choice = input("Enter your choice: ")
    if choice == '1':
        # Add User operation
        pass
    elif choice == '2':
        add_course(conn)  # Assuming you have or will create this function
    elif choice == '3':
        add_intent(conn)  # Assuming you have or will create this function
    elif choice == '4':
        # Add Document operation
        pass
    elif choice == '5':
        # View Chat Logs operation
        pass
    elif choice == '6':
        return
    else:
        print("Invalid choice. Please try again.")

def add_course(conn):
    course_name = input("Enter course name: ")
    year = input("Enter year: ")
    semester = input("Enter semester: ")
    course_code = input("Enter course code: ")
    with conn.cursor() as cur:
        cur.execute("INSERT INTO courses (course_name, year, semester, course_code) VALUES (%s, %s, %s, %s)",
                    (course_name, year, semester, course_code))
        conn.commit()
        print("Course added successfully.")

def add_intent(conn):
    question = input("Enter question: ")
    answer = input("Enter answer: ")
    # Assuming the intent is not directly related to a specific course for simplicity
    # If it is, you'd need to fetch the course_id based on user input
    course_id = input("Enter course ID (leave blank if not applicable): ")
    course_id = None if course_id == "" else int(course_id)
    with conn.cursor() as cur:
        cur.execute("INSERT INTO intents (question, answer, course_id) VALUES (%s, %s, %s)",
                    (question, answer, course_id))
        conn.commit()
        print("Intent added successfully.")

def main():
    email = input("Enter email: ")
    password = getpass("Enter password: ")
    if verify_admin(email, password):
        print("Authentication successful. Welcome, admin!")
        conn = connect_db(db_params)  # Ensure you have a connection before operations
        if conn:
            while True:
                admin_operations(conn)  # Pass the connection to the function
                if input("Perform another operation? (y/n): ").lower() != 'y':
                    conn.close()
                    break
    else:
        print("Authentication failed. Please check your credentials.")

if __name__ == "__main__":
    main()
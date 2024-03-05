import psycopg2
from getpass import getpass 
import json

# Database connection parameters
db_params = {
    'dbname': 'postgres',
    'user': 'postgres.jswvecjagqmromsmvpsc',
    'password': 'hiromiandjay2024',
    'host': 'aws-0-us-west-1.pooler.supabase.com'
}

def connect_db(params):
    """
    Connects to the PostgreSQL database using the parameters.

    Parameters:
    - params (dict): A dictionary containing database connection parameters such as dbname, user, password, and host.
    
    Returns:
    - psycopg2.connection: A connection object to the PostgreSQL database on success.
    - None: If connection fails.
    """
    try:
        conn = psycopg2.connect(**params)
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

def verify_admin(email, password):
    """
    Verifies if the given email and password belong to an admin (role = 'p').

    Parameters:
    - email (str): The admin's email address.
    - password (str): The admin's password.
    
    Returns:
    - bool: True if the user is verified as an admin/professor, False otherwise.
    """
    conn = connect_db(db_params)
    if conn is not None:
        with conn.cursor() as cur:
            cur.execute("SELECT password, role FROM users WHERE email = %s", (email,))
            user_data = cur.fetchone()
            if user_data and user_data[0] == password:
                return user_data[1] == 'p'  # 'p' indicates an admin role
    return False

def search(conn):
    conn = connect_db(db_params)
    word = input("Enter word to search: ")
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM intents WHERE question ~jdoe@sandiego.edu %s", (word,))
        result = cur.fetchall()
        results = [list(i) for i in result]
    print(results)

def collect_user_input_for_table(table_info, conn=None):
    """
    Collects user input for each column specified in table_info.

    Parameters:
    - table_info (dict): A dictionary containing information about the table and its columns.
    - conn (psycopg2.connection): A connection object to the PostgreSQL database.
    
    Returns:
    - dict: A dictionary of column-value pairs based on user input.
    """
    columns = table_info["columns"]
    user_data = {}

    if 'question' in columns:  # Assuming this means we're dealing with the 'intents' table
        display_courses(conn)

    for column, data_type in columns.items():
        while True:
            user_input = input(f"Enter {column}: ")
            try:
                if data_type == int:
                    user_data[column] = int(user_input)
                elif data_type == float:
                    user_data[column] = float(user_input)
                else:
                    user_data[column] = user_input  # Default to string
                break
            except ValueError:
                print(f"Invalid input for {column}. Please enter a {data_type.__name__}.")

    return user_data

def display_courses(conn):
    """
    Fetches and displays a list of courses from the database.
    
    Parameters:
    - conn (psycopg2.connection): A connection object to the PostgreSQL database.
    """
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT course_id, course_code, course_name, year, semester FROM courses ORDER BY course_code")
            courses = cur.fetchall()
            print("Available courses:")
            for course in courses:
                # Display course details including code, year, semester, and ID
                print(f"{course[1]}: {course[3]} {course[4]} (ID: {course[0]})")
    except Exception as e:
        print(f"Error fetching courses: {e}")

def insert_data_into_table(conn, table_name, user_data):
    """
    Inserts the provided data into the specified table.

    Parameters:
    - conn (psycopg2.connection): A connection object to the PostgreSQL database.
    - table_name (str): The name of the table where data will be inserted.
    - user_data (dict): A dictionary containing the data to be inserted into the table.
    """
    columns_str = ", ".join(user_data.keys())
    placeholders = ", ".join(["%s"] * len(user_data))  #Placeholders for query parameters
    values = list(user_data.values())

    try:
        with conn.cursor() as cur:
            sql = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders});"
            cur.execute(sql, values)
            conn.commit()
            print("Entry added successfully.")
    except Exception as e:
        print(f"Error adding entry to the table: {e}")
        conn.rollback()

def collect_document_input(conn):
    """
    Collects user input for document metadata and the path to the document file.

    Parameters:
    - conn (psycopg2.connection): A connection object to the PostgreSQL database.
    """
    document_data = {}
    document_data['title'] = input("Enter document title: ")
    document_data['description'] = input("Enter document description: ")
    display_courses(conn)
    course_id_input = input("Enter course ID (optional, press Enter to skip): ")

    # Convert course_id to an integer if provided, or set to None if not
    course_id = int(course_id_input) if course_id_input.isdigit() else None

    file_path = input("Enter path to document file: ")

    return {
        "metadata": document_data,
        "file_path": file_path,
        "course_id": course_id
    }

def insert_document(conn, document_data):
    """
    Inserts the document and its metadata into the documents table.

    Parameters:
    - conn (psycopg2.connection): A connection object to the PostgreSQL database.
    - document_data (dict): A dictionary containing the document's metadata, file path, and course_id.
    """
    with open(document_data['file_path'], 'rb') as file:
        document_content = file.read()
        metadata = json.dumps(document_data['metadata'])
        
        with conn.cursor() as cur:
            sql = """
                INSERT INTO documents (document_data, document_content, course_id) 
                VALUES (%s, %s, %s)
            """
            cur.execute(sql, (metadata, document_content, document_data['course_id']))
            conn.commit()
            print("Document added successfully.")

def add_document_to_table(conn):
    """
    Parameters:
    - conn (psycopg2.connection): A connection object to the PostgreSQL database.
    """
    # For simplicity, this is hardcoded to handle document uploads
    print("Adding a new document entry.")
    document_data = collect_document_input(conn)
    if document_data:
        insert_document(conn, document_data)

def add_entry_to_table(conn):
    """
    Prompts the user to select a table and then collects and inserts data for that table.

    Parameters:
    - conn (psycopg2.connection): A connection object to the PostgreSQL database.
    """
    tables_info = {
        "1": {
            "name": "users",
            "columns": {
                "first_name": str,
                "last_name": str,
                "username": str,
                "password": str,
                "email": str,
                "role": str
            }
        },
        "2": {
            "name": "intents",
            "columns": {
                "question": str,
                "answer": str,
                "course_id": int
            }
        },
        "3": {
            "name": "courses",
            "columns": {
                "course_name": str,
                "year": int,
                "semester": str,
                "course_code": str
            }
        }
    }

    print("Select the table you want to add an entry to:")
    print("1. Users")
    print("2. Intents")
    print("3. Courses")
    table_choice = input("Enter your choice (number): ")


    if table_choice not in tables_info:
        print("Invalid choice. Returning to main menu.")
        return

    table_info = tables_info[table_choice]
    user_data = collect_user_input_for_table(table_info, conn)
    insert_data_into_table(conn, table_info["name"], user_data)

def admin_operations(conn):
    """
    Displays admin operations and handles user selection.

    Parameters:
    - conn (psycopg2.connection): A connection object to the PostgreSQL database.
    """
    while True:
        print("1. Add entry to a table\n2. Add a document to database \n3. Query Table\n4. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            add_entry_to_table(conn)
        elif choice == '2':
            add_document_to_table(conn)
        elif choice == '3':
            search(conn)
        elif choice == '4':
            return
        else:
            print("Invalid choice. Please try again.")

def main():
    """
    Main function to run the admin operations.
    """
    email = input("Enter email: ")
    password = getpass("Enter password: ")
    if verify_admin(email, password):
        print("Authentication successful. Welcome, admin!")
        conn = connect_db(db_params)
        if conn:
            admin_operations(conn)
            conn.close()
    else:
        print("Authentication failed. Please check your credentials.")

if __name__ == "__main__":
    main()

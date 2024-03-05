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
    print("1. Add entry to a table\n2. Query table\n3. Exit")
    choice = input("Enter your choice: ")
    if choice == '1':
        pass
    elif choice == '2':
<<<<<<< HEAD
        search(conn)
=======
        pass
>>>>>>> 0ccd1a9501dd3527adc1eb714e773bc695d61f02
    elif choice == '3':
        return
    else:
        print("Invalid choice. Please try again.")

<<<<<<< HEAD

def search(conn):
    conn = connect_db(db_params)
    word = input("Enter word to search: ")
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM intents WHERE question LIKE %s", (word,))
        result = cur.fetchall()
        results = [list(i) for i in result]
    print(results)

=======
>>>>>>> 0ccd1a9501dd3527adc1eb714e773bc695d61f02

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
import psycopg2
from time import sleep
# from psycopg2.extras import RealDictCursor

conn = psycopg2.connect(
    database="python_crud", 
    user="postgres", 
    password="admin", 
    host="localhost", 
    port="5432"
)
cur = conn.cursor()

def create_user(name, email):
    try:
        cur.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
        conn.commit()
        print(f"User {name} created successfully.")
    except psycopg2.Error as e:
        print(f"Error creating user: {e}")

def read_users():
    try:
        cur.execute("SELECT * FROM users")
        rows = cur.fetchall()
        if rows:
            for row in rows:
                print(f"ID: {row[0]}, Name: {row[1]}, Email: {row[2]}")
        else:
            print("No users found.")
    except psycopg2.Error as e:
        print(f"Error reading users: {e}")

def update_user(user_id, name, email):
    try:
        cur.execute("UPDATE users SET name = %s, email = %s WHERE id = %s", (name, email, user_id))
        conn.commit()
        if cur.rowcount > 0:
            print(f"User ID {user_id} updated successfully.")
        else:
            print(f"No user found with ID {user_id}.")
    except psycopg2.Error as e:
        print(f"Error updating user: {e}")

def delete_user(user_id):
    try:
        cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()
        if cur.rowcount > 0:
            print(f"User ID {user_id} deleted successfully.")
        else:
            print(f"No user found with ID {user_id}.")
    except psycopg2.Error as e:
        print(f"Error deleting user: {e}")


def is_user_existing(user_id):
    try:
        # with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            user = cur.fetchone()

            print("\n ------ USER INFORMATION: ------")
            print(f"\n ID: {user[0]}")
            print(f"\n Name: {user[1]}")
            print(f"\n Email: {user[2]} \n")

            if user:
                return True
            else:
                return False

    except psycopg2.Error as e:
        print(f"Error finding user with the id: {e}")

def menu():
    while True:
        print("\n--- CRUD Menu ---")
        print("1. Create User")
        print("2. Read Users")
        print("3. Update User")
        print("4. Delete User")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            print("\n ------ CREATE USER ------")

            name = input("Enter name: ")
            email = input("Enter email: ")
            create_user(name, email)
        elif choice == '2':
            print("\n ------ ALL USERS ------")
            read_users()
        elif choice == '3':
            print("\n ------ UPDATE USER ------")
            user_id = input("Enter user ID to update: ")

            is_existing = is_user_existing(user_id)

            if not is_existing:
                print("User does not exist!")
                continue

            name = input("Enter new name: ")
            email = input("Enter new email: ")
            update_user(user_id, name, email)
        elif choice == '4':
            print("\n ------ REMOVE USER ------")
            
            user_id = input("Enter user ID to delete: ")
            delete_user(user_id)
        elif choice == '5':

            print("\nExiting Application in", end=" ")

            for i in range(3, 0, -1):
                print(f"{i}", end=" ", flush=True)
                sleep(0.8)
            break

        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    menu()

    cur.close()
    conn.close()
import sqlite3

def view_users():
    # Connect to the database
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Retrieve data from the users table
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    # Print the retrieved data
    for user in users:
        print(user)

    # Close the connection
    conn.close()

if __name__ == "__main__":
    view_users()

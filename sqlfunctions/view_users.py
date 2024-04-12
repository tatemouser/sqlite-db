import sqlite3

def view_users():
    # Connect to the database
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Retrieve data from the users table
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    # Print the retrieved data
    print("Users:")
    for user in users:
        print(user)

    # Retrieve data from the items table
    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()

    # Print the retrieved data
    print("\nItems:")
    for item in items:
        print(item)

    # Retrieve data from the checkouts table
    cursor.execute("SELECT * FROM checkouts")
    checkouts = cursor.fetchall()

    # Print the retrieved data
    print("\nCheckouts:")
    for checkout in checkouts:
        print(checkout)

    # Close the connection
    conn.close()

if __name__ == "__main__":
    view_users()

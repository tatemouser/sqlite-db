import sqlite3
import bcrypt
from remove_duplicates import remove_duplicates

def sys_init():
    # Connect to an SQLite database
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Create a table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT,
            first_name TEXT,
            last_name TEXT,
            email TEXT,
            phone TEXT,
            user_type TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            item INTEGER PRIMARY KEY,
            title TEXT,
            type TEXT,
            status TEXT
        )
    ''')


    # Insert some dummy data with hashed passwords
    password1_hash = bcrypt.hashpw(b'secret1', bcrypt.gensalt())
    password2_hash = bcrypt.hashpw(b'secret2', bcrypt.gensalt())
    cursor.execute(
        "INSERT INTO users (username, password, first_name, last_name, email, phone, user_type) VALUES (?, ?, ?, ?, ?, ?, ?)",
        ('user1', password1_hash, 'John', 'Doe', 'john@example.com',
         '1234567890', 'librarian'))
    cursor.execute(
        "INSERT INTO users (username, password, first_name, last_name, email, phone, user_type) VALUES (?, ?, ?, ?, ?, ?, ?)",
        ('user2', password2_hash, 'Jane', 'Smith', 'jane@example.com',
         '0987654321', 'patron'))

    # Commit the changes
    conn.commit()

    # Close the connection
    conn.close()


sys_init()


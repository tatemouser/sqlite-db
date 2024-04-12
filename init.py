import sqlite3
import bcrypt

def sys_init():
    # Connect to an SQLite database
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Create tables if they don't exist
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
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            item_id INTEGER PRIMARY KEY,
            title TEXT,
            type TEXT,
            availability TEXT
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS checkouts (
            checkout_id INTEGER PRIMARY KEY,
            user_id INTEGER,
            item_id INTEGER,
            checkout_date TEXT,
            return_date TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (item_id) REFERENCES items(item_id)
        );
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

    # Insert some dummy data into items table
    cursor.execute(
        "INSERT INTO items (title, type, availability) VALUES (?, ?, ?)",
        ('Book1', 'Book', 'Available'))
    cursor.execute(
        "INSERT INTO items (title, type, availability) VALUES (?, ?, ?)",
        ('DVD1', 'DVD', 'Available'))

    # Insert some dummy data into checkouts table
    cursor.execute(
        "INSERT INTO checkouts (user_id, item_id, checkout_date, return_date) VALUES (?, ?, ?, ?)",
        (1, 1, '2024-04-10', '2024-04-20'))
    cursor.execute(
        "INSERT INTO checkouts (user_id, item_id, checkout_date, return_date) VALUES (?, ?, ?, ?)",
        (2, 2, '2024-04-10', '2024-04-20'))

    # Commit the changes
    conn.commit()

    # Close the connection
    conn.close()

sys_init()

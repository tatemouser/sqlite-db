import sqlite3
import bcrypt

# INITIALIZATION
# CREATE TABLES
# INSERT DATA
# COMMIT CHANGES
# INITLIZE 

def sys_init():
    # Connect to DB and using cursor for interaction 
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
    password1_hash = bcrypt.hashpw(b'Ilovetocode1', bcrypt.gensalt())
    password2_hash = bcrypt.hashpw(b'Ilovetocode2', bcrypt.gensalt())
    password3_hash = bcrypt.hashpw(b'Ilovetocode3', bcrypt.gensalt())
    password4_hash = bcrypt.hashpw(b'Ilovetocode4', bcrypt.gensalt())
    password5_hash = bcrypt.hashpw(b'Ilovetocode5', bcrypt.gensalt())

    # TRADITIONAL WAY TO ADD DATA
        # ADD ITEM
            # cursor.execute(
            #     "INSERT INTO items (title, type, availability) VALUES (?, ?, ?)",
            #     ('Book1', 'Book', 'Available'))
        # ADD USER
            # cursor.execute(
            #     "INSERT INTO users (username, password, first_name, last_name, email, phone, user_type) VALUES (?, ?, ?, ?, ?, ?, ?)",
            #     ('user1', password1_hash, 'John', 'Doe', 'john@example.com',
            #      '1234567890', 'librarian'))

    # ADD DATA TO USERS ITEMS AND CHEKOUTS TABLE
    # ADD 5 USERS
    users = [
        ('user1', password1_hash, 'John', 'Doe', 'john@example.com', '1234567890', 'librarian'),
        ('user2', password2_hash, 'Jane', 'Smith', 'jane@example.com', '0987654321', 'patron'),
        ('user3', password3_hash, 'Alice', 'Johnson', 'alice@example.com', '9876543210', 'patron'),
        ('user4', password4_hash, 'Bob', 'Brown', 'bob@example.com', '0123456789', 'librarian'),
        ('user5', password5_hash, 'Emma', 'Davis', 'emma@example.com', '5555555555', 'patron')
    ]
    cursor.executemany(
        "INSERT INTO users (username, password, first_name, last_name, email, phone, user_type) VALUES (?, ?, ?, ?, ?, ?, ?)",
        users
    )

    # ADD 10 TO ITEMS
    items = [
        ('Long Book', 'Book', 'Not Available'),
        ('Fast Movie', 'DVD', 'Not Available'),
        ('Quick Song', 'CD', 'Available'),
        ('Diary', 'Book', 'Available'),
        ('Quiz Help', 'DVD', 'Available'),
        ('Noahs Song', 'CD', 'Available'),
        ('Bible', 'Book', 'Available'),
        ('Code tutorial', 'DVD', 'Available'),
        ('Hello World', 'CD', 'Available'),
        ('Bible Part 2', 'Book', 'Available')
    ]
    cursor.executemany(
        "INSERT INTO items (title, type, availability) VALUES (?, ?, ?)",
        items
    )

    # Insert some dummy data into checkouts table
    cursor.execute(
        "INSERT INTO checkouts (user_id, item_id, checkout_date, return_date) VALUES (?, ?, ?, ?)",
        (1, 1, '2024-04-10', '2024-04-20'))
    cursor.execute(
        "INSERT INTO checkouts (user_id, item_id, checkout_date, return_date) VALUES (?, ?, ?, ?)",
        (2, 2, '2024-04-10', '2024-04-20'))

    #  Save DB changes (permanent) then ends connection 
    conn.commit()
    conn.close()
sys_init()

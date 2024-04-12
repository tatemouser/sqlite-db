import sqlite3

def remove_duplicates():
    try:
        # Connect to the database
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        # Remove duplicates from the users table
        cursor.execute('''
            DELETE FROM users
            WHERE user_id NOT IN (
                SELECT MIN(user_id)
                FROM users
                GROUP BY username
            )
        ''')

        # Remove duplicates from the items table
        cursor.execute('''
            DELETE FROM items
            WHERE item_id NOT IN (
                SELECT MIN(item_id)
                FROM items
                GROUP BY title, type
            )
        ''')

        # Remove duplicates from the checkouts table
        cursor.execute('''
            DELETE FROM checkouts
            WHERE checkout_id NOT IN (
                SELECT MIN(checkout_id)
                FROM checkouts
                GROUP BY user_id, item_id
            )
        ''')

        # Commit the changes
        conn.commit()

    except sqlite3.Error as e:
        print("SQLite error:", e)

    finally:
        # Close the connection
        if conn:
            conn.close()

# Call the function to remove duplicates
remove_duplicates()

import sqlite3

def remove_duplicates():
    try:
        # Connect to the database
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        # Find duplicate usernames and keep the one with the lowest ID
        cursor.execute('''
            DELETE FROM users
            WHERE user_id NOT IN (
                SELECT MIN(user_id)
                FROM users
                GROUP BY username
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

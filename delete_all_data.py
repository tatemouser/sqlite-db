import sqlite3

def delete_all_data():
    # Connect to the SQLite database
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    try:
        # Delete all rows from the users table
        cursor.execute("DELETE FROM users")
        
        # Commit the changes
        conn.commit()
        
        print("All data deleted successfully from the database.")

    except sqlite3.Error as e:
        print("Error deleting data:", e)

    finally:
        # Close the connection
        conn.close()

# Call the function to delete all data
delete_all_data()

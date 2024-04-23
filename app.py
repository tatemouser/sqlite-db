from flask import Flask, render_template, request, jsonify, redirect, session
from user_manage import login, User
from init import sys_init
from datetime import datetime
import sqlite3
from datetime import datetime, timedelta
import bcrypt




app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Define a function to connect to the SQLite database
def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

with app.app_context():
    sys_init()

@app.route('/')
def index():
    if request.args:
        return render_template('index.html', messages=request.args['messages'])
    else:
        return render_template('index.html', messages='')

@app.route('/ajaxkeyvalue', methods=['POST'])
def ajax():
    data = request.json  # Assuming the AJAX request sends JSON data
    print(data)
    # Process the data
    username = data['username']
    password = data['password']

    print(username)
    print(password)

    user = login(username, password)
    if not user:
        response_data = {'status': 'fail'}
    else:
        session['logged_in'] = True
        session['username'] = username
        session['user'] = {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'phone': user.phone,
            'user_type': user.user_type
        }

        response_data = {'status': 'ok', 'user': user.to_json()}

    return jsonify(response_data)

@app.route('/profile')
def profile():
    user_data = session.get('user')

    if user_data:
        # Reconstruct the user object
        user = User(user_id=user_data['id'], username=user_data['username'],
                    password_hash='', first_name=user_data['first_name'],
                    last_name=user_data['last_name'], email=user_data['email'],
                    phone=user_data['phone'], user_type=user_data['user_type'])

        if user.user_type == 'librarian':
            return render_template('librarian_profile.html', user_info=user_data)
        elif user.user_type == 'patron':
            return render_template('patron_profile.html', user_info=user_data)
        else:
            return "Unknown user type"
    else:
        return redirect('/?messages=Please login again!')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        user_data = session.get('user')
        if user_data:
            return render_template('search.html', user_info=user_data)
        else:
            return "Error: User information not found"
    elif request.method == 'POST':
        # Get the search query from the form
        title = request.form['title']

        # Create a parameterized query
        query = "SELECT * FROM items WHERE title LIKE ?"

        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Execute the query with safe parameters with wildcards
        cursor.execute(query, ('%' + title + '%',))

        items = cursor.fetchall()
        conn.close()

        # Render the search results
        user_data = session.get('user')
        if user_data:
            return render_template('search.html', user_info=user_data, items=items)
        else:
            return "Error: User information not found"


















@app.route('/filter', methods=['POST'])
def filter_items():
    item_type = request.form['item_type']
    
    # Query the database for items of the selected type
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items WHERE type = ?", (item_type,))
    items = cursor.fetchall()
    conn.close()
    
    # Render the filtered items
    user_data = session.get('user')
    if user_data:
        return render_template('search.html', user_info=user_data, items=items)
    else:
        return "Error: User information not found"
    


@app.route('/checkout', methods=['POST'])
def checkout():
    # Retrieve user_id from the form data
    user_id = request.form.get('user_id')

    checked_items = request.form.getlist('checked_items')
    
    if not checked_items:
        return "No items selected for checkout."
    
    # Update the status of checked items to 'Not Available'
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get current date (without time)
    checkout_date = datetime.now().strftime('%Y-%m-%d')  
    
    # Calculate return date (14 days from checkout date)
    return_date = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
    
    # Check if there are already 5 checkouts for the user
    cursor.execute("SELECT COUNT(*) FROM checkouts WHERE user_id = ?", (user_id,))
    # Fetch the result of the COUNT query and extract the count value
    num_checkouts = cursor.fetchone()[0]
    
    if num_checkouts >= 5:
        conn.close()
        return redirect('/search')
    
    for item_id in checked_items:
        cursor.execute("UPDATE items SET availability = ? WHERE item_id = ?", ('Not Available', item_id))
        
        # Insert a new row into the checkouts table with a default return_date
        cursor.execute("INSERT INTO checkouts (user_id, item_id, checkout_date, return_date) VALUES (?, ?, ?, ?)",
                       (user_id, item_id, checkout_date, return_date))
        
    conn.commit()
    conn.close()

    
    # Redirect back to the search page after checkout
    return redirect('/search')


@app.route('/show_all_users', methods=['POST'])
def show_all_users():
    # Query all items from the database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()

    # Render all items
    user_data = session.get('user')
    if user_data:
        return render_template('search.html', user_info=user_data, users=users)
    else:
        return "Error: User information not found"

@app.route('/add_item', methods=['POST'])
def add_item():
    # Get the form data with validation (consider adding more as needed)
    title = request.form.get('title', '').strip()  # Remove leading/trailing whitespaces
    item_type = request.form.get('type', '').strip()
    availability = request.form.get('availability', 'Available').strip()

    # Create a parameterized query
    query = "INSERT INTO items (title, type, availability) VALUES (?, ?, ?)"

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Execute the query with safe parameters
    cursor.execute(query, (title, item_type, availability))
    conn.commit()
    conn.close()

    # Redirect to the same page or another page
    return redirect('/search')  # Adjust the URL as needed


@app.route('/add_user', methods=['POST'])
def add_user():
    # Get the form data with basic validation (consider adding more as needed)
    username = request.form.get('username', '').strip()
    first_name = request.form.get('first_name', '').strip()
    last_name = request.form.get('last_name', '').strip()
    email = request.form.get('email', '').strip()
    phone = request.form.get('phone', '').strip()  # Assuming phone is not mandatory
    user_type = request.form.get('user_type', '').strip()

    # Create a parameterized query
    query = "INSERT INTO users (username, password, first_name, last_name, email, phone, user_type) VALUES (?, ?, ?, ?, ?, ?, ?)"

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # TODO:
    # Hash the password before storing it (crucial!)
    # Replace this with your preferred hashing algorithm (e.g., bcrypt)
    password1_hash = bcrypt.hashpw(b'secret1', bcrypt.gensalt())
    hashed_password = password1_hash  # Implement a secure hashing function

    # Execute the query with safe parameters
    cursor.execute(query, (username, hashed_password, first_name, last_name, email, phone, user_type))
    conn.commit()
    conn.close()

    # Redirect to the same page or another page (consider success/error message)
    return redirect('/search')  # Adjust URL as needed

@app.route('/find_user', methods=['POST'])
def find_user():
    user_id = request.form.get('user_id')

    # Create a parameterized query
    query = "SELECT * FROM users WHERE user_id = ?"

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Execute the query with safe parameters
    cursor.execute(query, (user_id,))
    users = cursor.fetchall()
    conn.close()

    # Render the filtered users
    user_data = session.get('user')
    if user_data:
        return render_template('search.html', user_info=user_data, users=users)
    else:
        return "Error: User information not found"


@app.route('/find_checkouts', methods=['POST'])
def find_checkouts():
    user_id = request.form.get('user_id')

    # Query the database for items checked out by the user (parameterized)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM checkouts WHERE user_id = ?", (user_id,))
    checkouts = cursor.fetchall()
    conn.close()

    # Get user info from session
    user_info = session.get('user')

    # Improved get_item_title function using a parameterized query
    def get_item_title(item_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT title FROM items WHERE item_id = ?"
        cursor.execute(query, (item_id,))
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else "Unknown"

    # Render the checkouts information with the secure get_item_title function
    return render_template('search.html', user_info=user_info, checkouts=checkouts, get_item_title=get_item_title)








if __name__ == '__main__':
    app.run(debug=True)

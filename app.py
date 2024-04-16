from flask import Flask, render_template, request, jsonify, redirect, session
from user_manage import login, User
from init import sys_init
from datetime import datetime
import sqlite3


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
        
        # Query the database for items with matching title
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM items WHERE title LIKE ?", ('%' + title + '%',))
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
    checked_items = request.form.getlist('checked_items')
    
    if not checked_items:
        return "No items selected for checkout."
    
    # Update the status of checked items to 'Not Available'
    conn = get_db_connection()
    cursor = conn.cursor()
    checkout_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Get current date and time
    user_id = session.get('user').get('user_id')  # Get the user_id of the current user
    
    for item_id in checked_items:
        cursor.execute("UPDATE items SET availability = ? WHERE item_id = ?", ('Not Available', item_id))
        
        # Insert a new row into the checkouts table
        cursor.execute("INSERT INTO checkouts (user_id, item_id, checkout_date) VALUES (?, ?, ?)",
                       (user_id, item_id, checkout_date))
        
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
    # Get the form data
    title = request.form.get('title')
    item_type = request.form.get('type')
    availability = request.form.get('availability', 'Available')  # Default to 'Available' if not provided

    # Insert the new item into the items table
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO items (title, type, availability) VALUES (?, ?, ?)", (title, item_type, availability))
    conn.commit()
    conn.close()

    # Redirect to the same page or another page
    return redirect('/search')  # Adjust the URL as needed

@app.route('/add_user', methods=['POST'])
def user():
    # Get the form data
    username = request.form.get('username')
    password = request.form.get('password')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    user_type = request.form.get('user_type')
    # TODO: HASH PASSWORD
    # Insert the new item into the items table
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password, first_name, last_name, email, phone, user_type) VALUES (?, ?, ?, ?, ?, ?, ?)", (username, password, first_name, last_name, email, phone, user_type))
    conn.commit()
    conn.close()

    # Redirect to the same page or another page
    return redirect('/search')  # Adjust the URL as needed



@app.route('/find_user', methods=['POST'])
def find_user():
    user_id = request.form.get('user_id')
    
    # Query the database for the user with the specified user_id
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
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
    
    # Query the database for items checked out by the user
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM checkouts WHERE user_id = ?", (user_id,))
    checkouts = cursor.fetchall()
    conn.close()
    
    # Get user_info from session
    user_info = session.get('user')
    
    # Render the checkouts information
    return render_template('search.html', user_info=user_info, checkouts=checkouts)









if __name__ == '__main__':
    app.run(debug=True)

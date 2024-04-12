from flask import Flask, render_template, request, jsonify, redirect, session
from user_manage import login, User
from init import sys_init

app = Flask(__name__)

app.secret_key = 'your_secret_key'

with app.app_context():
   sys_init()


@app.route('/')
def index():
   if request.args:
      return render_template(
          'index.html', messages=json.loads(request.args['messages']))
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
          'user_id': user.user_id,
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
    user = User(
        user_id=user_data['user_id'],
        username=user_data['username'],
        password_hash='',
        first_name=user_data['first_name'],
        last_name=user_data['last_name'],
        email=user_data['email'],
        phone=user_data['phone'],
        user_type=user_data['user_type'])

    # Replace this section with conditional rendering based on user_type
    if user.user_type == 'librarian':
      return render_template('librarian_profile.html', user_info=user)
    else:
      return render_template('patron_profile.html', user_info=user)
  else:
    return redirect('/', messages="Please login again!")


@app.route('/logout')
def logout():
   session.clear()
   return redirect('/')


if __name__ == '__main__':
   app.run(debug=True)

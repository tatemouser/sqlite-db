import sqlite3
import bcrypt

# USER CLASS FOR OBJECTS
# HASH PASSWORD
# VERIFY PASSWORD
# LOGIN FUNCTION



class User:
   #  Initialize attributes when 'user' object is created
   def __init__(self, user_id, username, password_hash, first_name, last_name,
                email, phone, user_type):
      self.id = user_id
      self.username = username
      self.password_hash = password_hash
      self.first_name = first_name
      self.last_name = last_name
      self.email = email
      self.phone = phone
      self.user_type = user_type

   # Converts attrbutes to a JSON format for easy serialization
   # Allows for easy transmission of data between server and client components
   def to_json(self):
      user_json = {
          "id": self.id,
          "username": self.username,
          "first_name": self.first_name,
          "last_name": self.last_name,
          "email": self.email,
          "phone": self.phone,
          "user_type": self.user_type
      }
      return user_json





# NOTE: Salt is tandom value added ot password for added hashing security
def hash_password(password):
   # Encode the password to bytes using UTF-8 encoding
   # Generate a salt using bcrypt's gensalt function
   return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(password, hashed_password):
   # Hash comparison
   return bcrypt.checkpw(password.encode('utf-8'), hashed_password)





# login function with hashed passwords
def login(username, password):
   conn = sqlite3.connect('users.db')
   cursor = conn.cursor()

   # Execute SQL query w/ username then fetch first row
   query = "SELECT * FROM users WHERE username = ?"
   cursor.execute(query, (username,))
   user_data = cursor.fetchone()

   # If user data is retrieved then compare two hashes
   if user_data:
      stored_password_hash = user_data[2]
      if verify_password(password, stored_password_hash):
         # Create a User object with the retrieved user data
         user = User(user_data[0], user_data[1], user_data[2], user_data[3],
                     user_data[4], user_data[5], user_data[6], user_data[7])
      else:
         user = None
   else:
      user = None

   conn.close()

   # Return the user object based off of hash comparison
   return user


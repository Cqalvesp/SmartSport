import os
import pymysql
from smartsportDB import db_connection

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token

app = Flask(__name__)
CORS(app, origins=["Webflow URL"])

bcrypt = Bcrypt(app)
app.congif["JWT_SECRET_KEY"] = os.environ.get('FLASK_SECRET_KEY', 'default-secret-key')
jwt = JWTManager(app)

# Route for User Registration
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    firstname = data.get('firstname', None)
    lastname = data.get('lastname', None)

    if (username and email and password):
        return jsonify({"error": "Username, Email, and Password are required fields"}), 400

    try:
        conn = db_connection()
        cursor = conn.cursor()

        # Check for duplicate username
        cursor.execute("SELECT UserID FROM users WHERE Username = %s", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            cursor.close()
            conn.close()
            return jsonify({"error" : "This Username is already taken"}), 409

        # Hashing password before it is stored in database
        hashed_pass = bcrypt.generate_password_hash(password).decode('utf-8')

        # Add user to database
        cursor.execute("""
                INSERT INTO users (Username, Email, Password, FirstName, LastName)
                VALUES (%s, %s, %s, %s, %s) """, (username, email, password, firstname, lastname))
        
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message" : "User registered successfully!"}), 201

    except pymysql.MySQLError as err:
        return jsonify({"error" : str(err)}), 500


# Route for User Login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not (username and password):
        return jsonify({"error" : "Username and Password are required"}), 400
    
    try: 
        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user WHERE username = %s", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and bcrypt.check_password_hash(user['password'], password):
            # Create JWT Token for authentication
            access_token = create_access_token(identity=user['id'])
            return jsonify(access_token=access_token), 200
        else:
            return jsonify({"error" : "Password or Username is incorrect"}), 401
        
    except pymysql.MySQLError as err:
        return jsonify({"error" : str(err)}), 500

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, request, jsonify
from smartsportDB import get_db_connection  
import bcrypt

app = Flask(__name__)

@app.route('/register', methods=['POST'])
def register_user():
    # Get data from the request
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"error": "Missing required fields"}), 400
    
    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Check if username already exists
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        return jsonify({"error": "Username already exists"}), 409  # Conflict, duplicate user

    # Insert new user into the database
    cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", 
                   (username, email, hashed_password))
    connection.commit()
    cursor.close()

    return jsonify({"message": "User registered successfully!"}), 201

if __name__ == "__main__":
    app.run(debug=True)

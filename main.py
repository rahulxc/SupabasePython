
from flask import Flask, request, jsonify, send_from_directory
from supabase import create_client
import os

app = Flask(__name__)

# Initialize Supabase client
supabase = create_client(
    os.environ.get("SUPABASE_URL"),
    os.environ.get("SUPABASE_KEY")
)

@app.route('/')
def index():
    return send_from_directory('templates', 'auth.html')

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    try:
        response = supabase.auth.sign_up({
            "email": email,
            "password": password
        })
        user_data = {
            "id": response.user.id,
            "email": response.user.email,
        }
        return jsonify({"message": "Signup successful", "user": user_data}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        user_data = {
            "id": response.user.id,
            "email": response.user.email,
        }
        return jsonify({
            "message": "Login successful",
            "user": user_data
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/logout', methods=['POST'])
def logout():
    try:
        supabase.auth.sign_out()
        return jsonify({"message": "Logout successful"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

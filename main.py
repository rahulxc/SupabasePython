
from flask import Flask, request, jsonify, send_from_directory, redirect
from supabase import create_client
import os

app = Flask(__name__)
app.static_folder = 'static'

supabase = create_client(
    os.environ.get("SUPABASE_URL"),
    os.environ.get("SUPABASE_KEY")
)

@app.route('/')
def index():
    return send_from_directory('templates', 'index.html')

@app.route('/signin')
def signin_page():
    return send_from_directory('templates', 'signin.html')

@app.route('/signup')
def signup_page():
    return send_from_directory('templates', 'signup.html')

@app.route('/dashboard')
def dashboard():
    return send_from_directory('templates', 'dashboard.html')

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    try:
        # Sign up without email confirmation
        response = supabase.auth.sign_up({
            "email": email,
            "password": password,
            "options": {
                "data": {"email_confirm": True}
            }
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

@app.route('/notes', methods=['GET'])
def get_notes():
    try:
        response = supabase.table('notes').select("*").order('created_at', desc=True).execute()
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/notes', methods=['POST'])
def create_note():
    data = request.json
    content = data.get('content')
    
    try:
        response = supabase.table('notes').insert({"content": content}).execute()
        return jsonify(response.data[0]), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/notes/<note_id>', methods=['DELETE'])
def delete_note(note_id):
    try:
        supabase.table('notes').delete().eq('id', note_id).execute()
        return jsonify({"message": "Note deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

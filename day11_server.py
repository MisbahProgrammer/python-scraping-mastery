from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)
DB_NAME = "portfolio.db"

# 1. Setup a new table for your Portfolio Projects
def setup_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            language TEXT
        )
    ''')
    conn.commit()
    conn.close()

setup_db()

# 2. NEW: POST Route to receive new data
@app.route('/api/add_project', methods=['POST'])
def add_project():
    print("🚨 INCOMING POST REQUEST RECEIVED!")
    
    # Grab the JSON data sent by the user/client
    incoming_data = request.get_json()
    project_title = incoming_data.get('title')
    coding_language = incoming_data.get('language')

    # Security check: Make sure they didn't send empty data
    if not project_title or not coding_language:
        return jsonify({"error": "Missing title or language!"}), 400

    # Save the new project into the SQL database
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO projects (title, language) VALUES (?, ?)", (project_title, coding_language))
    conn.commit()
    conn.close()

    # Reply back to the user that it was a success
    return jsonify({
        "status": "success", 
        "message": f"Project '{project_title}' successfully saved to the database!"
    }), 201

if __name__ == "__main__":
    print("🚀 Day 11 API Server running on port 5000...")
    app.run(debug=True, port=5000)
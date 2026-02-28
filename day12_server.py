from flask import Flask, render_template, jsonify, request
import sqlite3

app = Flask(__name__)
DB_NAME = "portfolio.db"

# --- DATABASE SETUP (Same as Day 11) ---
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

# --- ROUTE 1: View Projects (The Dashboard) ---
@app.route('/projects')
def view_projects():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Fetch ALL projects from the database
    cursor.execute("SELECT * FROM projects ORDER BY id DESC")
    all_projects = cursor.fetchall()
    conn.close()

    # Send the data to the HTML file
    return render_template('projects.html', projects=all_projects)

# --- ROUTE 2: Add Project API (From Day 11) ---
@app.route('/api/add_project', methods=['POST'])
def add_project():
    data = request.get_json()
    title = data.get('title')
    language = data.get('language')

    if not title or not language:
        return jsonify({"error": "Bad data"}), 400

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO projects (title, language) VALUES (?, ?)", (title, language))
    conn.commit()
    conn.close()

    return jsonify({"status": "success", "message": "Saved!"}), 201

if __name__ == "__main__":
    print("🚀 Day 12 Dashboard running on http://127.0.0.1:5000/projects")
    app.run(debug=True, port=5000)
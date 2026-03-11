from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DB_NAME = "portfolio.db"

# --- ROUTE 1: View Dashboard ---
@app.route('/projects')
def view_projects():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM projects ORDER BY id DESC")
    all_projects = cursor.fetchall()
    conn.close()
    return render_template('projects.html', projects=all_projects)

# --- ROUTE 2: Add Project (Via Web Form) ---
@app.route('/add_project_web', methods=['POST'])
def add_project_web():
    # Notice we use request.form instead of request.get_json()
    title = request.form.get('title')
    language = request.form.get('language')

    if title and language:
        print(f"📥 Saving new project from web: {title}")
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO projects (title, language) VALUES (?, ?)", (title, language))
        conn.commit()
        conn.close()

    # Immediately refresh the page to show the new project
    return redirect(url_for('view_projects'))

# --- ROUTE 3: Delete Project ---
@app.route('/delete/<int:project_id>', methods=['POST'])
def delete_project(project_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM projects WHERE id = ?", (project_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('view_projects'))

if __name__ == "__main__":
    print("🚀 Day 14 Dashboard running!")
    print("👉 Go to http://127.0.0.1:5000/projects")
    app.run(debug=True, port=5000)
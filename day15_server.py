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

# --- ROUTE 2: Add Project ---
@app.route('/add_project_web', methods=['POST'])
def add_project_web():
    title = request.form.get('title')
    language = request.form.get('language')
    if title and language:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO projects (title, language) VALUES (?, ?)", (title, language))
        conn.commit()
        conn.close()
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

# --- ROUTE 4: Edit Project (NEW) ---
@app.route('/edit/<int:project_id>', methods=['GET', 'POST'])
def edit_project(project_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # If the user clicks "Save Changes" (POST)
    if request.method == 'POST':
        new_title = request.form.get('title')
        new_language = request.form.get('language')
        
        # Use the SQL UPDATE command to modify the existing row
        cursor.execute("UPDATE projects SET title = ?, language = ? WHERE id = ?", (new_title, new_language, project_id))
        conn.commit()
        conn.close()
        return redirect(url_for('view_projects'))

    # If the user just clicked the "Edit" button (GET), load the form
    else:
        cursor.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
        project_data = cursor.fetchone()
        conn.close()
        
        # Pass the existing data to the edit.html template
        return render_template('edit.html', project=project_data)

if __name__ == "__main__":
    print("🚀 Day 15 Full-CRUD Dashboard running!")
    print("👉 Go to http://127.0.0.1:5000/projects")
    app.run(debug=True, port=5000)
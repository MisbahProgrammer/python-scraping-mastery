from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DB_NAME = "portfolio.db"

# --- ROUTE 1: View Projects ---
@app.route('/projects')
def view_projects():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM projects ORDER BY id DESC")
    all_projects = cursor.fetchall()
    conn.close()
    return render_template('projects.html', projects=all_projects)

# --- ROUTE 2: Delete a Project (NEW) ---
@app.route('/delete/<int:project_id>', methods=['POST'])
def delete_project(project_id):
    print(f"🗑️ Request received to delete project #{project_id}")
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Execute the SQL DELETE command safely
    cursor.execute("DELETE FROM projects WHERE id = ?", (project_id,))
    conn.commit()
    conn.close()

    # After deleting, immediately refresh the page by redirecting back to the dashboard
    return redirect(url_for('view_projects'))

if __name__ == "__main__":
    print("🚀 Day 13 Dashboard with Delete functionality running!")
    print("👉 Go to http://127.0.0.1:5000/projects")
    app.run(debug=True, port=5000)
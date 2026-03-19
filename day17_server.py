from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "super_secret_portfolio_key" 
DB_NAME = "portfolio.db"

# --- ROUTE 1: View Dashboard (UPDATED WITH SEARCH) ---
@app.route('/projects')
def view_projects():
    # Grab the search term from the URL (e.g., /projects?search=python)
    search_query = request.args.get('search')
    
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        if search_query:
            print(f"🔍 User is searching for: {search_query}")
            # The % symbol is a wildcard. "%python%" matches "python scripts", "my python", etc.
            search_pattern = f"%{search_query}%"
            
            # Search both the title AND the language columns
            cursor.execute('''
                SELECT * FROM projects 
                WHERE title LIKE ? OR language LIKE ? 
                ORDER BY id DESC
            ''', (search_pattern, search_pattern))
        else:
            # If no search query, just load everything normally
            cursor.execute("SELECT * FROM projects ORDER BY id DESC")
            
        all_projects = cursor.fetchall()
        conn.close()
        
        return render_template('projects.html', projects=all_projects)
        
    except sqlite3.Error as error:
        print(f"🚨 DATABASE ERROR: {error}")
        return "Sorry, the database is currently down."

# --- ROUTE 2: Add Project (Same as Day 16) ---
@app.route('/add_project_web', methods=['POST'])
def add_project_web():
    title = request.form.get('title')
    language = request.form.get('language')
    if title and language:
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO projects (title, language) VALUES (?, ?)", (title, language))
            conn.commit()
            conn.close()
            flash(f"Success! '{title}' was added.", "success")
        except sqlite3.Error as error:
            flash("Failed to save project.", "error")
    return redirect(url_for('view_projects'))

# --- ROUTE 3: Delete Project (Same as Day 16) ---
@app.route('/delete/<int:project_id>', methods=['POST'])
def delete_project(project_id):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM projects WHERE id = ?", (project_id,))
        conn.commit()
        conn.close()
        flash("Project deleted.", "success")
    except sqlite3.Error as error:
        flash("Could not delete project.", "error")
    return redirect(url_for('view_projects'))

# --- ROUTE 4: Edit Project (Same as Day 15) ---
@app.route('/edit/<int:project_id>', methods=['GET', 'POST'])
def edit_project(project_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    if request.method == 'POST':
        new_title = request.form.get('title')
        new_language = request.form.get('language')
        cursor.execute("UPDATE projects SET title = ?, language = ? WHERE id = ?", (new_title, new_language, project_id))
        conn.commit()
        conn.close()
        flash("Project updated successfully!", "success")
        return redirect(url_for('view_projects'))
    else:
        cursor.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
        project_data = cursor.fetchone()
        conn.close()
        return render_template('edit.html', project=project_data)

if __name__ == "__main__":
    print("🚀 Day 17 Dashboard running!")
    app.run(debug=True, port=5000)
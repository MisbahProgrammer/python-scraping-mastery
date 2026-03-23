from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "super_secret_portfolio_key" 
DB_NAME = "portfolio.db"

@app.route('/projects')
def view_projects():
    search_query = request.args.get('search')
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # --- NEW: Fetching Statistics ---
        # Count how many projects exist for each language
        cursor.execute("SELECT language, COUNT(*) FROM projects GROUP BY language ORDER BY COUNT(*) DESC")
        language_stats = cursor.fetchall()
        
        # --- EXISTING: Fetching Projects ---
        if search_query:
            search_pattern = f"%{search_query}%"
            cursor.execute('''
                SELECT * FROM projects 
                WHERE title LIKE ? OR language LIKE ? 
                ORDER BY id DESC
            ''', (search_pattern, search_pattern))
        else:
            cursor.execute("SELECT * FROM projects ORDER BY id DESC")
            
        all_projects = cursor.fetchall()
        conn.close()
        
        # Pass BOTH the projects and the stats to the HTML template
        return render_template('projects.html', projects=all_projects, stats=language_stats)
        
    except sqlite3.Error as error:
        return f"🚨 DATABASE ERROR: {error}"

# --- ROUTE 2: Add Project ---
@app.route('/add_project_web', methods=['POST'])
def add_project_web():
    title = request.form.get('title')
    language = request.form.get('language')
    github_link = request.form.get('github_link') 
    if title and language:
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO projects (title, language, github_link) VALUES (?, ?, ?)", (title, language, github_link))
            conn.commit()
            conn.close()
            flash(f"Success! '{title}' was added.", "success")
        except sqlite3.Error:
            flash("Failed to save project.", "error")
    return redirect(url_for('view_projects'))

# --- ROUTE 3: Delete Project ---
@app.route('/delete/<int:project_id>', methods=['POST'])
def delete_project(project_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM projects WHERE id = ?", (project_id,))
    conn.commit()
    conn.close()
    flash("Project deleted.", "success")
    return redirect(url_for('view_projects'))

# --- ROUTE 4: Edit Project ---
@app.route('/edit/<int:project_id>', methods=['GET', 'POST'])
def edit_project(project_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    if request.method == 'POST':
        new_title = request.form.get('title')
        new_language = request.form.get('language')
        new_link = request.form.get('github_link') 
        cursor.execute("UPDATE projects SET title = ?, language = ?, github_link = ? WHERE id = ?", (new_title, new_language, new_link, project_id))
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
    print("🚀 Day 19 Dashboard with Statistics running!")
    app.run(debug=True, port=5000)
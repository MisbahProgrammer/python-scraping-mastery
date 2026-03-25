from flask import Flask, render_template, request, redirect, url_for, flash, Response
import sqlite3
import csv
from io import StringIO

app = Flask(__name__)
app.secret_key = "super_secret_portfolio_key" 
DB_NAME = "portfolio.db"

# --- ROUTE 1: View Dashboard & Stats (Same as Day 19) ---
@app.route('/projects')
def view_projects():
    search_query = request.args.get('search')
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute("SELECT language, COUNT(*) FROM projects GROUP BY language ORDER BY COUNT(*) DESC")
        language_stats = cursor.fetchall()
        
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
        return render_template('projects.html', projects=all_projects, stats=language_stats)
    except sqlite3.Error as error:
        return f"🚨 DATABASE ERROR: {error}"

# --- ROUTE 2, 3, 4: Add, Delete, Edit (Same as Day 19) ---
@app.route('/add_project_web', methods=['POST'])
def add_project_web():
    title = request.form.get('title')
    language = request.form.get('language')
    github_link = request.form.get('github_link') 
    if title and language:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO projects (title, language, github_link) VALUES (?, ?, ?)", (title, language, github_link))
        conn.commit()
        conn.close()
        flash(f"Success! '{title}' was added.", "success")
    return redirect(url_for('view_projects'))

@app.route('/delete/<int:project_id>', methods=['POST'])
def delete_project(project_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM projects WHERE id = ?", (project_id,))
    conn.commit()
    conn.close()
    flash("Project deleted.", "success")
    return redirect(url_for('view_projects'))

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

# --- ROUTE 5: Export to CSV (NEW) ---
@app.route('/export')
def export_csv():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, language, github_link FROM projects ORDER BY id DESC")
    projects = cursor.fetchall()
    conn.close()

    # Create an in-memory text buffer
    output = StringIO()
    writer = csv.writer(output)
    
    # Write the column headers first
    writer.writerow(['Project ID', 'Title', 'Language', 'GitHub Link'])
    
    # Write all the database rows
    writer.writerows(projects)

    # Package it as a downloadable file response
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=my_portfolio_data.csv"}
    )

if __name__ == "__main__":
    print("🚀 Day 20 Dashboard with CSV Export running!")
    app.run(debug=True, port=5000)
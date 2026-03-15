from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
# A secret key is required to use Flask's 'flash' feature securely
app.secret_key = "super_secret_portfolio_key" 
DB_NAME = "portfolio.db"

# --- ROUTE 1: View Dashboard ---
@app.route('/projects')
def view_projects():
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM projects ORDER BY id DESC")
        all_projects = cursor.fetchall()
        conn.close()
        return render_template('projects.html', projects=all_projects)
    except sqlite3.Error as error:
        # If the database fails, the app won't crash. It prints the error to the terminal.
        print(f"🚨 DATABASE ERROR: {error}")
        return "Sorry, the database is currently down. Please try again later."

# --- ROUTE 2: Add Project ---
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
            
            # Send a green success message to the HTML
            flash(f"Success! '{title}' was added to your portfolio.", "success")
            
        except sqlite3.Error as error:
            # Send a red error message to the HTML
            flash("Failed to save project to the database.", "error")
            print(f"🚨 DB ERROR: {error}")
            
    return redirect(url_for('view_projects'))

# --- ROUTE 3: Delete Project ---
@app.route('/delete/<int:project_id>', methods=['POST'])
def delete_project(project_id):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM projects WHERE id = ?", (project_id,))
        conn.commit()
        conn.close()
        
        flash("Project successfully deleted.", "success")
        
    except sqlite3.Error as error:
        flash("Could not delete project.", "error")
        
    return redirect(url_for('view_projects'))

if __name__ == "__main__":
    print("🚀 Day 16 Crash-Proof Server running!")
    app.run(debug=True, port=5000)
import sqlite3

DB_NAME = "portfolio.db"

print("🔄 Starting database migration...")

try:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # ALTER TABLE adds a new column without deleting existing data
    cursor.execute("ALTER TABLE projects ADD COLUMN github_link TEXT;")
    
    conn.commit()
    print("✅ Success! The 'github_link' column has been added to your database.")
except sqlite3.OperationalError as e:
    print(f"⚠️ Notice: {e} (The column might already exist!)")
finally:
    conn.close()
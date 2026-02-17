import sqlite3

# ==========================================
# DAY 8: SQL & Databases (The System Admin's Weapon)
# Goal: Create a database, save data, and read it back.
# ==========================================

# 1. CONNECT (Create the Database)
# This creates a file named 'portfolio.db' in your folder.
db_file = "portfolio.db"
connection = sqlite3.connect(db_file)
cursor = connection.cursor()

print(f"💾 Connected to database: {db_file}")

# 2. CREATE TABLE (The Structure)
# We need columns: ID, Project Name, Language, and Lines of Code.
# "IF NOT EXISTS" prevents errors if you run the script twice.
cursor.execute('''
    CREATE TABLE IF NOT EXISTS my_projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        language TEXT,
        lines_of_code INTEGER
    )
''')
print("✅ Table 'my_projects' is ready.")

# 3. INSERT DATA (Saving Info)
# Let's add your actual projects into the database.
projects_to_add = [
    ("Day 1: Hello World", "Python", 5),
    ("Day 6: Scraper", "Python", 45),
    ("Day 7: GitHub API", "Python", 32),
    ("Future: Yandex Clone", "Python", 15000)
]

# We loop through the list and inject them into SQL
print("\n📝 Inserting data into the vault...")
cursor.executemany("INSERT INTO my_projects (name, language, lines_of_code) VALUES (?, ?, ?)", projects_to_add)

# IMPORTANT: You must 'commit' (save) the changes!
connection.commit()
print("✅ Data saved successfully.")

# 4. QUERY DATA (Reading it back)
# Now, let's ask the database what it has inside.
print("\n🔍 Reading from the Database:")
print(f"{'ID':<5} | {'PROJECT NAME':<25} | {'LANGUAGE':<10} | {'SIZE (LOC)'}")
print("-" * 60)

# SQL Command: SELECT everything FROM the table
for row in cursor.execute("SELECT * FROM my_projects"):
    # row is a tuple: (1, 'Day 1...', 'Python', 5)
    p_id, p_name, p_lang, p_size = row
    print(f"{p_id:<5} | {p_name:<25} | {p_lang:<10} | {p_size}")

# 5. CLOSE
connection.close()
print("\n🔒 Database connection closed.")
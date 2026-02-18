import sqlite3
import requests
import datetime
import os

# --- CONFIGURATION ---
GITHUB_USERNAME = "MisbahProgrammer"  # Change this to your real username if different
DB_NAME = "portfolio.db"

# --- PART 1: FETCH DATA (The API Robot) ---
def fetch_github_stats():
    print(f"🤖 Fetching data for {GITHUB_USERNAME}...")
    url = f"https://api.github.com/users/{GITHUB_USERNAME}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return {
            "public_repos": data['public_repos'],
            "followers": data['followers'],
            "total_stars": 120,  # Note: Real API needs a loop for stars, hardcoding for demo
            "date": datetime.date.today().isoformat()
        }
    else:
        print("❌ Error fetching data!")
        return None

# --- PART 2: SAVE DATA (The Database Manager) ---
def save_to_db(stats):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # 1. Create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS github_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            public_repos INTEGER,
            followers INTEGER,
            total_stars INTEGER
        )
    ''')
    
    # 2. Insert new data
    cursor.execute('''
        INSERT INTO github_stats (date, public_repos, followers, total_stars)
        VALUES (?, ?, ?, ?)
    ''', (stats['date'], stats['public_repos'], stats['followers'], stats['total_stars']))
    
    conn.commit()
    conn.close()
    print("✅ Data saved to database.")

# --- PART 3: GENERATE REPORT (The Designer) ---
def generate_portfolio_page():
    # 1. Get the latest stats from DB
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM github_stats ORDER BY id DESC LIMIT 1")
    latest = cursor.fetchone() # Returns (id, date, repos, followers, stars)
    conn.close()

    if not latest:
        print("⚠️ No data found to generate report.")
        return

    # Unpack data
    date, repos, followers, stars = latest[1], latest[2], latest[3], latest[4]

    # 2. Create HTML with Tailwind CSS
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://cdn.tailwindcss.com"></script>
        <title>Misbah's Portfolio Tracker</title>
    </head>
    <body class="bg-gray-900 text-white font-sans flex items-center justify-center h-screen">
        
        <div class="bg-gray-800 p-8 rounded-2xl shadow-2xl w-96 border border-gray-700">
            <h1 class="text-3xl font-bold text-center mb-2 text-blue-400">🚀 Misbah's Stats</h1>
            <p class="text-center text-gray-400 mb-6">Last Updated: {date}</p>
            
            <div class="space-y-4">
                <div class="flex justify-between items-center bg-gray-700 p-4 rounded-lg">
                    <span class="text-lg">📦 Public Repos</span>
                    <span class="text-2xl font-bold text-green-400">{repos}</span>
                </div>
                
                <div class="flex justify-between items-center bg-gray-700 p-4 rounded-lg">
                    <span class="text-lg">👥 Followers</span>
                    <span class="text-2xl font-bold text-purple-400">{followers}</span>
                </div>
                
                <div class="flex justify-between items-center bg-gray-700 p-4 rounded-lg">
                    <span class="text-lg">⭐ Total Stars</span>
                    <span class="text-2xl font-bold text-yellow-400">{stars}</span>
                </div>
            </div>

            <button class="mt-8 w-full bg-blue-600 hover:bg-blue-500 text-white font-bold py-2 px-4 rounded transition">
                View GitHub Profile
            </button>
        </div>

    </body>
    </html>
    """

    # 3. Save to file
    with open("index.html", "w", encoding="utf-8") as file:
        file.write(html_content)
    
    print("✨ Portfolio Page Generated: index.html")

# --- MAIN AUTOMATION ---
if __name__ == "__main__":
    # Step 1: Get Data
    stats = fetch_github_stats()
    
    if stats:
        # Step 2: Save to SQL
        save_to_db(stats)
        
        # Step 3: Update Website
        generate_portfolio_page()
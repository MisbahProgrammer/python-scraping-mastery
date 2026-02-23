from flask import Flask, jsonify
import sqlite3

# Initialize the Flask application
app = Flask(__name__)
DB_NAME = "portfolio.db"

# Create a "Route" (an endpoint for your API)
@app.route('/api/stats', methods=['GET'])
def get_my_stats():
    print("📡 Someone requested the stats API...")
    
    # 1. Connect to your database
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # 2. Get the latest record
    try:
        cursor.execute("SELECT date, public_repos, followers, total_stars FROM github_stats ORDER BY id DESC LIMIT 1")
        data = cursor.fetchone()
        conn.close()

        # 3. Format the data as JSON (just like GitHub did for us!)
        if data:
            return jsonify({
                "status": "success",
                "developer": "Misbah Ur Rehman",
                "latest_stats": {
                    "date": data[0],
                    "public_repos": data[1],
                    "followers": data[2],
                    "total_stars": data[3]
                }
            })
        else:
            return jsonify({"status": "error", "message": "No data found in database."})
            
    except sqlite3.OperationalError:
        return jsonify({"status": "error", "message": "Database not found. Did you run Day 9 first?"})

# --- MAIN SERVER ---
if __name__ == "__main__":
    print("🚀 Starting Misbah's Local API Server on port 5000...")
    app.run(debug=True, port=5000)
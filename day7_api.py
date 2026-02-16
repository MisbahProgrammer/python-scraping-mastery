import requests
import json

# ==========================================
# DAY 7: API Integration 
# Goal: Fetch your own repository data from GitHub.
# ==========================================

# 1. SETUP: Target your specific GitHub username
GITHUB_USERNAME = "MisbahProgrammer" 
API_URL = f"https://api.github.com/users/{GITHUB_USERNAME}/repos"

def get_my_repos():
    print(f"📡 Connecting to GitHub API for user: {GITHUB_USERNAME}...")
    
    try:
        # 2. REQUEST: Send a GET request to GitHub
        response = requests.get(API_URL)
        
        # 3. CHECK: Did the server say "OK"? (Status 200)
        if response.status_code == 200:
            print("✅ Success! Data received.\n")
            
            # 4. PARSE: Convert the JSON text into a Python List
            repositories = response.json()
            
            if not repositories:
                print(f"⚠️ User '{GITHUB_USERNAME}' has no public repositories yet.")
                print("   (Action: Push your Day 6 code to see it appear here!)")
                return

            # 5. DISPLAY: Print a clean table of your work
            print(f"{'REPO NAME':<25} | {'LANGUAGE':<12} | {'SIZE (KB)':<10}")
            print("-" * 55)
            
            for repo in repositories:
                name = repo['name']
                # Handle cases where language is None (e.g. just a Readme)
                language = repo['language'] if repo['language'] else "Text"
                size = repo['size']
                
                print(f"{name:<25} | {language:<12} | {size:<10}")
                
        elif response.status_code == 404:
            print(f"❌ Error: User '{GITHUB_USERNAME}' not found.")
        else:
            print(f"❌ Error: API returned status {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection Error: {e}")

if __name__ == "__main__":
    get_my_repos()
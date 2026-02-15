import requests
from bs4 import BeautifulSoup
import csv
import os

# ==========================================
# DAY 6: Web Scraping (The "Money" Skill)
# Goal: Download a website, find data, save it.
# ==========================================

# 1. SETUP: Force the file to save in the script's folder
script_folder = os.path.dirname(os.path.abspath(__file__))
csv_file_path = os.path.join(script_folder, "scraped_quotes.csv")

# 2. THE TARGET: A "sandbox" website made for practicing scraping
url = "https://quotes.toscrape.com"

# Headers make us look like a real browser (Chrome), not a robot.
# This prevents some websites from blocking us.
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def scrape_quotes():
    print(f"Connecting to {url}...")
    
    # 3. REQUEST: Knock on the door and ask for the HTML code
    response = requests.get(url, headers=headers)
    
    # Check if the door opened (Status Code 200 means "OK")
    if response.status_code == 200:
        print("Success! HTML downloaded. Parsing data...")
        
        # 4. PARSE: Turn the messy HTML text into a "Soup" object we can search
        soup = BeautifulSoup(response.text, "html.parser")
        
        # 5. EXTRACT: Find the specific HTML tags
        # On this site, every quote is inside a <div class="quote">
        quote_cards = soup.find_all("div", class_="quote")
        
        print(f"Found {len(quote_cards)} quotes on the page.")
        
        data_to_save = []
        
        # Loop through each card and pull out the text
        for card in quote_cards:
            # Find the quote text (span class="text")
            text = card.find("span", class_="text").get_text(strip=True)
            
            # Find the author (small class="author")
            author = card.find("small", class_="author").get_text(strip=True)
            
            # Add it to our list
            data_to_save.append({
                "Author": author,
                "Quote": text
            })
            
        # 6. SAVE: Dump it into a CSV file
        save_to_csv(data_to_save)
        
    else:
        print(f"Error: Website returned status code {response.status_code}")

def save_to_csv(data):
    print(f"Saving data to {csv_file_path}...")
    
    with open(csv_file_path, "w", newline="", encoding="utf-8") as f:
        # Define the column names
        writer = csv.DictWriter(f, fieldnames=["Author", "Quote"])
        
        # Write the top row (headers)
        writer.writeheader()
        
        # Write the data rows
        writer.writerows(data)
        
    print("DONE! Check your folder for 'scraped_quotes.csv'.")

# ==========================================
# RUN THE BOT
# ==========================================
if __name__ == "__main__":
    scrape_quotes()
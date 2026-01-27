# Day 1 Redux: The Data Miner
# Goal: Scrape Book Titles and Prices from a sandbox website and save to CSV.
# This proves I can extract data from the web.

import requests
from bs4 import BeautifulSoup
import csv

# 1. The Target URL (A safe place to practice scraping)
url = "http://books.toscrape.com/"

print(f"Connecting to {url}...")
response = requests.get(url)

# Check if connection was successful
if response.status_code == 200:
    print("Connection successful! Parsing data...")
    
    # 2. Parse the HTML
    soup = BeautifulSoup(response.text, "html.parser")
    
    # 3. Find all books (Tag: <article>, Class: product_pod)
    books = soup.find_all("article", class_="product_pod")
    
    # 4. Open a CSV file to save the data
    filename = "books_data.csv"
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        # Write the Header
        writer.writerow(["Book Title", "Price", "Stock Status"])
        
        # 5. Loop through each book
        count = 0
        for book in books:
            try:
                # Extract Title (from the <a> tag inside <h3>)
                title = book.h3.a["title"]
                
                # Extract Price (text of the <p> tag with class 'price_color')
                price = book.find("p", class_="price_color").text
                
                # Extract Stock (text of the <p> tag with class 'availability')
                stock = book.find("p", class_="instock availability").text.strip()
                
                # Save to file
                writer.writerow([title, price, stock])
                count += 1
            except AttributeError:
                continue # Skip if bad data
            
    print(f"Success! Scraped {count} books. Check '{filename}'.")

else:
    print(f"Failed to connect. Error: {response.status_code}")
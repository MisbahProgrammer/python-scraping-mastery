# Day 2: The Pagination Solver
# Goal: Scrape ALL 1,000 books by following the "next" button.

import requests
from bs4 import BeautifulSoup
import csv
import time # Import time to add a delay (so we don't crash the server)

# 1. Setup the CSV File
filename = "all_books.csv"
with open(filename, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Book Title", "Price", "Availability"]) # Header

    # 2. Start at Page 1
    url = "http://books.toscrape.com/catalogue/page-1.html"
    page_count = 1

    # 3. The "While" Loop (Runs as long as 'url' is not Empty)
    while url:
        print(f"Scraping Page {page_count}...")
        
        # Fetch the page
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Find all books on this page
        books = soup.find_all("article", class_="product_pod")
        
        # Loop through books and save them
        for book in books:
            try:
                title = book.h3.a["title"]
                price = book.find("p", class_="price_color").text
                stock = book.find("p", class_="instock availability").text.strip()
                
                writer.writerow([title, price, stock])
            except AttributeError:
                continue

        # 4. Find the "Next" Button
        # It looks like: <li class="next"><a href="page-2.html">next</a></li>
        next_button = soup.find("li", class_="next")
        
        if next_button:
            # Get the link inside the button
            next_link = next_button.find("a")["href"]
            
            # Combine it to make the full URL
            # Note: The site structure is simple, so we just replace the end of the URL
            # Real websites might need 'urllib.parse.urljoin'
            url = "http://books.toscrape.com/catalogue/" + next_link
            
            page_count += 1
            time.sleep(1) # Sleep for 1 second to be polite to the server
        else:
            # If no "Next" button is found, we are done!
            print("No 'Next' button found. Scraping complete.")
            url = None # This kills the While loop

print(f"Done! Scraped {page_count} pages. Data saved to '{filename}'.")
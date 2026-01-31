import requests
from bs4 import BeautifulSoup
import csv # The tool to create Excel-ready files

# --- STEP 1: SETUP THE FILE ---
filename = "books_database.csv"

# Open the file in 'write' mode ('w')
# newline='' prevents empty rows between data
with open(filename, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    
    # Write the Header Row (The Column Names)
    writer.writerow(['Book Title', 'Price', 'Rating', 'Availability'])

    # --- STEP 2: CONNECT TO WEBSITE ---
    url = "http://books.toscrape.com/"
    print("Connecting to website...")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # --- STEP 3: FIND ALL PRODUCTS ---
    # On this site, every book is inside an <article class="product_pod">
    books = soup.find_all("article", class_="product_pod")
    
    print(f"Found {len(books)} books. Extracting data...\n")

    # --- STEP 4: LOOP AND EXTRACT ---
    count = 0
    for book in books:
        # 1. Title (It's inside the <h3> tag, in the 'title' attribute)
        title = book.h3.a['title']
        
        # 2. Price (Inside <p class="price_color">)
        price_text = book.find('p', class_='price_color').text
        # Clean it: Remove the weird 'Â£' character if it appears
        price = price_text.replace('Â£', '£')
        
        # 3. Rating (Tricky! It's a class name like "star-rating Three")
        # We find the tag, get the class list, and take the last word
        star_tag = book.find('p', class_='star-rating')
        rating_class = star_tag['class'] # Returns ['star-rating', 'Three']
        rating = rating_class[1] # We want 'Three'
        
        # 4. Availability
        stock = book.find('p', class_='instock availability').text.strip()
        
        # --- STEP 5: WRITE TO CSV ---
        writer.writerow([title, price, rating, stock])
        
        count += 1
        print(f"Saved: {title}")

print(f"\nSuccess! Data saved to '{filename}'.")
print("You can open this file in Excel.")
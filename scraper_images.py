import requests
from bs4 import BeautifulSoup
import os  # To create folders on your computer

# --- 1. SETUP: Create a folder to save images ---
folder_name = "downloaded_covers"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)
    print(f"Created folder: {folder_name}")

# --- 2. CONNECT: Go to the website ---
url = "http://books.toscrape.com/"
print(f"Connecting to {url}...")
response = requests.get(url)

# Check if the website blocked us (200 means OK)
if response.status_code == 200:
    print("Connection Successful! Finding images...\n")
    soup = BeautifulSoup(response.text, "html.parser")

    # --- 3. FIND: Grab all image tags ---
    # We look for all <img ...> tags inside the product section
    images = soup.find_all("img")

    # --- 4. DOWNLOAD LOOP ---
    count = 0
    for img in images:
        # Get the image link (src)
        img_url = img['src']
        
        # Clean the link (remove relative dots like ../)
        clean_url = img_url.replace("../", "")
        
        # Create the full web address for the image
        full_image_url = "http://books.toscrape.com/" + clean_url
        
        # Get the filename (e.g., '1000_places_to_see.jpg')
        filename = clean_url.split("/")[-1] 
        
        # DOWNLOAD the actual image data
        image_data = requests.get(full_image_url).content
        
        # SAVE it to your folder
        with open(os.path.join(folder_name, filename), 'wb') as file:
            file.write(image_data)
            
        count += 1
        print(f"[{count}] Downloaded: {filename}")

    print(f"\nSuccess! I downloaded {count} images into the '{folder_name}' folder.")

else:
    print("Failed to connect to the website.")
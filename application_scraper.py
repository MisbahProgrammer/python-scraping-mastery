import json
import csv
import os

# ==========================================
# FIXED: FORCE SAVE TO SCRIPT FOLDER
# ==========================================

# 1. Get the folder where THIS script is located
# __file__ = the path of this code file
# os.path.dirname = gets the folder part of that path
script_folder = os.path.dirname(os.path.abspath(__file__))

print(f"Script is running in: {script_folder}")

# 2. Function to build the full path safely
def get_path(filename):
    return os.path.join(script_folder, filename)

# ==========================================
# DATA & SAVING (Same as before, but using get_path)
# ==========================================

university_data = [
    {
        "id": 1,
        "university": "ITMO University",
        "program": "02.03.03 Software & Administration",
        "physics_exam": False,
        "seats_available": 13
    },
    {
        "id": 2,
        "university": "MISIS",
        "program": "09.03.01 Computer Engineering",
        "physics_exam": True,
        "seats_available": 50
    }
]

def save_to_json(data, filename):
    # USE THE FIXED PATH
    full_path = get_path(filename)
    print(f"STATUS: Saving to {full_path}...")
    
    with open(full_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        
    print("SUCCESS: JSON file created.\n")

def save_to_csv(data, filename):
    # USE THE FIXED PATH
    full_path = get_path(filename)
    print(f"STATUS: Saving to {full_path}...")
    
    headers = data[0].keys()
    
    with open(full_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)
        
    print("SUCCESS: CSV file created.\n")

# ==========================================
# EXECUTION
# ==========================================
if __name__ == "__main__":
    save_to_json(university_data, "my_applications.json")
    save_to_csv(university_data, "my_applications.csv")
    
    # 3. Open the folder for you (Works on Windows)
    try:
        os.startfile(script_folder)
        print("I opened the folder for you!")
    except:
        pass
import requests

# The exact URL of your local API endpoint
API_URL = "http://127.0.0.1:5000/api/add_project"

# The data package (JSON payload) we want to send to the server
new_project_data = {
    "title": "Russian Language Flashcard App",
    "language": "Python"
}

print("📤 Sending new project data to the API...")

# Use requests.post() instead of requests.get()
response = requests.post(API_URL, json=new_project_data)

# Print the server's reply!
print("📥 Server Reply:", response.json())
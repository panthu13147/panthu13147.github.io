import requests
from bs4 import BeautifulSoup

# Add headers just in case
headers = {'User-Agent': 'Mozilla/5.0'}
url = "https://nostarch.com"

res = requests.get(url, headers=headers)
print(f"Status Code: {res.status_code}") # Should be 200

# DEBUGGING STEP: Print the raw HTML
# This tells us if the site is empty, blocked, or using JavaScript
print("\n--- RAW CONTENT START ---")
print(res.text[:500]) 
print("--- RAW CONTENT END ---\n")

soup = BeautifulSoup(res.text, 'html.parser')

# Safe way to check for title
if soup.title:
    print(f"Title found: {soup.title.string}")
else:
    print("No <title> tag found in the response.")
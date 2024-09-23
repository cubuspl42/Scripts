#!/usr/bin/env python3

import requests

url = "https://raw.githubusercontent.com/Expensify/App/main/contributingGuides/REVIEWER_CHECKLIST.md"

def fetch_and_replace():
    response = requests.get(url)

    if response.status_code == 200:
        modified_text = response.text.replace("- [ ]", "- [x]")
        print(modified_text)
    else:
        print(f"Failed to get the file, status code: {response.status_code}")

if __name__ == "__main__":
    fetch_and_replace()

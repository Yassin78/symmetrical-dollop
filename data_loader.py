import requests
import os
import time
import json

OPEN5E_API_ROOT = "https://api.open5e.com/v1/"

def fetch_open5e_directory_data():
    response = requests.get(OPEN5E_API_ROOT)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch Open5e API directory: {response.text}")

    return response.json()

def json_to_md(json_data):
    md_content = []
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            md_content.append(f"## {key}\n")
            md_content.append(f"{value}\n")
    elif isinstance(json_data, list):
        for item in json_data:
            md_content.append("- " + str(item) + "\n")
    else:
        md_content.append(str(json_data))
    return ''.join(md_content)

def store_open5e_directory_data():
    directory_data = fetch_open5e_directory_data()
    if not os.path.exists("data"):
        os.mkdir("data")

    for endpoint, url in directory_data.items():
        # Check if file already exists
        filepath = f"data/{endpoint}.md"
        if os.path.exists(filepath):
            print(f"Data already loaded for {endpoint}.")
            continue

        print(f"Fetching data from {endpoint}...")
        response = requests.get(url)
        if response.status_code == 200:
            data_md = json_to_md(response.json())
            with open(filepath, 'w') as file:
                file.write(data_md)
            print(f"Data stored for {endpoint}.")
        else:
            print(f"Error fetching data from {endpoint}: {response.text}")
        
        # Adding a delay to avoid rate limit
        time.sleep(1)

if __name__ == "__main__":
    store_open5e_directory_data()


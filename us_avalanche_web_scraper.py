import requests
from bs4 import BeautifulSoup
import csv

# Define the URL
url = 'https://avalanche.org/avalanche-accidents/'

# Send a GET request to the URL
response = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Find tables with the specified headers
details_tables = soup.find_all('table', class_='us_acc_table_border')

# CSV file for tables with headers "Date", "State", "Location", "Description", and "Killed"
with open('details_data.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Date', 'State', 'Location', 'Description', 'Killed'])
    for table in details_tables:
        # Check if the table headers match the specified format
        headers = table.find_all('th', class_='table-header')
        header_texts = [header.get_text(strip=True) for header in headers]
        expected_headers = ['Date', 'State', 'Location', 'Description', 'Killed']
        if header_texts == expected_headers:
            rows = table.find_all('tr')
            for row in rows[1:]:  # Skip the first row which contains headers
                cols = row.find_all('td')
                if len(cols) == 5:
                    date = cols[0].get_text(strip=True)
                    state = cols[1].get_text(strip=True)
                    location = cols[2].get_text(strip=True)
                    description = cols[3].get_text(strip=True)
                    killed = cols[4].get_text(strip=True)
                    writer.writerow([date, state, location, description, killed])

print("CSV file has been created successfully.")

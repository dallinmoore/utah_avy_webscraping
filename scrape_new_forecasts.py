# needs to be finished to get the links for the new forecasts and run the rose functions for each report

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from process_rose_data import process_rose_data


# Define the URL
base_url = 'https://utahavalanchecenter.org'
archives_url = '/archives/forecasts?page='
page = 1
url = base_url + archives_url + str(page)

# Initialize an empty list to store data
data = []


while page<4:
    print(f'Scraping page {page}.',end='\r')
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Check if the page has no results
    if soup.find('div', class_='view-empty'):
        print("No results found. Stopping loop.")
        break
    
    # Find all the table rows
    table_rows = soup.find_all('tr')
    
    # Iterate through each row
    for row in table_rows[1:]:  # Skip the first row as it contains headers
        # Extract data from each column
        columns = row.find_all('td')
        
        # Extract text from each column and strip whitespace
        date_issued = columns[0].get_text().strip()
        forecast_area = columns[1].get_text()[11:-15].strip()
        # forecaster = columns[2].get_text().strip()
        link = columns[1].find('a')['href']  # Extract link from the second column
        
        # Append the data as a dictionary to the list
        data.append({'Date Issued': date_issued,
                     'Forecast Area': forecast_area,
                    #  'Forcaster': forecaster,
                     'Link': base_url+link})
    
    # Increment page number for the next iteration
    page += 1
    url = base_url + archives_url + str(page)


# Create DataFrame from the list of dictionaries
df = pd.DataFrame(data)

df.to_csv('updated-avalanche-forecast-links.csv',index=False)
print("CSV: 'updated-avalanche-forecast-links.csv' has been created.")


def get_rose_link(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.text, 'html.parser')
        rose_img = soup.find('img', class_="full-width compass-width sm-pb3")['src']
        if rose_img is not None:
            return rose_img
        else:
            return None
    except Exception as e:
        print(f"Error occurred while processing {url}: {e}")  # Log the error
        return None

curr_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the script
input_csv = os.path.join(curr_dir, 'updated-avalanche-forecast-links.csv')  # avalanche-forecast-links
output_csv = os.path.join(curr_dir, 'avalanche-forecast-rose-new.csv')
process_rose_data(input_csv, output_csv, get_rose_link)

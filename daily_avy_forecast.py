import requests
from bs4 import BeautifulSoup
import pandas as pd

# Define the URL
base_url = 'https://utahavalanchecenter.org'
archives_url = '/archives/forecasts?page='
page = 1
url = base_url + archives_url + str(page)

# Initialize an empty list to store data
data = []


while True:
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

df.to_csv('avalanche-forecast-links.csv',index=False)
print("CSV: 'avalanche-forecast-links.csv' has been created.")
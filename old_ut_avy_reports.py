import requests
from bs4 import BeautifulSoup
import pandas as pd

# Define the URL
base_url = 'https://utahavalanchecenter.org'
archives_url = '/archive/advisories/'

# define the regions
regions = ['logan','ogden','salt-lake','provo','uintas','skyline','moab','abajo','la-sal-mountains','southwest','wasatch']

data = []  # List to store extracted data

for region in regions:
    print(f"Scraping {region.capitalize()}.         ", end="\r")
    region_url = base_url + archives_url + region
    response = requests.get(region_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        divs = soup.find_all('div', class_='text_02 body')
        for div in divs:
            links = div.find_all('a')
            for link in links:
                link_text = link.get_text()
                link_href = link['href']
                data.append({'Date Issued': f'{link_text[4:6]}/{link_text[6:]}/{link_text[0:4]}', 
                             'Forecast Area': region.replace("-", " ").capitalize(), 
                             'Link': base_url+link_href})

# Convert data to DataFrame
df = pd.DataFrame(data)

# Save DataFrame to CSV
df.to_csv('old-forecast-links.csv', index=False)
print("CSV: 'old-forecast-links.csv' has been created")
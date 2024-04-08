import os
from process_rose_data import process_rose_data
import requests
from bs4 import BeautifulSoup

def get_rose_link(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.text, 'html.parser')
        div = soup.find('div', class_="advisory-row advanced")
        if div is not None:
            rose_img = div.find_all('img')[1]['src']
            return rose_img[4:]
        else:
            return None
    except Exception as e:
        print(f"Error occurred while processing {url}: {e}")  # Log the error
        return None

curr_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the script
input_csv = os.path.join(curr_dir, 'old-forecast-links.csv')  # old-forecast-links
output_csv = os.path.join(curr_dir, 'avalanche-forecast-rose-old2.csv')
process_rose_data(input_csv, output_csv, get_rose_link)
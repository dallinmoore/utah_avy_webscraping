import os
from process_rose_data import process_rose_data
import requests
from bs4 import BeautifulSoup

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

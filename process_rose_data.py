import csv
import os
import cv2
import numpy as np 
import time
from read_the_rose import read_the_rose, coordinates
import requests

base_url = 'https://utahavalanchecenter.org'

def process_rose_data(input_file, output_file, get_rose_link_function):
    with open(input_file, 'r', newline='', encoding='utf-8') as infile, open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + list(coordinates.keys())  # Add danger level columns
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        total_rows = sum(1 for row in reader)  # Count total number of rows
        start_time = time.time()
        infile.seek(0)  # Reset file pointer
        next(reader)  # Skip header

        for i, row in enumerate(reader, start=1):
            link = row['Link']
            rose_link = base_url + get_rose_link_function(link)

            if rose_link:
                try:
                    response = requests.get(rose_link)
                    response.raise_for_status()  # Raise an exception for HTTP errors
                    image_data = response.content
                    # Decode the image from memory
                    image_np = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)
                    rose_data = read_the_rose(image_np)
                    row.update(rose_data)
                except Exception as e:
                    print(f"Error processing rose image for {link}: {e}")  # Log the error

            # Calculate and print progress percentage
            percent_complete = (i / total_rows) * 100
            elapsed_time = time.time() - start_time
            print(f"Progress: {percent_complete:.2f}% complete. {elapsed_time//60:.0f} min {elapsed_time%60:.2f} sec elapsed.", end='\r', flush=True)

            writer.writerow(row)
    print("\nCSV write complete.")

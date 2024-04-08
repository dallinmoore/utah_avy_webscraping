import cv2
import numpy as np
from io import BytesIO

def read_the_rose(image):
    # Convert the image from BGR to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Dictionary to store danger levels for each point
    danger_levels = {}

    # Loop through each coordinate in the coordinates dictionary
    for point, coord in coordinates.items():
        # Extract the HSV value at the coordinate
        hsv_value = hsv_image[coord[1], coord[0]]

        # Convert HSV value to danger level
        danger_level = convert_to_danger_level(hsv_value)
        
        # Store the danger level in the dictionary
        danger_levels[point] = danger_level

    return danger_levels

def convert_to_danger_level(hsv_value):
    # Calculate Euclidean distance between the HSV value and each danger level
    distances = {level: np.linalg.norm(np.array(hsv_value) - np.array(level_hsv)) for level, level_hsv in danger_levels.items()}
    
    # Find the danger level with the minimum distance
    closest_level = min(distances, key=distances.get)
    
    return closest_level


# Define the coordinates for each of the 24 specific points
coordinates = {
    'North-lower': [200, 70],
    'Northeast-lower': [285, 100],
    'East-lower': [320, 170],
    'Southeast-lower': [290, 250],
    'South-lower': [200, 280],
    'Southwest-lower': [100, 250],
    'West-lower': [75, 170],
    'Northwest-lower': [110, 100],
    'North-middle': [200, 100],
    'Northeast-middle': [250, 120],
    'East-middle': [270, 160],
    'Southeast-middle': [250, 210],
    'South-middle': [200, 230],
    'Southwest-middle': [150, 210],
    'West-middle': [120, 160],
    'Northwest-middle': [150, 120],
    'North-upper': [200, 130],
    'Northeast-upper': [220, 130],
    'East-upper': [230, 155],
    'Southeast-upper': [230, 175],
    'South-upper': [200, 185],
    'Southwest-upper': [175, 175],
    'West-upper': [160, 155],
    'Northwest-upper': [175, 140]
}
 
# Define the expected values for each of the danger levels
# danger_levels = {'None':[0,0,192],
#                  'Low':[58,155,184],
#                  'Moderate':[28,255,255],
#                  'Considerable':[16,224,247],
#                  'High':[179,225,237],
#                  'Extreme':[0,0,0]}
danger_levels = {0:[0,0,192],
                 1:[58,155,184],
                 2:[28,255,255],
                 3:[16,224,247],
                 4:[179,225,237],
                 5:[0,0,0]}

'''
# Example use case
import os
curr_dir = os.getcwd()
image_path = os.path.join(curr_dir,'avy-danger-rose-1.png') 
image = cv2.imread(image_path)

# Call the function to extract danger levels
print(read_danger_rose(image))
'''

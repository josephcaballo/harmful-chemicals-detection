## Pre-requisites:
# 1. Install the Google Cloud Vision API client library for Python: pip install google-cloud-vision

import json
from pathlib import Path

# Path to the JSON file containing harmful chemicals
file_path = Path('harmful-chemicals.json')

try:
    # Open the file in read mode ('r')
    with open(file_path, 'r') as file:
        # Load the JSON data into a Python variable (e.g., 'data')
        data = json.load(file)
except FileNotFoundError:
    print("Error: The file was not found.")
except json.JSONDecodeError as e:
    print(f"Error: Failed to decode JSON. Check file format: {e}")

def detect_text_uri(uri):
    """Detects harmful ingredients based on the harmful chemicals list"""
    from google.cloud import vision

    # Instatiate client and image
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = uri

    # Save detected texts from the image
    response = client.text_detection(image=image)
    texts = response.text_annotations

    # convert target words to lowercase for case-insensitive comparison
    target_word = [word.lower() for word in data['additives']] 
    # combine all detected text into a single string for easier searching
    contents = "".join([text.description.lower() for text in texts]) 

    # Print detected texts
    matches = [word for word in target_word if word in contents]
    print(matches)

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )


detect_text_uri("https://www.post-gazette.com/image/2024/12/30/1140x_a10-7_cTC/Atlanta-Georgia-December-16-2024-Candy-Ingredients-Label-1")
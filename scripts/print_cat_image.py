import requests
from PIL import Image
import numpy as np
from io import BytesIO
import os

CATKEY = os.environ['CATKEY']

def get_random_cat_image(api_key):
    url = "https://api.thecatapi.com/v1/images/search"
    headers = {
        "x-api-key": api_key
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        # Extract the URL of the cat image from the response
        image_url = data[0]["url"]
        print(response.text)

        # Download the image
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))

        # Resize the image
        width, height = img.size
        aspect_ratio = height/width
        new_width = 20
        new_height = aspect_ratio * new_width * 0.55
        img = img.resize((new_width, int(new_height)))

        # Convert the image to grayscale
        img = img.convert('L')

        pixels = np.array(img)

        # Define the ASCII characters
        ascii_chars = "@%#*+=-:. "

        # Replace each pixel with an ASCII character
        ascii_str = ''
        for pixel_value in pixels.flatten():
            ascii_str += ascii_chars[pixel_value//28]
        ascii_str_len = len(ascii_str)

        # Split the ASCII string into multiple strings and join them with a newline character
        ascii_img=""
        for i in range(0, ascii_str_len, new_width):
            ascii_img += ascii_str[i:i+new_width] + "\n"

        # Print the ASCII image
        print(ascii_img)

        return image_url
    else:
        print("Failed to fetch cat image:", response.text)
        return None

# Replace 'YOUR_API_KEY' with your actual API key from The Cat API
image_url = get_random_cat_image(CATKEY)
if image_url:
    print("Random cat image URL:", image_url)
else:
    print("Failed to fetch a random cat image.")

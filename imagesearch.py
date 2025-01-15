import os
import requests
from dotenv import load_dotenv
from urllib.parse import urlencode

load_dotenv()

api_key = os.getenv('SEARCH_ENGINE_API_KEY')
search_engine_id = os.getenv('SEARCH_ENGINE_ID')

def search_and_save_image_google(keyword, save_folder="output/media/image"):
    """
    Searches for an image using Google Custom Search API and saves it locally.
    
    Args:
        keyword (str): The search term for the image.
        save_folder (str): Directory to save the downloaded image.
        api_key (str): Your Google API Key.
        search_engine_id (str): Your Google Custom Search Engine ID.

    Returns:
        str or None: File path of the saved image if successful, None otherwise.
    """
    try:
        # Validate input parameters
        if not api_key or not search_engine_id:
            print("API Key and Search Engine ID are required.")
            return None
        
        print(f"Searching for image with keyword: '{keyword}'")
        
        # Create the save folder if it doesn't exist
        os.makedirs(save_folder, exist_ok=True)
        
        # Google Custom Search API request
        params = {
            "q": keyword,
            "cx": search_engine_id,
            "key": api_key,
            "searchType": "image",
            "num": 1
        }
        url = f"https://www.googleapis.com/customsearch/v1?{urlencode(params)}"
        response = requests.get(url)
        
        # Check for API response success
        if response.status_code != 200:
            print(f"Failed to fetch image for keyword '{keyword}': {response.text}")
            return None
        
        response_json = response.json()
        if "items" not in response_json or not response_json["items"]:
            print(f"No images found for keyword '{keyword}'")
            return None
        
        # Get the first image URL
        image_url = response_json["items"][0]["link"]
        print(f"Found image URL: {image_url}")
        
        # Download the image content
        image_response = requests.get(image_url)
        if image_response.status_code == 200:
            # Save the image locally
            file_path = os.path.join(save_folder, f"{keyword.replace(' ', '_')}.jpg")
            with open(file_path, "wb") as f:
                f.write(image_response.content)
            print(f"Image saved: {file_path}")
            return file_path
        else:
            print(f"Failed to download image from URL: {image_url}")
            return None
    
    except Exception as e:
        print(f"Error during image search and save: {e}")
        return None


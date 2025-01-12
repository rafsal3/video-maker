import json
import spacy
import requests
from dotenv import load_dotenv
import os

load_dotenv()
# apis declaration
api_key = os.getenv('UNSPLASH_ACCESS_KEY')


# Step 1: Parse Transcript File
def parse_transcript(file_path):
    try:
        print("Transcript parsing ...")
        with open(file_path, 'r') as f:
            transcript = json.load(f)
        text = transcript["text"]
        words = transcript["words"]
        print("Parsing completed ...")
        return text,words
    except Exception as e:
        print(f"Error reading transcript: {e}")
        return None,None


#  keyword Extraction
def extract_keywords(text):
    try:
        print("Extracting keywords ...")
        #  Load spacy model
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text)
        #  extract noune and proper nouns
        keywords = [token.text for token in doc if token.pos_ in ("NOUN","PROPN")]
        print("Keyword extraction completed ...")
        return list(set(keywords)) #remove duplicates
    except Exception as e:
        print(f"Error extracting keywords: {e}")
        return []

# media search

def search_and_save_image(keyword,save_folder="output/media"):
    try:
        print("Collecting images ...")
        # creaete the folder if that doesnt exist
        os.makedirs(save_folder,exist_ok=True)

        # Unsplash API request
        url = f"https://api.unsplash.com/search/photos?query={keyword}&client_id={api_key}&per_page=1"
        response = requests.get(url)
        if response.status_code !=200:
            print(f"Failed to fetch image for keyword '{keyword}': {response.text}")
            return None
        
        results = response.json().get("results", [])
        if not results:
            print(f"No images found for keyword '{keyword}'")
            return None
        
        # get the first image UPL
        image_url = results[0]["urls"]["regular"]

        # Download the image content
        image_response = requests.get(image_url)
        if image_response.status_code == 200:

            # save the image locally
            file_path = os.path.join(save_folder,f"{keyword}.jpg")
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


def map_media_to_timestamps(words, keywords, audio_duration, media_folder="output/media"):
    print("Image collection completed ...")
    print("map media to timestamps started...")
    mappings = []

    # Map keywords to their first occurrence in the words list
    for keyword in keywords:
        for i, word_data in enumerate(words):
            if keyword.lower() in word_data["word"].lower():
                # Extract start timestamp
                start_time = word_data["start"] / 1000

                # Construct the media path
                media_path = f"{media_folder}/{keyword}.jpg"

                # Add to mappings with placeholder end_time
                mappings.append({
                    "keyword": keyword,
                    "start_time": start_time,
                    "end_time": start_time,  # Placeholder
                    "media_path": media_path
                })
                break  # Stop at the first match

    # Sort mappings by start_time
    mappings.sort(key=lambda x: x["start_time"])

    # Adjust end times dynamically for each mapping
    for i in range(len(mappings)):
        if i < len(mappings) - 1:
            # Current mapping's end_time is the next mapping's start_time
            next_start_time = mappings[i + 1]["start_time"]
            mappings[i]["end_time"] = max(next_start_time, mappings[i]["start_time"] + 0.5)
        else:
            # Last mapping's end_time is the audio duration
            mappings[i]["end_time"] = min(audio_duration, mappings[i]["start_time"] + 1.0)
    print("Mapping completed...")
    return mappings




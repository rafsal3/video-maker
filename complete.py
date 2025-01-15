from media import search_and_save_image, parse_transcript, map_media_to_timestamps_v2
from gif import search_and_save_GIF
from audio import generate_audio
from moviepy.editor import *
from transcript import generate_transcript
from script import generate_keywords
import json
import ast

import json

def process_keywords_and_save_media(keyword_list_path):
    # Step 1: Load the keyword list from the JSON file
    try:
        with open(keyword_list_path, 'r') as file:
            keyword_list = json.load(file)
    except Exception as e:
        print(f"Error loading keyword list: {e}")
        return None
    
    saved_media = {}

    # Step 2: Process each keyword and save corresponding media
    for item in keyword_list:
        keyword = item["keyword"]
        media_type = item["type"].lower()

        if media_type == "image":
            # search and save image
            file_path = search_and_save_image(keyword)
            saved_media[keyword] = file_path

        elif media_type == "giph":
            # search and save GIF
            file_path = search_and_save_GIF(keyword)
            saved_media[keyword] = file_path
        else:
            print(f"Unsupported media type '{media_type}' for keyword: {keyword}")

    # Step 3: Save the saved_media dictionary to a JSON file
    output_path = "output/saved_media.json"
    try:
        with open(output_path, 'w') as output_file:
            json.dump(saved_media, output_file, indent=4)
        print(f"Saved media successfully to {output_path}")
    except Exception as e:
        print(f"Error saving media: {e}")

    # Return the dictionary with saved media file paths
    return saved_media


def read_script(file_path):
    with open(file_path, 'r') as file:
        return file.read()




import json
import ast

def create_keyword_list_using_gemini(transcript_file_path):
    # Step 1: Load the transcript JSON file
    try:
        with open(transcript_file_path, 'r') as file:
            transcript_data = json.load(file)
    except Exception as e:
        print(f"Error loading transcript file: {e}")
        return None
    
    # Extract the text from the transcript
    transcript_text = transcript_data.get("text", "")
    if not transcript_text:
        print("No text found in the transcript file")
        return None

    # Step 2: Craft the prompt with the transcript text
    prompt = f"""
    Extract the important words or phrases from the following text and classify each one as either 'image' or 'giph' (GIF). 
    For each keyword, return its classification based on its context:
    - If it's a noun (e.g., person, object, place), classify it as 'image'.
    - If it's a verb or action (e.g., jumping, dancing), classify it as 'giph'.

    Here's the text:

    {transcript_text}

    Please provide the output in the following format:
    [{{'keyword': 'man', 'type': 'image'}}, {{'keyword': 'jumping', 'type': 'giph'}}, ...]
    """
    
    # Step 3: Send the crafted prompt to the Gemini API
    # Replace the following line with the actual API call to Gemini
    response = generate_keywords(prompt)
    print(response)
    
    # Step 4: Clean up the response (remove extra characters, newlines, etc.)
    # If the response is a string with unwanted markdown format, we need to clean it
    cleaned_response = response.strip().strip('```json').strip()

    # Convert the cleaned string into a Python list using ast.literal_eval() for safety
    try:
        keyword_list = ast.literal_eval(cleaned_response)
    except Exception as e:
        print(f"Error in parsing response: {e}")
        return None
    
    # Step 5: Save the cleaned response to a JSON file
    output_file_path = "output/keywords.json"
    with open(output_file_path, 'w') as json_file:
        json.dump(keyword_list, json_file, indent=2)
    
    print(f"Keywords saved to {output_file_path}")
    return output_file_path



if __name__ == "__main__":



    # file_path = "output/script.txt"

    # script_content = read_script(file_path)

    # audio_file_path = generate_audio(script_content)
    # audio_file_path = "output/audio.wav"

    # transcript_file_path = generate_transcript(audio_file_path)

    # Example transcript text
    # transcript_text = "In today's top story, a man is jumping over a car while flying in the sky."
    transcript_file_path = "output/transcript.json"
    keyword_list_path = "output/keywords.json"
    file_path = "output/transcript.json"
    audio_path = "output/audio.wav"

    audio = AudioFileClip(audio_path)
    audio_duration = audio.duration

    text,words = parse_transcript(file_path)
    # keyword_list_path = create_keyword_list_using_gemini(transcript_file_path)
    # saved_media_map = process_keywords_and_save_media(keyword_list_path)
    # Load the media keywords from the JSON file
    with open("output/keywords.json", "r") as file:
        media_keywords = json.load(file)

    mappings = map_media_to_timestamps_v2(words, media_keywords, audio_duration)

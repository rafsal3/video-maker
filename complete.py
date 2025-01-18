from media import search_and_save_image, parse_transcript, map_media_to_timestamps_v2
from gif import search_and_save_GIF
from audio import generate_audio
from moviepy.editor import *
from transcript import generate_transcript
from script import generate_keywords
import json
import ast
import os
from imagesearch import search_and_save_image_google
import re


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
            # Try searching and saving with Google first
            file_path = search_and_save_image_google(keyword)

            if not file_path:  # If Google doesn't return an image, fall back to the other function
                print(f"Google search failed for '{keyword}', trying alternative method.")
                file_path = search_and_save_image(keyword)

            if file_path:
                saved_media[keyword] = file_path
            else:
                print(f"No image found for keyword: {keyword}")

        elif media_type == "gif":
            # Search and save GIF
            file_path = search_and_save_GIF(keyword)

            if file_path:
                saved_media[keyword] = file_path
            else:
                print(f"No GIF found for keyword: {keyword}")

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
    with open(file_path, 'r', encoding='utf-8') as file:
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
    Extract the important words or phrases from the following text and classify each one as either 'image' or 'gif' (GIF). 
    For each keyword, return its classification based on its context:
    - If it's a noun (e.g., person, object, place), classify it as 'image'.
    - If it's a verb or action (e.g., jumping, dancing), classify it as 'gif'.

    Here's the text:

    {transcript_text}

    Please provide the output in the following format:
    [{{'keyword': 'man', 'type': 'image'}}, {{'keyword': 'jumping', 'type': 'gif'}}, ...]
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


# video editor
def create_video_with_moviepy(format, mapping_file, keywords_file, audio_file, output_file, background_color=(16, 12, 46)):
    try:
        print("Video editing started...")

        # Load the audio to determine its duration
        audio = AudioFileClip(audio_file)
        audio_duration = audio.duration

        # Set video format size
        if format == "long":
            sizem = (1280, 720)
        elif format == "short":
            sizem = (720, 1280)
        else:
            raise ValueError("Invalid format. Use 'long' or 'short'.")

        # Load mapping and keywords files
        with open(mapping_file, 'r') as f:
            media_mappings = json.load(f)

        with open(keywords_file, 'r') as f:
            keyword_types = {entry["keyword"]: entry["type"] for entry in json.load(f)}

        # Create a blank background video with the same duration as the audio
        background_video = ColorClip(size=sizem, color=background_color, duration=audio_duration)

        media_clips = []
        for mapping in media_mappings:
            media_path = mapping["media_path"]
            if not os.path.isfile(media_path):
                print(f"Warning: Media file not found: {media_path}")
                continue

            media_type = keyword_types.get(mapping["keyword"], None)
            if media_type == "image":
                # Process image clips
                media_clip = (
                    ImageClip(media_path)
                    .set_duration(mapping["end_time"] - mapping["start_time"])
                    .set_start(mapping["start_time"])
                    .set_position("center")
                )
            elif media_type == "gif":
                # Process video clips
                media_clip = (
                    VideoFileClip(media_path)
                    .subclip(0, mapping["end_time"] - mapping["start_time"])
                    .set_start(mapping["start_time"])
                    .resize(height=sizem[1], width=sizem[0])  # Resize to fit the background
                )
            else:
                print(f"Warning: Unsupported media type for keyword: {mapping['keyword']}")
                continue

            media_clips.append(media_clip)

        # Combine the background and media clips
        final_video = CompositeVideoClip([background_video] + media_clips)

        # Add the audio to the video
        final_video = final_video.set_audio(audio)

        # Write the final video to a file
        final_video.write_videofile(output_file, codec="libx264", fps=24)

        print(f"Video created successfully: {output_file}")

    except Exception as e:
        print(f"Error during video creation: {e}")




def transcript_to_sentences(file_path):
    """
    Converts a word-by-word transcript into a sentence-by-sentence transcript.

    Args:
        file_path (str): The path to the input transcript JSON file.

    Returns:
        str: The path to the output JSON file with sentence-level transcripts.
    """
    # Ensure the output directory exists
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Read the transcript JSON file
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    text = data.get("text", "")
    words = data.get("words", [])
    
    # Split the text into sentences using punctuation
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    sentence_transcripts = []
    sentence_start_index = 0
    
    # Match sentences with timestamps
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        
        sentence_start_time = words[sentence_start_index]["start"]
        sentence_end_time = None
        
        word_count = len(sentence.split())
        sentence_words = words[sentence_start_index:sentence_start_index + word_count]
        
        # Adjust the end timestamp based on the last word in the sentence
        if sentence_words:
            sentence_end_time = sentence_words[-1]["end"]
        
        sentence_transcripts.append({
            "sentence": sentence,
            "start": sentence_start_time,
            "end": sentence_end_time
        })
        
        sentence_start_index += word_count
    
    # Define the output file path
    output_path = os.path.join(output_dir, "sentence_transcript.json")
    
    # Save the sentence-level transcripts to a JSON file
    with open(output_path, 'w', encoding='utf-8') as json_file:
        json.dump(sentence_transcripts, json_file, ensure_ascii=False, indent=4)
    
    return output_path


def script_to_sentences(file_path):

    # Ensure the output directory exists
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    # Read the input file
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Split the content into sentences based on punctuation (?, !, ., ", ,, etc.)
    sentences = re.split(r'(?<=[.!?\"\,])\s+', content)
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]  # Remove empty sentences

    # Define the output file path
    output_path = os.path.join(output_dir, "sentence.json")

    # Save sentences to a JSON file
    with open(output_path, 'w', encoding='utf-8') as json_file:
        json.dump(sentences, json_file, ensure_ascii=False, indent=4)

    return output_path
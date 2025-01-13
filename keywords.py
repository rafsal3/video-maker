import requests
from dotenv import load_dotenv
import os
import json
import google.generativeai as genai

load_dotenv()

google_api_key = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=google_api_key)

try:
    model = genai.GenerativeModel("gemini-1.5-flash")
    print("Model initialized successfully")
except Exception as e:
    print(f"Error initializing model: {e}")


def generate_keywords(file_path):
    try:
        instrunction = """"Generate a JSON array where each object represents a word segment from the provided transcript JSON. Each object should include the following fields:

start: Start time of the word segment.
end: End time of the word segment.
word: The word itself.
prompt: A suggested image or GIF search prompt for this word, if applicable.
type: The type of asset suggested by the prompt ('image' or 'GIF').
The API should prioritize generating prompts for key concepts or visually impactful words within the transcript, leaving 'prompt' and 'type' as 'null' for other words.

"""
        input_text = json.dumps(file_path)
        prompt = instrunction + " " + input_text
        print("Generating media keywords")
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
         # Save transcription result to a JSON file
        transcript_path = "output/keywords.txt"
        os.makedirs(os.path.dirname(transcript_path), exist_ok=True)
        with open(transcript_path, 'w') as text_file:
            text_file.write(response)
        


    except Exception as e:
        return f"Error: {e}"


file_path = "output/transcript.json"
generate_keywords(file_path)
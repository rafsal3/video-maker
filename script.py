import google.generativeai as genai
from dotenv import load_dotenv
import os
import json

# load environement variables from .env file
load_dotenv()

google_api_key = os.getenv('GEMINI_API_KEY')

genai.configure(api_key=google_api_key)


def generate_script(prompt,output_format="json"):
    try:
        print("Generating Script ...")
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        
        if output_format == "json":
            result = {"prompt": prompt, "response": response.text}
            
            # Ensure the output directory exists
            output_dir = "output"
            os.makedirs(output_dir, exist_ok=True)  # Create folder if it doesn't exist
            
            # Save the JSON file
            file_path = os.path.join(output_dir, "script.json")
            print(f"Saving to: {file_path}")
            with open(file_path, "w") as f:
                json.dump(result, f, indent=4)

            
            print(f"JSON saved to {file_path}")
            return result
        
        print("Script saved ...")
        return response.text
    except Exception as e:
        return f"Error: {e}"

def generate_keywords(prompt,output_format="text"):
    try:
        print("Generating Script ...")
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        
        if output_format == "text":
            result = response.text
            
            # Ensure the output directory exists
            output_dir = "output"
            os.makedirs(output_dir, exist_ok=True)  # Create folder if it doesn't exist
            
            # # Save the JSON file
            # file_path = os.path.join(output_dir, "script.json")
            # print(f"Saving to: {file_path}")
            # with open(file_path, "w") as f:
            #     json.dump(result, f, indent=4)
            return result
        
        print("Script saved ...")
        return response.text
    except Exception as e:
        return f"Error: {e}"
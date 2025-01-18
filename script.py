import google.generativeai as genai
from dotenv import load_dotenv
import os
import json

# load environement variables from .env file
load_dotenv()

google_api_key = os.getenv('GEMINI_API_KEY')

genai.configure(api_key=google_api_key)


def generate_script(prompt, output_format="json"):
    try:
        print("Generating Script ...")
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)

        # Ensure the output directory exists
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)  # Create folder if it doesn't exist

        if output_format == "json":
            # Save as JSON file
            result = {"prompt": prompt, "response": response.text}
            file_path = os.path.join(output_dir, "script.json")
            print(f"Saving to: {file_path}")
            with open(file_path, "w") as f:
                json.dump(result, f, indent=4)
            print(f"JSON saved to {file_path}")
            return file_path
        elif output_format == "text":
            # Save only the response text to a plain text file
            file_path = os.path.join(output_dir, "script.txt")
            print(f"Saving to: {file_path}")
            with open(file_path, "w") as f:
                f.write(response.text)
            print(f"Text saved to {file_path}")
            return file_path

        # If an unsupported format is passed
        raise ValueError(f"Unsupported output format: {output_format}")
    except Exception as e:
        return f"Error: {e}"

# def generate_keywords(script,output_format="text"):
#     try:
#         print("Generating keywords ...")
#         model = genai.GenerativeModel("gemini-1.5-flash")
#         response = model.generate_content(script)
        
#         if output_format == "text":
#             result = response.text
            
#             # Ensure the output directory exists
#             output_dir = "output"
#             os.makedirs(output_dir, exist_ok=True)  # Create folder if it doesn't exist
            

#             return result
        
#         print("Script saved ...")
#         return response.text
#     except Exception as e:
#         return f"Error: {e}"

def generate_keywords(script_path, output_file="output/keywords.json", output_format="json"):
    try:
        # Ensure the script file exists
        if not os.path.exists(script_path):
            raise FileNotFoundError(f"Script file not found: {script_path}")
        
        # Read the script from the file with proper encoding
        with open(script_path, "r", encoding="utf-8") as file:
            script = file.read()
        
        print("Generating keywords ...")
        
        # Initialize the Gemini model
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        # Updated prompt to include clear instruction with proper syntax for JSON format
        prompt = f"""
        Please extract key phrases or words from the following script, categorize them based on the following types, 
        and return the result as a JSON list:
        - **image**: For objects, places, or concepts that can be visually represented.
        - **gif**: For actions, events, or dynamic concepts.
        - **text**: For abstract concepts, emotions, or anything that's difficult to represent visually.

        **Script:**  
        {script}

        For each keyword or phrase, please identify the type it belongs to (image, gif, or text) and return the result in the following format:

        {{
          "keyword": "extracted keyword or phrase",
          "type": "image/gif/text"
        }}
        the output have to be row json format. no other characters
        """
        
        # Generate keywords from the script
        response = model.generate_content(prompt)
        
        # Debug: Print raw response for inspection
        print("Raw API Response:", response.text)
        
        # Clean the response to remove backticks
        response_text = response.text.strip("```")
        
        # Process response based on the desired output format
        if output_format == "json":
            try:
                # Attempt to parse the cleaned response as JSON
                result = json.loads(response_text)
            except json.JSONDecodeError:
                print("The API response is not valid JSON. Check the raw response above.")
                return None
            
            # Save the result to a file
            output_dir = os.path.dirname(output_file)
            os.makedirs(output_dir, exist_ok=True)  # Ensure the output directory exists
            
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=4, ensure_ascii=False)
            
            print(f"Keywords saved to {output_file}")
            return result
        
        elif output_format == "text":
            # Plain text output
            result = response_text
            
            # Save the result to a file
            output_dir = os.path.dirname(output_file)
            os.makedirs(output_dir, exist_ok=True)
            
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(result)
            
            print(f"Script saved to {output_file}")
            return result
        
        else:
            raise ValueError(f"Unsupported output format: {output_format}")
    
    except FileNotFoundError as fnf_error:
        print(fnf_error)
        return None
    except Exception as e:
        print(f"Error generating keywords: {e}")
        return None
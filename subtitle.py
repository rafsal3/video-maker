import json
import os


def create_subtitles(transcript_path, output_path="output/subtitle.srt"):
    try:
        with open(transcript_path, 'r') as f:
            transcript_data = json.load(f)

        subtitles = []
        prev_end_time = 0

        for word in transcript_data['words']:
            start_time = word['start'] / 1000  # Convert milliseconds to seconds
            end_time = word['end'] / 1000

            subtitle = {
                'start': prev_end_time,
                'end': end_time,
                'text': word['word']
            }

            subtitles.append(subtitle)
            prev_end_time = end_time

        # Create the output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, 'w') as f:
            for idx, subtitle in enumerate(subtitles):
                start_time_ms = int(subtitle['start'] * 1000)
                end_time_ms = int(subtitle['end'] * 1000)
                f.write(f"{idx+1}\n")
                f.write(f"{start_time_ms} --> {end_time_ms}\n")
                f.write(f"{subtitle['text']}\n\n")

    except FileNotFoundError:
        print(f"Error: Transcript file not found at '{transcript_path}'")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{transcript_path}'")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")





transcript_file = 'output/transcript.json' 
create_subtitles(transcript_file) 
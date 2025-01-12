import assemblyai as aai
from dotenv import load_dotenv
import json
import os

def generate_transcript(audio_file_path):
    print("Generating Transcript ...")
    # Load environment variables
    load_dotenv()

    # AssemblyAI API setup
    api_key = os.getenv('ASSEMBLY_AI_API_KEY')
    if not api_key:
        raise EnvironmentError("ASSEMBLY_AI_API_KEY not found in environment variables.")
    aai.settings.api_key = api_key

    # Check if audio file exists
    if not os.path.exists(audio_file_path):
        raise FileNotFoundError(f"Audio file not found: {audio_file_path}")

    # Initialize transcription
    transcriber = aai.Transcriber()

    # Transcription configuration setup
    config = aai.TranscriptionConfig(
        word_boost=None,  # Add keywords to boost recognition accuracy (optional)
        boost_param=None,
        speaker_labels=False,  # Enable if you want speaker identification
        punctuate=True,  # Add punctuation to the transcription
        format_text=True   # Format text for readability
    )

    try:
        # Perform transcription
        transcript = transcriber.transcribe(audio_file_path, config)

        if transcript.status == aai.TranscriptStatus.error:
            raise Exception(f"Transcription failed: {transcript.error}")

        # Collect transcription result
        transcription_result = {
            "text": transcript.text,
            "words": [
                {
                    "start": word.start,
                    "end": word.end,
                    "word": word.text
                }
                for word in transcript.words
            ],
        }

        # Save transcription result to a JSON file
        transcript_path = "output/transcript.json"
        os.makedirs(os.path.dirname(transcript_path), exist_ok=True)
        with open(transcript_path, 'w') as json_file:
            json.dump(transcription_result, json_file, indent=4)
        print("Transcript saved ...")
        return transcript_path

    except Exception as e:
        raise Exception(f"Error in transcription: {e}")
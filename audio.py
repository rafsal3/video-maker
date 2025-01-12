from pyht import Client
from pyht.client import TTSOptions
from dotenv import load_dotenv
import os

load_dotenv()

# Play.ht API credentials
USER_ID = os.getenv('PLAY_USER_ID')
SECRET_KEY = os.getenv('PLAY_SECRET_KEY')

# initialize play.ht client

client = Client(user_id=USER_ID,api_key=SECRET_KEY)


def generate_audio(script):

    print("Generating Audio...")
     # Voice manifest URL (or fallback voice)
    voice_manifest_url = "s3://voice-cloning-zero-shot/775ae416-49bb-4fb6-bd45-740f205d20a1/jennifersaad/manifest.json"

    # tts option
    options = TTSOptions(
        voice = voice_manifest_url
    )

    # output folder
    output_dir = "output"
    os.makedirs(output_dir,exist_ok=True) #create folder if not already exist

    # file path for the audio outpu
    file_path = os.path.join(output_dir,"audio.wav")

    try:
        # open the output file to write the audio
        with open(file_path,"wb") as audio_file:
            for chunk in client.tts(script,options,voice_engine='PlayDialog-http'):
                # write the audio chunk to the file
                audio_file.write(chunk)
        print(f"audio generated and saved as{file_path}")
        return file_path #return file path of saved audio file
    except Exception as e:
        print (f"Error: {e}")
        return None 

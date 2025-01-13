import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()

api_key = os.getenv('TENOR_API_KEY')
lmt = 1
ckey = os.getenv('C_KEY')



def search_and_save_GIF(search_term):
    # get the gif
    r = requests.get("https://tenor.googleapis.com/v2/search?q=%s&key=%s&client_key=%s&limit=%s" % (search_term, api_key, ckey,  lmt))

    if r.status_code == 200:
        gif_data = json.loads(r.content)

        save_folder = "output/media/gifs"
        os.makedirs(save_folder,exist_ok=True)

        # etxtract the MP$ URL
        mp4_url = gif_data["results"][0]["media_formats"]["mp4"]["url"]

        # dowload the MP$ file
        mp4_response = requests.get(mp4_url)

        file_path = os.path.join(save_folder,f"{search_term}.mp4")

        if mp4_response.status_code == 200:
            # save the file locally
            with open(file_path, "wb") as f:
                f.write(mp4_response.content)
            print("MP4 file downloaded successfully as 'output.mp4'.")
            return file_path
        else:
            print("Failed to download the MP4 file.")
        
    else:
        print("Failed to fetch GIF data.")


# import my custom functions here
from script import generate_script
from complete import read_script, create_keyword_list_using_gemini, create_video_with_moviepy, process_keywords_and_save_media
from audio import generate_audio
from transcript import generate_transcript
from media import parse_transcript, map_media_to_timestamps_v2

# import from general libraries
from moviepy.editor import *
import json

if __name__ == "__main__":

    # create script
    # prompt = input("Enter you prompt")
    script_file_path = "output/script.txt"
    # script_file_path = generate_script(prompt,output_format="text")
    # script_content = read_script(script_file_path)

    # create audio
    # audio_file_path = generate_audio(script_content)
    audio_file_path = "output/audio.wav"
    audio = AudioFileClip(audio_file_path)
    audio_duration = audio.duration

    # create transcript
    # transcript_file_path = generate_transcript(audio_file_path)
    transcript_file_path = "output/transcript.json"
    text,words = parse_transcript(transcript_file_path)

    # create keyword list
    # keyword_list_path = create_keyword_list_using_gemini(transcript_file_path)
    keyword_list_path = "output/keywords.json"

    # saved_media_map = process_keywords_and_save_media(keyword_list_path)

    # loading media keywords
    with open("output/keywords.json", "r") as file:
        media_keywords = json.load(file)

    # mapping media to timestamps
    mapping_file  = map_media_to_timestamps_v2(words, media_keywords, audio_duration)
    # mapping_file = "output/mappings.json"

    video_format = "long"

    create_video_with_moviepy(
    format=video_format,
    mapping_file=mapping_file,
    keywords_file=keyword_list_path,
    audio_file=audio_file_path,
    output_file="output/final.mp4",

)





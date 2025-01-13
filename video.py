from moviepy.editor import *
from media import map_media_to_timestamps ,parse_transcript, extract_keywords, search_and_save_image
from script import generate_script
from transcript import generate_transcript
from audio import generate_audio
from gif import search_and_save_GIF
import os




from moviepy.editor import ColorClip, ImageClip, AudioFileClip, CompositeVideoClip

def create_video_with_moviepy(format,media_mappings, audio_file, output_file, background_color=(0, 0, 0)):
    try:
        print("video editing started ...")
        # load the audio to determines its duration
        audio = AudioFileClip(audio_file)
        audio_duration = audio.duration

        # format
        if format == "long":
            sizem = (1280,720)
        elif format == "short":
            sizem = (720,1280)

        # create blank bg video with the same duration as the audio
        background_video = ColorClip(size=sizem, color=background_color,duration=audio_duration)

        image_clips = []
        for mapping in media_mappings:
            image_clip = (
                ImageClip(mapping["media_path"])
                .set_duration(mapping["end_time"]-mapping["start_time"])
                .set_start(mapping["start_time"])
                .set_position("center")
            )
            image_clips.append(image_clip)

        # combine the background and image clips
        final_video = CompositeVideoClip([background_video] + image_clips)

        # add the audio to the video
        final_video = final_video.set_audio(audio)

        # write the final video to a file
        final_video.write_videofile(output_file,codec="libx264", fps=24)

        print(f"Video created successfully: {output_file}")

    except Exception as e:
        print(f"Error during video creation: {e}") 






def make_video(format,prompt):
    print("Starting processing...")
    result_as_json = generate_script(prompt)
    script = result_as_json["response"]
    audio_path = generate_audio(script)
    file_path = generate_transcript(audio_path)


 
  
    text,words = parse_transcript(file_path)
    keywords = extract_keywords(text)

    audio = AudioFileClip(audio_path)
    audio_duration = audio.duration

    # Final output video file
    output_file = "output/final_video.mp4"

    for keyword in keywords:
        saved_image_path = search_and_save_image(keyword)
        # saved_image_path = search_and_save_GIF(keyword)
        print(f"Saved Image Path: {saved_image_path}")

    mappings = map_media_to_timestamps(words,keywords,audio_duration)
    create_video_with_moviepy(format,mappings,audio_path,output_file,)



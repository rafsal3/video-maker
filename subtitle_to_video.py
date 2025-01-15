from moviepy.editor import *
import re
from moviepy.video.tools.subtitles import SubtitlesClip

def parse_srt(srt_path):
    """
    Parses a non-standard SRT file into a list of subtitle entries.

    Args:
        srt_path: Path to the .srt file.
    
    Returns:
        A list of subtitle entries where each entry is a tuple of
        (start_time, end_time, text).
    """
    with open(srt_path, 'r', encoding='utf-8') as f:
        srt_content = f.read()
    
    # Regular expression to parse non-standard SRT content
    pattern = r'(\d+)\n(\d+) --> (\d+)\n(.*?)\n\n'
    matches = re.findall(pattern, srt_content, re.DOTALL)
    
    if not matches:
        print("No subtitles found in the SRT file.")
    
    subtitles = []
    for match in matches:
        start_time = int(match[1]) / 1000  # Convert milliseconds to seconds
        end_time = int(match[2]) / 1000    # Convert milliseconds to seconds
        text = match[3].strip()
        subtitles.append(((start_time, end_time), text))
    
    print(f"Parsed {len(subtitles)} subtitles.")
    return subtitles

def add_subtitles_to_video(video_path, srt_path, output_path):
    """
    Adds subtitles to a video using MoviePy.

    Args:
        video_path: Path to the input video file.
        srt_path: Path to the non-standard SRT subtitle file.
        output_path: Path to save the output video with subtitles.
    """
    # Load video
    video = VideoFileClip(video_path)
    
    # Parse subtitles from the .srt file
    subtitle_data = parse_srt(srt_path)
    
    if not subtitle_data:
        raise ValueError("No subtitles to process. Check your SRT file format.")
    
    # Define a function to generate TextClip objects for each subtitle
    def generate_subtitle_clip(txt):
        return TextClip(txt, font="Arial", fontsize=24, color='white', bg_color='black')
    
    # Create SubtitlesClip object
    subtitles = SubtitlesClip(subtitle_data, generate_subtitle_clip)
    
    # Overlay subtitles on the video
    final_clip = CompositeVideoClip([video, subtitles.set_pos(('center', 'bottom'))])
    
    # Export the video with subtitles
    final_clip.write_videofile(
        output_path,
        fps=video.fps,
        temp_audiofile="temp-audio.m4a",
        remove_temp=True,
        codec="libx264",
        audio_codec="aac"
    )

# Example usage
video_path = "output/final_video.mp4"  # Replace with your input video path
srt_path = "output/subtitle.srt"  # Path to the non-standard SRT subtitle file
output_path = "output/output_video_with_subtitles.mp4"  # Replace with your desired output path
add_subtitles_to_video(video_path, srt_path, output_path)

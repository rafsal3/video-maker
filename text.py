import json
import os
import pygame
import shutil
import random
from moviepy.editor import ImageSequenceClip

# Define a color palette with visually appealing colors
COLOR_PALETTE = [
    (255, 255, 255),    # White
    (255, 200, 87),     # Golden Yellow
    (87, 199, 255),     # Sky Blue
    (255, 87, 87),      # Coral Red
    (138, 255, 87),     # Lime Green
    (255, 87, 255),     # Pink
    (87, 255, 255),     # Cyan
    (255, 162, 87),     # Orange
    (167, 87, 255),     # Purple
    (87, 255, 198),     # Turquoise
]

def create_text_video(word, temp_folder="temp_frames", final_folder="final_videos"):
    # Create folders
    os.makedirs(temp_folder, exist_ok=True)
    os.makedirs(final_folder, exist_ok=True)
    
    # Video settings
    resolution = (1280, 720)  # HD resolution
    fps = 24  # Frame rate
    duration = 5  # Video duration in seconds

    # Text settings
    font = pygame.font.Font(None, 100)
    black = (0, 0, 0)
    
    # Randomly select a color for this video
    text_color = random.choice(COLOR_PALETTE)
    print(f"Using color RGB{text_color} for text: {word}")

    # Pygame display
    screen = pygame.Surface(resolution)

    # Calculate text reveal timing
    total_frames = int(fps * duration)
    letters_per_frame = len(word) / (fps * (duration / 2))  # Reveal text in half the duration

    # Render frames
    frames = []
    for i in range(total_frames):
        revealed_count = min(len(word), int(i * letters_per_frame))
        revealed_text = word[:revealed_count]

        # Clear screen
        screen.fill(black)

        # Render text with the randomly selected color
        text_surface = font.render(revealed_text, True, text_color)
        text_rect = text_surface.get_rect(center=(resolution[0] // 2, resolution[1] // 2))
        screen.blit(text_surface, text_rect)

        # Save frame as image
        frame_path = os.path.join(temp_folder, f"frame_{i:04d}.png")
        pygame.image.save(screen, frame_path)
        frames.append(frame_path)

    # Create video using MoviePy
    clip = ImageSequenceClip(frames, fps=fps)
    output_path = os.path.join(final_folder, f"{word.replace(' ', '_')}.mp4")
    clip.write_videofile(output_path, codec="libx264", fps=fps)

    # Clean up temporary frames
    for frame in frames:
        os.remove(frame)
    
    # Remove only the temporary frames folder
    shutil.rmtree(temp_folder)
    
    return output_path

def create_videos_from_keywords(json_file_path, final_folder="final_videos"):
    # Ensure the final videos folder exists
    os.makedirs(final_folder, exist_ok=True)
    
    # Load and process keywords
    with open(json_file_path, "r", encoding="utf-8") as file:
        keywords = json.load(file)
    
    created_videos = []
    for item in keywords:
        if item["type"] == "text":
            word = item["keyword"]
            print(f"\nCreating video for keyword: {word}")
            video_path = create_text_video(word, temp_folder="temp_frames", final_folder=final_folder)
            created_videos.append(video_path)
    
    # Print summary of created videos
    print("\nCreated videos:")
    for video in created_videos:
        print(f"- {video}")
    print(f"\nAll videos have been saved in the '{final_folder}' folder")

# Usage
if __name__ == "__main__":
    create_videos_from_keywords("output/keywords.json", final_folder="final_videos")
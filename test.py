import json
import os
import pygame
import shutil
import random
import math
from moviepy.editor import ImageSequenceClip

# Enhanced color palette with gradients
GRADIENT_PAIRS = [
    ((255, 87, 87), (167, 87, 255)),    # Red to Purple
    ((87, 199, 255), (138, 255, 87)),   # Blue to Green
    ((255, 200, 87), (255, 87, 255)),   # Gold to Pink
    ((87, 255, 255), (87, 255, 198)),   # Cyan to Turquoise
]

class TextEffect:
    def __init__(self, word, resolution):
        self.word = word
        self.resolution = resolution
        self.font_base_size = 100
        self.gradient = random.choice(GRADIENT_PAIRS)
        
    def get_gradient_color(self, pos, t):
        """Get color from gradient based on position and time"""
        color1, color2 = self.gradient
        factor = (math.sin(t * 2 + pos) + 1) / 2
        return tuple(int(c1 * (1 - factor) + c2 * factor) 
                    for c1, c2 in zip(color1, color2))
    
    def apply_wave_effect(self, text_pos, t, amplitude=20):
        """Apply sine wave movement to text position"""
        return (text_pos[0], 
                text_pos[1] + math.sin(t * 4) * amplitude)
    
    def apply_scale_effect(self, size, t):
        """Scale text size based on time"""
        scale = 1 + math.sin(t * 3) * 0.2
        return int(size * scale)
    
    def create_particle_background(self, surface, t):
        """Create animated particle background"""
        num_particles = 50
        for i in range(num_particles):
            x = (i * 50 + t * 100) % self.resolution[0]
            y = (math.sin(x / 100 + t) * 100 + self.resolution[1]/2) % self.resolution[1]
            pygame.draw.circle(surface, (30, 30, 30), (int(x), int(y)), 3)

    def render_frame(self, revealed_text, t):
        """Render a single frame with all effects"""
        surface = pygame.Surface(self.resolution)
        
        # Create dynamic background
        surface.fill((0, 0, 0))
        self.create_particle_background(surface, t)
        
        # Calculate dynamic font size
        font_size = self.apply_scale_effect(self.font_base_size, t)
        font = pygame.font.Font(None, font_size)
        
        # Render each letter separately with gradient effect
        x_offset = 0
        for i, char in enumerate(revealed_text):
            if char.strip():  # Skip spaces in special effects
                # Get color from gradient
                color = self.get_gradient_color(i / len(self.word), t)
                
                # Render character
                char_surface = font.render(char, True, color)
                
                # Calculate position with wave effect
                char_pos = self.apply_wave_effect(
                    (self.resolution[0]/2 - len(revealed_text)*font_size/4 + x_offset,
                     self.resolution[1]/2),
                    t + i/5)
                
                # Add glow effect
                glow_surface = pygame.Surface(char_surface.get_size(), pygame.SRCALPHA)
                pygame.draw.rect(glow_surface, (*color, 50), 
                               char_surface.get_rect().inflate(10, 10), 
                               border_radius=5)
                
                # Blit glow and character
                surface.blit(glow_surface, 
                           (char_pos[0] - 5, char_pos[1] - 5))
                surface.blit(char_surface, char_pos)
                
                x_offset += char_surface.get_width()
            else:
                x_offset += font_size/3
                
        return surface

def create_text_video(word, temp_folder="temp_frames", final_folder="final_videos"):
    os.makedirs(temp_folder, exist_ok=True)
    os.makedirs(final_folder, exist_ok=True)
    
    # Video settings
    resolution = (1280, 720)
    fps = 24
    duration = 5
    
    # Initialize text effect
    effect = TextEffect(word, resolution)
    
    # Render frames
    frames = []
    total_frames = int(fps * duration)
    letters_per_frame = len(word) / (fps * (duration / 2))
    
    for i in range(total_frames):
        t = i / fps  # Current time in seconds
        revealed_count = min(len(word), int(i * letters_per_frame))
        revealed_text = word[:revealed_count]
        
        # Render frame with effects
        surface = effect.render_frame(revealed_text, t)
        
        # Save frame
        frame_path = os.path.join(temp_folder, f"frame_{i:04d}.png")
        pygame.image.save(surface, frame_path)
        frames.append(frame_path)
    
    # Create video
    clip = ImageSequenceClip(frames, fps=fps)
    output_path = os.path.join(final_folder, f"{word.replace(' ', '_')}.mp4")
    clip.write_videofile(output_path, codec="libx264", fps=fps)
    
    # Cleanup
    for frame in frames:
        os.remove(frame)
    shutil.rmtree(temp_folder)
    
    return output_path

def create_videos_from_keywords(json_file_path, final_folder="final_videos"):
    os.makedirs(final_folder, exist_ok=True)
    
    with open(json_file_path, "r", encoding="utf-8") as file:
        keywords = json.load(file)
    
    created_videos = []
    for item in keywords:
        if item["type"] == "text":
            word = item["keyword"]
            print(f"\nCreating video for keyword: {word}")
            video_path = create_text_video(word, temp_folder="temp_frames", 
                                         final_folder=final_folder)
            created_videos.append(video_path)
    
    print("\nCreated videos:")
    for video in created_videos:
        print(f"- {video}")
    print(f"\nAll videos have been saved in the '{final_folder}' folder")

if __name__ == "__main__":
    create_videos_from_keywords("output/keywords.json", final_folder="final_videos")
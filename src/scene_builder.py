"""
Scene Builder
Composes scenes: background + character + text.
Matches the video's scene composition exactly.
"""
from moviepy.editor import CompositeVideoClip, ImageClip
from PIL import Image
import numpy as np
from pathlib import Path

class SceneBuilder:
    """
    Builds individual scenes with characters and text overlays.
    """
    
    def __init__(self, background_path, video_size=(1080, 1920)):
        self.background = ImageClip(str(background_path))
        self.video_width, self.video_height = video_size
        self.background = self.background.resize(video_size)
    
    def create_scene(self, character_path, text_clip, character_position="bottom"):
        """
        Creates a scene with character and text.
        
        character_position: "bottom", "center", "top", "right"
        """
        # Load and resize character
        character = ImageClip(str(character_path))
        
        # Scale character to fit nicely (about 40% of screen height)
        target_height = int(self.video_height * 0.4)
        scale_factor = target_height / character.h
        character = character.resize(scale_factor)
        
        # Position character
        char_x = (self.video_width - character.w) // 2
        
        if character_position == "bottom":
            char_y = int(self.video_height * 0.55)
        elif character_position == "top":
            char_y = int(self.video_height * 0.1)
        elif character_position == "right":
            char_x = int(self.video_width * 0.55)
            char_y = int(self.video_height * 0.5)
        else:  # center
            char_y = (self.video_height - character.h) // 2
        
        character = character.set_position((char_x, char_y))
        
        # Position text at top (like in video)
        text_clip = text_clip.set_position(("center", 100))
        
        # Composite everything together
        scene = CompositeVideoClip([
            self.background,
            character,
            text_clip
        ], size=(self.video_width, self.video_height))
        
        return scene

# Test
if __name__ == "__main__":
    from text_overlay import TextOverlay
    
    # Build a test scene
    builder = SceneBuilder("assets/backgrounds/dotted_grid.png")
    
    text_gen = TextOverlay("assets/fonts/bold_font.ttf")
    text_clip = text_gen.create_word_by_word(["A", "man"], word_duration=1.0)
    
    scene = builder.create_scene(
        "assets/characters/detective.png",
        text_clip,
        character_position="bottom"
    )
    scene.set_duration(2).write_videofile("output/test_scene.mp4", fps=30)
    print("Test scene created: output/test_scene.mp4")

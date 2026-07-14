"""
Text Overlay Engine
Creates bold text with white stroke + word-by-word reveal animation.
Matches the analyzed video style exactly.
"""
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from moviepy.editor import ImageClip, concatenate_videoclips
from pathlib import Path

class TextOverlay:
    """
    Creates text overlays with white stroke + black fill,
    exactly like the analyzed video.
    """
    
    def __init__(self, font_path, font_size=80):
        self.font_path = font_path
        self.font_size = font_size
        try:
            self.font = ImageFont.truetype(str(font_path), font_size)
        except:
            print(f"Warning: Could not load font {font_path}, using default")
            self.font = ImageFont.load_default()
    
    def create_text_image(self, text, width=1080, height=300):
        """
        Creates a transparent PNG with styled text.
        Returns: PIL Image with alpha channel
        """
        img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Calculate text position (centered)
        bbox = draw.textbbox((0, 0), text, font=self.font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (width - text_width) // 2
        y = (height - text_height) // 2
        
        # Draw white stroke (outline)
        stroke_width = 3
        for dx in range(-stroke_width, stroke_width + 1):
            for dy in range(-stroke_width, stroke_width + 1):
                if dx != 0 or dy != 0:
                    draw.text(
                        (x + dx, y + dy), 
                        text, 
                        font=self.font, 
                        fill=(255, 255, 255, 255)
                    )
        
        # Draw black fill text
        draw.text((x, y), text, font=self.font, fill=(0, 0, 0, 255))
        
        return img
    
    def create_word_by_word(self, words, word_duration=0.6, fps=30):
        """
        Creates word-by-word reveal animation (like the video).
        Each word appears for word_duration seconds.
        """
        clips = []
        
        for i in range(len(words)):
            # Build cumulative text
            cumulative_text = " ".join(words[:i+1])
            img = self.create_text_image(cumulative_text)
            
            frame = np.array(img)
            clip = ImageClip(frame).set_duration(word_duration)
            clips.append(clip)
        
        return concatenate_videoclips(clips, method="compose")

# Test
if __name__ == "__main__":
    from pathlib import Path
    
    text_overlay = TextOverlay(
        font_path=Path("assets/fonts/bold_font.ttf"),
        font_size=80
    )
    
    # Test word-by-word animation
    words = ["Detectives", "say", "if", "you", "can", "solve", "this,"]
    clip = text_overlay.create_word_by_word(words, word_duration=0.8)
    clip.write_videofile("output/test_text.mp4", fps=30)
    print("Test video created: output/test_text.mp4")

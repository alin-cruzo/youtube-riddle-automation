"""
Simplified Video Generator
Builds complete riddle videos efficiently without hanging.
"""
from moviepy.editor import ImageSequenceClip, AudioFileClip, afx
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from pathlib import Path

class SimpleVideoGenerator:
    def __init__(self, assets_dir="assets", output_dir="output"):
        self.assets_dir = Path(assets_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Load font
        try:
            self.font = ImageFont.truetype(str(self.assets_dir / "fonts" / "bold_font.ttf"), 80)
        except:
            self.font = ImageFont.load_default()
            print("Warning: Using default font")
        
        # Load background
        self.bg = Image.open(self.assets_dir / "backgrounds" / "dotted_grid.png").convert("RGBA")
    
    def draw_text_with_stroke(self, draw, text, x, y, font, fill=(0,0,0), stroke=(255,255,255), stroke_width=3):
        """Draw text with white stroke outline."""
        for dx in range(-stroke_width, stroke_width+1):
            for dy in range(-stroke_width, stroke_width+1):
                if dx != 0 or dy != 0:
                    draw.text((x+dx, y+dy), text, font=font, fill=stroke)
        draw.text((x, y), text, font=font, fill=fill)
    
    def create_frame(self, character_name, text, width=1080, height=1920):
        """Create a single frame with background + character + text."""
        # Start with background
        frame = self.bg.copy().resize((width, height))
        
        # Add character if specified
        if character_name:
            char_path = self.assets_dir / "characters" / f"{character_name}.png"
            if char_path.exists():
                char = Image.open(char_path).convert("RGBA")
                # Scale character to ~40% of height
                target_h = int(height * 0.4)
                scale = target_h / char.height
                char = char.resize((int(char.width * scale), target_h))
                # Position at bottom center
                x = (width - char.width) // 2
                y = int(height * 0.55)
                frame.paste(char, (x, y), char)
        
        # Add text at top
        draw = ImageDraw.Draw(frame)
        bbox = draw.textbbox((0, 0), text, font=self.font)
        text_w = bbox[2] - bbox[0]
        x = (width - text_w) // 2
        y = 100
        self.draw_text_with_stroke(draw, text, x, y, self.font)
        
        return np.array(frame.convert("RGB"))
    
    def generate_video(self, riddle_data, output_name="riddle.mp4"):
        """Generate complete video from riddle data."""
        frames = []
        fps = 30
        
        # Helper: add frames for a scene
        def add_scene(character, text, duration):
            frame = self.create_frame(character, text)
            for _ in range(int(duration * fps)):
                frames.append(frame)
        
        # HOOK
        add_scene("detective", "Detectives say if you can solve this,", 2)
        add_scene("two_brains", "you're either a genius or a psychopath.", 2)
        
        # SETUP
        add_scene("victim", "A man was found dead in his living room", 2.5)
        add_scene("victim", "early morning while drinking coffee.", 2.5)
        
        # POLICE
        add_scene("police", "The police were called and questioned everyone.", 3)
        
        # SUSPECTS
        for suspect in riddle_data["suspects"]:
            add_scene(suspect["character"], f"The {suspect['name']} said...", 1.5)
            add_scene(suspect["character"], suspect["alibi"], suspect["duration"])
        
        # CHALLENGE
        add_scene("detective", "Did you figure out who it was?", 3)
        
        # CTA
        add_scene("detective", "Comment your answer below", 2)
        add_scene("detective", "share with your psychopath friends.", 2)
        
        # Create video from frames
        print(f"Creating video with {len(frames)} frames...")
        clip = ImageSequenceClip(frames, fps=fps)
        
        # Add audio if available
        try:
            music = AudioFileClip(str(self.assets_dir / "music" / "mystery_bg.mp3"))
            if music.duration < clip.duration:
                music = afx.audio_loop(music, duration=clip.duration)
            else:
                music = music.subclip(0, clip.duration)
            music = music.volumex(0.3)
            clip = clip.set_audio(music)
        except Exception as e:
            print(f"No music: {e}")
        
        # Save
        output_path = self.output_dir / output_name
        clip.write_videofile(str(output_path), fps=fps, verbose=False, logger=None)
        print(f"Done: {output_path}")
        return output_path

# Test data
TEST_RIDDLE = {
    "suspects": [
        {"name": "wife", "alibi": "she was outside getting vegetables.", "character": "wife", "duration": 3},
        {"name": "brother", "alibi": "he was walking his dog.", "character": "brother", "duration": 3},
        {"name": "son", "alibi": "he was showering in his room.", "character": "son", "duration": 3},
        {"name": "maid", "alibi": "she was getting clothes from outside.", "character": "maid", "duration": 3},
        {"name": "cook", "alibi": "he was preparing eggs for breakfast.", "character": "cook", "duration": 3},
    ]
}

if __name__ == "__main__":
    gen = SimpleVideoGenerator()
    gen.generate_video(TEST_RIDDLE, "first_riddle.mp4")

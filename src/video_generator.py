"""
Complete Video Generator
Generates full riddle videos matching the analyzed video style.
"""
from moviepy.editor import concatenate_videoclips, AudioFileClip, afx
from pathlib import Path
from text_overlay import TextOverlay
from scene_builder import SceneBuilder

class RiddleVideoGenerator:
    """
    Generates complete riddle videos.
    """
    
    def __init__(self, assets_dir="assets", output_dir="output"):
        self.assets_dir = Path(assets_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        self.text_overlay = TextOverlay(
            self.assets_dir / "fonts" / "bold_font.ttf"
        )
        self.scene_builder = SceneBuilder(
            self.assets_dir / "backgrounds" / "dotted_grid.png"
        )
    
    def generate_video(self, riddle_data, output_filename=None):
        """
        Generates a complete video from riddle data.
        """
        scenes = []
        
        # === HOOK SCENE ===
        hook_words = riddle_data["hook"]["text"].split()
        hook_text = self.text_overlay.create_word_by_word(hook_words, word_duration=0.6)
        hook_scene = self.scene_builder.create_scene(
            self.assets_dir / "characters" / "detective.png",
            hook_text,
            character_position="bottom"
        ).set_duration(riddle_data["hook"]["duration"])
        scenes.append(hook_scene)
        
        # === HOOK CONTINUATION ===
        hook2_words = riddle_data["hook"]["continuation"].split()
        hook2_text = self.text_overlay.create_word_by_word(hook2_words, word_duration=0.6)
        hook2_scene = self.scene_builder.create_scene(
            self.assets_dir / "characters" / "two_brains.png",
            hook2_text,
            character_position="center"
        ).set_duration(3)
        scenes.append(hook2_scene)
        
        # === SETUP SCENE ===
        setup_words = riddle_data["setup"]["text"].split()
        setup_text = self.text_overlay.create_word_by_word(setup_words, word_duration=0.5)
        setup_scene = self.scene_builder.create_scene(
            self.assets_dir / "characters" / riddle_data["setup"]["character"] + ".png",
            setup_text,
            character_position="bottom"
        ).set_duration(riddle_data["setup"]["duration"])
        scenes.append(setup_scene)
        
        # === POLICE SCENE ===
        police_words = ["The", "police", "were", "called", "and", "questioned", "everyone."]
        police_text = self.text_overlay.create_word_by_word(police_words, word_duration=0.4)
        police_scene = self.scene_builder.create_scene(
            self.assets_dir / "characters" / "police.png",
            police_text,
            character_position="right"
        ).set_duration(3)
        scenes.append(police_scene)
        
        # === SUSPECTS SCENES ===
        for suspect in riddle_data["suspects"]:
            # Name intro
            intro_words = [f"The {suspect['name']}", "said..."]
            intro_text = self.text_overlay.create_word_by_word(intro_words, word_duration=0.5)
            intro_scene = self.scene_builder.create_scene(
                self.assets_dir / "characters" / suspect["character"] + ".png",
                intro_text,
                character_position="bottom"
            ).set_duration(1.5)
            scenes.append(intro_scene)
            
            # Alibi
            alibi_words = suspect["alibi"].split()
            alibi_text = self.text_overlay.create_word_by_word(alibi_words, word_duration=0.4)
            alibi_scene = self.scene_builder.create_scene(
                self.assets_dir / "characters" / suspect["character"] + ".png",
                alibi_text,
                character_position="bottom"
            ).set_duration(suspect["duration"])
            scenes.append(alibi_scene)
        
        # === CHALLENGE SCENE ===
        challenge_words = riddle_data["challenge"]["text"].split()
        challenge_text = self.text_overlay.create_word_by_word(challenge_words, word_duration=0.5)
        challenge_scene = self.scene_builder.create_scene(
            self.assets_dir / "characters" / "detective.png",
            challenge_text,
            character_position="bottom"
        ).set_duration(riddle_data["challenge"]["duration"])
        scenes.append(challenge_scene)
        
        # === CTA SCENE ===
        cta_words = riddle_data["cta"]["text"].split()
        cta_text = self.text_overlay.create_word_by_word(cta_words, word_duration=0.5)
        cta_scene = self.scene_builder.create_scene(
            self.assets_dir / "characters" / "detective.png",
            cta_text,
            character_position="bottom"
        ).set_duration(riddle_data["cta"]["duration"])
        scenes.append(cta_scene)
        
        # === COMBINE ALL SCENES ===
        final_video = concatenate_videoclips(scenes, method="compose")
        
        # Add background music
        try:
            music = AudioFileClip(str(self.assets_dir / "music" / "mystery_bg.mp3"))
            if music.duration < final_video.duration:
                music = afx.audio_loop(music, duration=final_video.duration)
            else:
                music = music.subclip(0, final_video.duration)
            music = music.volumex(0.3)
            final_video = final_video.set_audio(music)
        except Exception as e:
            print(f"Warning: Could not add music: {e}")
        
        # Export
        if not output_filename:
            output_filename = "riddle_video.mp4"
        
        output_path = self.output_dir / output_filename
        final_video.write_videofile(
            str(output_path),
            fps=30,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True
        )
        
        print(f"Video generated: {output_path}")
        return output_path

# Example riddle data (matches the analyzed video)
EXAMPLE_RIDDLE = {
    "id": "001",
    "hook": {
        "text": "Detectives say if you can solve this,",
        "continuation": "you're either a genius or a psychopath.",
        "duration": 4
    },
    "setup": {
        "text": "A man was found dead in his living room early morning while drinking coffee.",
        "character": "victim",
        "duration": 5
    },
    "suspects": [
        {"name": "wife", "alibi": "she was outside getting vegetables from their garden.", "character": "wife", "duration": 3},
        {"name": "brother", "alibi": "he was for a walk with his dog.", "character": "brother", "duration": 3},
        {"name": "son", "alibi": "he was shower in his room.", "character": "son", "duration": 3},
        {"name": "maid", "alibi": "she was getting clothes from outside since it started raining.", "character": "maid", "duration": 4},
        {"name": "cook", "alibi": "he was preparing eggs for breakfast for everyone.", "character": "cook", "duration": 3}
    ],
    "challenge": {
        "text": "Did you figure out who it was?",
        "duration": 3
    },
    "cta": {
        "text": "Comment your answer below share with your psychopath friends.",
        "duration": 4
    }
}

if __name__ == "__main__":
    generator = RiddleVideoGenerator()
    generator.generate_video(EXAMPLE_RIDDLE, "first_riddle.mp4")

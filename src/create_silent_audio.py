"""
Create silent audio placeholder.
FREE - Uses only Python, no downloads needed.
Replace with real mystery music later.
"""
from moviepy.editor import AudioClip
from pathlib import Path

Path("assets/music").mkdir(parents=True, exist_ok=True)
silent = AudioClip(lambda t: 0, duration=60)
silent.write_audiofile("assets/music/mystery_bg.mp3", fps=44100, verbose=False, logger=None)
print("Silent placeholder created: assets/music/mystery_bg.mp3")
print("Replace with real mystery music later for production.")

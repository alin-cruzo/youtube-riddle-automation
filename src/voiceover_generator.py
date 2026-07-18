"""
Voiceover Generator — edge-tts (free, no API key, human-like neural voices)

Produces a "deep and mysterious" narration by:
  - using a deep male neural voice (en-US-GuyNeural / en-GB-RyanNeural)
  - slowing the rate slightly and lowering pitch for a graver tone
  - capturing real WordBoundary timestamps as it generates, so captions
    can be synced to actual speech timing instead of an estimated duration
"""

import asyncio
from pathlib import Path

try:
    import edge_tts
    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False

# Deep, mysterious narrator preset
VOICE = "en-US-GuyNeural"
RATE = "-8%"     # slightly slower = more deliberate / ominous
PITCH = "-6Hz"   # lower pitch = deeper voice


class VoiceoverGenerator:
    def __init__(self, output_dir="output/audio"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def _generate_with_timing(self, text, output_path, voice, rate, pitch):
        communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
        word_boundaries = []
        with open(output_path, "wb") as f:
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    f.write(chunk["data"])
                elif chunk["type"] == "WordBoundary":
                    word_boundaries.append({
                        "text": chunk["text"],
                        "offset_sec": chunk["offset"] / 10_000_000,  # 100ns units -> sec
                        "duration_sec": chunk["duration"] / 10_000_000,
                    })
        return word_boundaries

    def generate(self, text, filename="voiceover.mp3", voice=VOICE, rate=RATE, pitch=PITCH):
        """
        Returns (audio_path, word_timings) where word_timings is a list of
        {"text": str, "offset_sec": float, "duration_sec": float}, or an
        empty list if edge-tts isn't available / the call failed.
        """
        output_path = self.output_dir / filename
        if not EDGE_TTS_AVAILABLE:
            print("  [voiceover_generator] edge-tts not installed, skipping voiceover")
            return None, []

        try:
            word_timings = asyncio.run(
                self._generate_with_timing(text, str(output_path), voice, rate, pitch)
            )
            return output_path, word_timings
        except Exception as e:
            print(f"  [voiceover_generator] generation failed: {e}")
            return None, []

    def build_riddle_script(self, riddle_data, hook_line):
        """Builds the full narration text from riddle data, in speaking order."""
        parts = [hook_line]
        parts.append(f"Someone was found dead in {riddle_data['setting']}, victim of {riddle_data['cause']}.")
        for suspect in riddle_data["suspects"]:
            alibi = suspect["alibi"].rstrip(".")
            parts.append(f"The {suspect['name']} said {alibi}.")
        parts.append("Only one of them is lying. Can you catch who did it?")
        return " ".join(parts)

    def generate_riddle_voiceover(self, riddle_data, hook_line, filename="riddle_voice.mp3"):
        script = self.build_riddle_script(riddle_data, hook_line)
        audio_path, word_timings = self.generate(script, filename)
        return script, audio_path, word_timings


if __name__ == "__main__":
    vg = VoiceoverGenerator()
    test_riddle = {
        "setting": "a countryside manor",
        "cause": "poisoned tea",
        "suspects": [
            {"name": "maid", "alibi": "she was gathering laundry from outside since it started raining."},
            {"name": "cook", "alibi": "he was preparing dinner in the kitchen."},
        ],
    }
    script, path, timings = vg.generate_riddle_voiceover(
        test_riddle, "Detectives say if you can solve this, you are either a genius or a psychopath."
    )
    print("Script:", script)
    print("Audio path:", path)
    print("Word timings captured:", len(timings))
    if timings[:5]:
        for t in timings[:5]:
            print("  ", t)

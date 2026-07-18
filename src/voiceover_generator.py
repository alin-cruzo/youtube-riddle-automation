"""
Voiceover Generator — edge-tts (free, no API key, human-like neural voices)

Captures whichever timing granularity the voice actually provides:
  - WordBoundary (best) if the voice supports it
  - SentenceBoundary (fallback) otherwise — this is what en-GB-RyanNeural
    and several other voices emit instead
"""

import asyncio
from pathlib import Path

try:
    import edge_tts
    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False

VOICE = "en-GB-RyanNeural"
RATE = "-12%"
PITCH = "-15Hz"


class VoiceoverGenerator:
    def __init__(self, output_dir="output/audio"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def _generate_with_timing(self, text, output_path, voice, rate, pitch):
        communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
        word_boundaries = []
        sentence_boundaries = []
        chunk_types_seen = set()
        with open(output_path, "wb") as f:
            async for chunk in communicate.stream():
                chunk_types_seen.add(chunk["type"])
                if chunk["type"] == "audio":
                    f.write(chunk["data"])
                elif chunk["type"] == "WordBoundary":
                    word_boundaries.append({
                        "text": chunk["text"],
                        "offset_sec": chunk["offset"] / 10_000_000,
                        "duration_sec": chunk["duration"] / 10_000_000,
                    })
                elif chunk["type"] == "SentenceBoundary":
                    sentence_boundaries.append({
                        "text": chunk["text"],
                        "offset_sec": chunk["offset"] / 10_000_000,
                        "duration_sec": chunk["duration"] / 10_000_000,
                    })
        print(f"  [voiceover_generator] chunk types seen: {chunk_types_seen}")
        return word_boundaries, sentence_boundaries

    def generate(self, text, filename="voiceover.mp3", voice=VOICE, rate=RATE, pitch=PITCH):
        """
        Returns (audio_path, word_timings, sentence_timings).
        word_timings is [] if the voice doesn't emit WordBoundary events;
        sentence_timings is [] only if neither type came through at all.
        """
        output_path = self.output_dir / filename
        if not EDGE_TTS_AVAILABLE:
            print("  [voiceover_generator] edge-tts not installed, skipping voiceover")
            return None, [], []

        try:
            word_timings, sentence_timings = asyncio.run(
                self._generate_with_timing(text, str(output_path), voice, rate, pitch)
            )
            if not word_timings and sentence_timings:
                print("  [voiceover_generator] no WordBoundary events — "
                      f"using {len(sentence_timings)} SentenceBoundary timings for sync instead")
            elif not word_timings and not sentence_timings:
                print("  [voiceover_generator] WARNING: no timing events of any kind — captions will use full estimated timing")
            return output_path, word_timings, sentence_timings
        except Exception as e:
            print(f"  [voiceover_generator] generation failed: {e}")
            return None, [], []

    def build_riddle_script(self, riddle_data, hook_line):
        parts = [hook_line]
        parts.append(f"Someone was found dead in {riddle_data['setting']}, victim of {riddle_data['cause']}.")
        for suspect in riddle_data["suspects"]:
            alibi = suspect["alibi"].rstrip(".")
            parts.append(f"The {suspect['name']} said {alibi}.")
        parts.append("Only one of them is lying. Can you catch who did it?")
        return " ".join(parts)

    def generate_riddle_voiceover(self, riddle_data, hook_line, filename="riddle_voice.mp3"):
        script = self.build_riddle_script(riddle_data, hook_line)
        audio_path, word_timings, sentence_timings = self.generate(script, filename)
        return script, audio_path, word_timings, sentence_timings


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
    script, path, word_timings, sentence_timings = vg.generate_riddle_voiceover(
        test_riddle, "Detectives say if you can solve this, you are either a genius or a psychopath."
    )
    print("Script:", script)
    print("Audio path:", path)
    print("Word timings:", len(word_timings), " Sentence timings:", len(sentence_timings))
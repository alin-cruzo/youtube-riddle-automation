"""
Cinematic Video Generator
AI images (Ken Burns zoom) + karaoke/sentence captions + deep mysterious voiceover,
mixed with low-volume background music.
"""

import os
from pathlib import Path

import numpy as np
from PIL import Image

from caption_engine import CaptionEngine

try:
    from moviepy.editor import (
        ImageClip, AudioFileClip, CompositeAudioClip, CompositeVideoClip,
        concatenate_videoclips, concatenate_audioclips,
    )
    MOVIEPY_AVAILABLE = True
except ImportError:
    MOVIEPY_AVAILABLE = False


class CinematicVideoGenerator:
    def __init__(self, width=1080, height=1920, fps=30, assets_dir="assets"):
        self.width = width
        self.height = height
        self.fps = fps
        self.assets_dir = Path(assets_dir)
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)
        self.captions = CaptionEngine(
            width=width, height=height,
            font_path=self.assets_dir / "fonts" / "bold_font.ttf",
        )

    # ---------- word/scene timing ----------

    def _estimate_word_durations(self, words, total_duration):
        """Length-weighted split of a duration across a list of words."""
        weights = [max(len(w), 2) for w in words]
        total_w = sum(weights)
        return [total_duration * (w / total_w) for w in weights]

    def _schedule_from_sentence_timings(self, words, sentences, sentence_timings):
        """
        Distributes word-level start/duration within each sentence's real
        offset/duration window, proportional to word length. Falls back to
        None if the sentence count doesn't line up with the timing count —
        caller should treat None as "use full estimate instead".
        """
        if len(sentences) != len(sentence_timings):
            print(f"  [video_generator] WARNING: sentence split ({len(sentences)}) "
                  f"doesn't match sentence_timings ({len(sentence_timings)}), "
                  f"falling back to full estimate")
            return None

        schedule = []
        word_cursor = 0
        for sent_words, timing in zip(sentences, sentence_timings):
            sent_start = timing["offset_sec"]
            sent_duration = max(timing["duration_sec"], 0.1)
            durations = self._estimate_word_durations(sent_words, sent_duration)
            cursor = sent_start
            for i, d in enumerate(durations):
                schedule.append((word_cursor, cursor, d))
                cursor += d
                word_cursor += 1
        return schedule

    def build_word_schedule(self, script, word_timings=None, sentence_timings=None,
                             fallback_total_duration=45.0):
        """
        Returns (schedule, total_duration). schedule is a list of
        (word_idx, start_sec, duration_sec) covering the whole script.

        Tries, in order:
          1. real per-word WordBoundary timings (best case)
          2. per-sentence SentenceBoundary timings, words distributed
             proportionally within each sentence's real window
          3. fully estimated duration split (last resort)
        """
        words = script.split()

        # Tier 1: real word-level timings
        if word_timings and len(word_timings) >= len(words) * 0.8:
            schedule = []
            for i, t in enumerate(word_timings[: len(words)]):
                schedule.append((i, t["offset_sec"], max(t["duration_sec"], 0.12)))
            total = word_timings[-1]["offset_sec"] + word_timings[-1]["duration_sec"]
            return schedule, total

        # Tier 2: sentence-level timings
        if sentence_timings:
            sentences = self._split_into_sentence_word_groups(script)
            schedule = self._schedule_from_sentence_timings(words, sentences, sentence_timings)
            if schedule is not None:
                total = sentence_timings[-1]["offset_sec"] + sentence_timings[-1]["duration_sec"]
                return schedule, total

        # Tier 3: fully estimated
        durations = self._estimate_word_durations(words, fallback_total_duration)
        schedule, cursor = [], 0.0
        for i, d in enumerate(durations):
            schedule.append((i, cursor, d))
            cursor += d
        return schedule, cursor

    def _split_into_sentence_word_groups(self, script):
        """Splits script into sentences on . ? ! and returns each sentence's
        words as a list, e.g. [["Someone", "was", ...], ["Only", "one", ...]]."""
        import re
        raw_sentences = re.split(r'(?<=[.?!])\s+', script.strip())
        return [s.split() for s in raw_sentences if s.strip()]

    def map_words_to_scenes(self, scene_image_map):
        scenes, cursor = [], 0
        for image_path, count in scene_image_map:
            scenes.append((image_path, cursor, cursor + count))
            cursor += count
        return scenes

    # ---------- image / motion ----------

    def _ken_burns_clip(self, image_path, duration, zoom_start=1.0, zoom_end=1.12):
        clip = ImageClip(str(image_path)).set_duration(duration)
        if clip.h < self.height:
            clip = clip.resize(height=self.height)

        def zoom(get_frame, t):
            frame = get_frame(t)
            progress = (t / duration) if duration > 0 else 0
            zoom_level = zoom_start + (zoom_end - zoom_start) * progress
            pil_img = Image.fromarray(frame)
            w, h = pil_img.size
            new_w, new_h = int(w * zoom_level), int(h * zoom_level)
            pil_img = pil_img.resize((new_w, new_h), Image.LANCZOS)
            left = max(0, (new_w - self.width) // 2)
            top = max(0, (new_h - self.height) // 2)
            cropped = pil_img.crop((left, top, left + self.width, top + self.height))
            return np.array(cropped)

        return clip.fl(zoom)

    def _caption_clip_for_scene(self, script, scene_words):
        """Builds one concatenated caption track covering a scene's word slice.

        IMPORTANT: this expects self.captions.render_frame() to return an
        RGBA image with real per-pixel alpha (transparent everywhere except
        the drawn text). If render_frame internally converts to RGB or
        pastes without a mask, overlay.convert("RGBA") below will silently
        manufacture a fully-opaque alpha channel (all 255) and you'll be
        back to a black box over your background — just without a crash.
        See caption_engine.py's render_frame if that happens.
        """
        sub_clips = []
        for word_idx, _start, duration in scene_words:
            overlay = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
            overlay = self.captions.render_frame(overlay, script, word_idx)

            if overlay.mode != "RGBA":
                print(f"  [video_generator] WARNING: render_frame returned mode "
                      f"'{overlay.mode}', expected 'RGBA' — captions may render "
                      f"as an opaque block. Check caption_engine.py.")
                overlay = overlay.convert("RGBA")

            arr = np.array(overlay)
            rgb = arr[:, :, :3]
            alpha = arr[:, :, 3] / 255.0

            img_clip = ImageClip(rgb).set_duration(duration)
            mask_clip = ImageClip(alpha, ismask=True).set_duration(duration)
            img_clip = img_clip.set_mask(mask_clip)

            sub_clips.append(img_clip)
        return concatenate_videoclips(sub_clips, method="compose")

    # ---------- main build ----------

    def generate_video(self, script, scene_image_map, word_schedule,
                        filename="output.mp4", voiceover_path=None, music_path=None):
        if not MOVIEPY_AVAILABLE:
            raise ImportError("moviepy is required: pip install moviepy==1.0.3")

        scenes = self.map_words_to_scenes(scene_image_map)

        clips = []
        for image_path, start_idx, end_idx in scenes:
            scene_words = word_schedule[start_idx:end_idx]
            if not scene_words:
                continue
            scene_start = scene_words[0][1]
            scene_end = scene_words[-1][1] + scene_words[-1][2]
            scene_duration = max(scene_end - scene_start, 0.3)

            bg_clip = self._ken_burns_clip(image_path, scene_duration).set_duration(scene_duration)
            caption_track = self._caption_clip_for_scene(script, scene_words).set_duration(scene_duration)

            clips.append(CompositeVideoClip([bg_clip, caption_track], size=(self.width, self.height)))

        final_video = concatenate_videoclips(clips, method="compose")

        audio_layers = []
        if voiceover_path and os.path.exists(str(voiceover_path)):
            audio_layers.append(AudioFileClip(str(voiceover_path)).volumex(0.95))

        music_path = music_path or (self.assets_dir / "music" / "mystery_bg.mp3")
        if music_path and os.path.exists(str(music_path)) and os.path.getsize(str(music_path)) > 10_000:
            music = AudioFileClip(str(music_path))
            if music.duration < final_video.duration:
                loops = int(final_video.duration / music.duration) + 1
                music = concatenate_audioclips([music] * loops)
            music = music.subclip(0, final_video.duration).volumex(0.10)
            audio_layers.append(music)
        elif music_path and os.path.exists(str(music_path)):
            print(f"  [video_generator] music file too small ({os.path.getsize(str(music_path))} bytes), skipping background music")

        if audio_layers:
            final_video = final_video.set_audio(CompositeAudioClip(audio_layers))

        output_path = self.output_dir / filename
        final_video.write_videofile(
            str(output_path), fps=self.fps, codec="libx264",
            audio_codec="aac", temp_audiofile="temp-audio.m4a",
            remove_temp=True, verbose=False, logger=None,
        )
        return output_path
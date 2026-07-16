"""
Main Orchestrator — AI images + Ken Burns motion + deep mysterious voiceover
+ karaoke captions + YouTube upload.
"""

import sys
from pathlib import Path
from datetime import datetime

base = Path(__file__).parent.parent
sys.path.insert(0, str(base / "src"))
sys.path.insert(0, str(base / "riddles"))

from image_generator import ImageGenerator
from voiceover_generator import VoiceoverGenerator
from video_generator import CinematicVideoGenerator
from thumbnail_generator import ThumbnailGenerator
from metadata_generator import MetadataGenerator
from riddle_generator import generate_riddle


def main():
    print("=" * 60)
    print("YouTube Riddle Shorts — Cinematic Pipeline")
    print("=" * 60)
    print(f"Started: {datetime.now()}")

    print("\n[1/6] Generating a fresh, non-repeating riddle...")
    riddle = generate_riddle()
    print(f"  Riddle: {riddle['title']} (answer: {riddle['answer']})")

    print("\n[2/6] Generating AI scene images...")
    img_gen = ImageGenerator()
    image_paths = img_gen.generate_riddle_images(riddle["data"], riddle["id"])
    print(f"  Generated {len(image_paths)} images")

    print("\n[3/6] Generating deep, mysterious voiceover...")
    voice_gen = VoiceoverGenerator()
    script, voiceover_path, word_timings = voice_gen.generate_riddle_voiceover(
        riddle["data"], riddle["hook"], filename=f"voice_{riddle['id']}.mp3"
    )
    print(f"  Script length: {len(script.split())} words, timings captured: {len(word_timings)}")

    print("\n[4/6] Building cinematic video with synced captions...")
    video_gen = CinematicVideoGenerator()

    # scene_image_map must mirror the exact word order build_riddle_script() used:
    # hook -> victim/cause line -> each suspect's alibi -> closing line
    hook_words = len(riddle["hook"].split())
    victim_line = f"Someone was found dead in {riddle['data']['setting']}, victim of {riddle['data']['cause']}."
    victim_words = len(victim_line.split())

    scene_image_map = [(image_paths["hook"], hook_words), (image_paths["victim"], victim_words)]
    for i, suspect in enumerate(riddle["data"]["suspects"]):
        alibi_line = f"The {suspect['name']} said {suspect['alibi'].rstrip('.')}."
        scene_image_map.append((image_paths[f"suspect_{i}"], len(alibi_line.split())))

    closing_words = len("Only one of them is lying. Can you catch who did it?".split())
    scene_image_map.append((image_paths["conclusion"], closing_words))

    total_script_words = len(script.split())
    mapped_words = sum(c for _, c in scene_image_map)
    if mapped_words != total_script_words:
        # safety net: if word counts drift, pad/trim the last scene so the
        # video always covers the full script instead of crashing
        diff = total_script_words - mapped_words
        last_img, last_count = scene_image_map[-1]
        scene_image_map[-1] = (last_img, max(last_count + diff, 1))

    word_schedule, total_duration = video_gen.build_word_schedule(
        script, word_timings, fallback_total_duration=max(total_script_words * 0.38, 8)
    )

    video_filename = f"short_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
    video_path = video_gen.generate_video(
        script, scene_image_map, word_schedule,
        filename=video_filename, voiceover_path=voiceover_path,
    )
    print(f"  Video generated: {video_path}")

    print("\n[5/6] Generating thumbnail...")
    thumb_gen = ThumbnailGenerator()
    thumbnail_path = str(Path(video_path).with_suffix(".png"))
    thumb_gen.create_thumbnail(riddle, thumbnail_path)
    print(f"  Thumbnail: {thumbnail_path}")

    print("\n[6/6] Generating metadata...")
    meta_gen = MetadataGenerator()
    metadata = meta_gen.generate_all(riddle)
    print(f"  Title: {metadata['title']}")
    print(f"  Hashtags: {metadata['hashtags']}")

    print("\n[UPLOAD] Uploading to YouTube...")
    try:
        from youtube_uploader import YouTubeUploader
        uploader = YouTubeUploader()
        video_id = uploader.upload_short(
            video_path=str(video_path),
            title=metadata["title"],
            description=metadata["description"],
            tags=metadata["tags"],
            thumbnail_path=thumbnail_path,
        )
        print(f"  Uploaded! https://youtube.com/shorts/{video_id}")
    except Exception as e:
        print(f"  Upload failed: {e}")
        print("  Video saved locally but not uploaded.")

    print("\n" + "=" * 60)
    print("Pipeline complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()

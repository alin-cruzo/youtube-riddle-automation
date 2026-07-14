"""Main Orchestrator"""

import sys
from pathlib import Path
from datetime import datetime

base = Path(__file__).parent.parent
sys.path.insert(0, str(base / "src"))
sys.path.insert(0, str(base / "riddles"))

from simple_video import SimpleVideoGenerator
from thumbnail_generator import ThumbnailGenerator
from metadata_generator import MetadataGenerator
from riddle_database import RIDDLE_DATABASE

def main():
    print("Starting pipeline at " + str(datetime.now()))
    
    video_gen = SimpleVideoGenerator()
    thumb_gen = ThumbnailGenerator()
    meta_gen = MetadataGenerator()
    
    hour = datetime.now().hour
    day_of_year = datetime.now().timetuple().tm_yday
    
    riddle_index = (day_of_year * 24 + hour) % len(RIDDLE_DATABASE)
    riddle = RIDDLE_DATABASE[riddle_index]
    
    print("Selected riddle: " + riddle["title"] + " (ID: " + riddle["id"] + ")")

    # Generate video
    video_filename = "short_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".mp4"
    video_path = video_gen.generate_video(riddle["data"], video_filename)
    print("Video generated: " + str(video_path))
    
    # Generate thumbnail
    thumbnail_path = str(Path(video_path).with_suffix(".png"))
    thumb_gen.create_thumbnail(riddle, thumbnail_path)
    print("Thumbnail generated: " + thumbnail_path)
    
    # Generate metadata
    metadata = meta_gen.generate_all(riddle)
    print("Title: " + metadata["title"])
    print("Hashtags: " + str(metadata["hashtags"]))
    
    # Upload to YouTube
    try:
        from youtube_uploader import YouTubeUploader
        uploader = YouTubeUploader()
        video_id = uploader.upload_short(
            video_path=str(video_path),
            title=metadata["title"],
            description=metadata["description"],
            tags=metadata["tags"],
            thumbnail_path=thumbnail_path
        )
        print("YouTube upload successful! Video ID: " + video_id)
    except Exception as e:
        print("YouTube upload failed: " + str(e))
        print("Video saved locally but not uploaded.")
    
    print("Pipeline complete!")

if __name__ == "__main__":
    main()

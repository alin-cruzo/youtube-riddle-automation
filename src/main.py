"""Main Orchestrator"""

import sys
from pathlib import Path
from datetime import datetime

# Add both src and riddles to path
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
    
    # Select riddle based on hour of day
    hour = datetime.now().hour
    day_of_year = datetime.now().timetuple().tm_yday
    
    # Calculate riddle index (cycles through database)
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
    
    print("Pipeline complete!")

if __name__ == "__main__":
    main()

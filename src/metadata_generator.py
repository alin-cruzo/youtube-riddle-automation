"""Metadata Generator"""

import random

class MetadataGenerator:
    TITLE_TEMPLATES = [
        "Can You Solve This? ",
        "Only 1% Can Solve This Mystery! ",
        "Genius or Psychopath? You Decide! ",
        "This Riddle Broke The Internet! ",
        "Solve This in 10 Seconds! ",
        "Detectives Are Stumped! Can You Help? ",
        "The Answer Will Shock You! ",
        "IQ Test: Can You Spot The Killer? ",
        "This Riddle is IMPOSSIBLE! ",
        "Comment Your Answer! "
    ]
    
    HASHTAG_POOL = [
        "#Riddle", "#Mystery", "#BrainTeaser",
        "#Detective", "#WhoDidIt", "#CrimeRiddle",
        "#LogicPuzzle", "#MindGames", "#PsychopathTest",
        "#GeniusTest", "#IQTest", "#BrainGames",
        "#Shorts", "#YouTubeShorts", "#Viral"
    ]
    
    def generate_title(self, riddle_title):
        template = random.choice(self.TITLE_TEMPLATES)
        return template + riddle_title
    
    def generate_hashtags(self, count=3):
        return random.sample(self.HASHTAG_POOL, count)
    
    def generate_description(self, riddle_title, hashtags):
        desc = "Can YOU solve this mystery?\n\n"
        desc += riddle_title + "\n\n"
        desc += "Drop your answer in the comments!\n"
        desc += "Tag a friend who needs to see this!\n\n"
        desc += " ".join(hashtags) + "\n"
        desc += "#Shorts #YouTubeShorts #Riddle"
        return desc
    
    def generate_all(self, riddle_data):
        title = self.generate_title(riddle_data["title"])
        hashtags = self.generate_hashtags()
        description = self.generate_description(riddle_data["title"], hashtags)
        tags = ["riddle", "mystery", "brain teaser", "detective", "shorts"]
        
        return {
            "title": title,
            "description": description,
            "hashtags": hashtags,
            "tags": tags
        }

if __name__ == "__main__":
    gen = MetadataGenerator()
    
    test_riddle = {
        "title": "The Coffee Murder",
        "answer": "The Maid"
    }
    
    meta = gen.generate_all(test_riddle)
    print("Title: " + meta["title"])
    print("Hashtags: " + str(meta["hashtags"]))
    print("Description:")
    print(meta["description"])

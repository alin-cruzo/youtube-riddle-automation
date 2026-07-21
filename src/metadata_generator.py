"""
Metadata Generator

Titles, hooks, and descriptions are now built from the actual riddle
specifics (cause of death, setting, suspect count) instead of a fixed
generic template pool. A generic "Can You Solve This?" title looks
identical across every video in Studio and gives viewers no reason to
pick this one over the last one — pulling in the real twist detail
gives each thumbnail/title pair something specific to promise.
"""

import random

class MetadataGenerator:
    # {cause} and {setting} get filled in from riddle_data at generation time.
    # Keep these under ~90 chars after filling so the full title always
    # displays without truncation in search/suggested results.
    TITLE_TEMPLATES = [
        "Murder By {cause} — Can You Catch The Liar?",
        "{suspect_count} Suspects, Only 1 Lie — Solve The {cause} Case!",
        "Killed By {cause} at {setting} — Who Did It?",
        "This {cause} Case Stumped Detectives! Can You Solve It?",
        "Only 1% Can Solve This {cause} Mystery!",
        "The {setting} Killer Left One Clue — Can You Spot It?",
        "IQ Test: Who Lied About The {cause}?",
        "Genius or Psychopath? Solve The {setting} Murder!",
    ]

    HASHTAG_POOL = [
        "#Riddle", "#Mystery", "#BrainTeaser",
        "#Detective", "#WhoDidIt", "#CrimeRiddle",
        "#LogicPuzzle", "#MindGames", "#PsychopathTest",
        "#GeniusTest", "#IQTest", "#BrainGames",
        "#Shorts", "#YouTubeShorts", "#Viral"
    ]

    def _short_cause(self, cause):
        """'poisoned tea' -> 'Poisoned Tea', 'a locked-room stabbing' -> 'Locked-Room Stabbing'"""
        words = cause.replace("a ", "", 1) if cause.startswith("a ") else cause
        return words.title()

    def _short_setting(self, setting):
        """'a countryside manor' -> 'The Countryside Manor'"""
        words = setting.replace("a ", "", 1).replace("an ", "", 1) if setting.startswith(("a ", "an ")) else setting
        return words.title()

    def generate_title(self, riddle_data):
        cause = self._short_cause(riddle_data["cause"])
        setting = self._short_setting(riddle_data["setting"])
        suspect_count = len(riddle_data["suspects"])

        template = random.choice(self.TITLE_TEMPLATES)
        return template.format(cause=cause, setting=setting, suspect_count=suspect_count)

    def generate_hashtags(self, count=3):
        return random.sample(self.HASHTAG_POOL, count)

    def generate_description(self, riddle_data, hashtags):
        cause = self._short_cause(riddle_data["cause"])
        setting = self._short_setting(riddle_data["setting"])
        suspect_count = len(riddle_data["suspects"])

        desc = f"{suspect_count} suspects. {setting}. Death by {cause.lower()}.\n\n"
        desc += "Only one of them is lying — can YOU catch it before the reveal?\n\n"
        desc += "Drop your answer in the comments before you scroll to the end!\n"
        desc += "Tag a friend who thinks they're a detective!\n\n"
        desc += " ".join(hashtags) + "\n"
        desc += "#Shorts #YouTubeShorts #Riddle"
        return desc

    def generate_all(self, riddle):
        riddle_data = riddle["data"]
        title = self.generate_title(riddle_data)
        hashtags = self.generate_hashtags()
        description = self.generate_description(riddle_data, hashtags)
        tags = ["riddle", "mystery", "brain teaser", "detective", "shorts",
                riddle_data["cause"].split()[-1], riddle_data["setting"].split()[-1]]

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
        "answer": "The Maid",
        "data": {
            "cause": "poisoned tea",
            "setting": "a countryside manor",
            "suspects": [{"name": "maid"}, {"name": "wife"}, {"name": "cook"}, {"name": "gardener"}],
        }
    }

    meta = gen.generate_all(test_riddle)
    print("Title: " + meta["title"])
    print("Hashtags: " + str(meta["hashtags"]))
    print("Tags: " + str(meta["tags"]))
    print("Description:")
    print(meta["description"])
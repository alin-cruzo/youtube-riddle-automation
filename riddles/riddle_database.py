"""Riddle Database"""

RIDDLE_DATABASE = [
    {
        "id": "001",
        "title": "The Coffee Murder",
        "answer": "The Maid",
        "data": {
            "suspects": [
                {"name": "wife", "alibi": "she was outside getting vegetables.", "character": "wife", "duration": 3},
                {"name": "brother", "alibi": "he was walking his dog in the rain.", "character": "brother", "duration": 3},
                {"name": "son", "alibi": "he was showering in his room.", "character": "son", "duration": 3},
                {"name": "maid", "alibi": "she was getting clothes from outside since it started raining.", "character": "maid", "duration": 4},
                {"name": "cook", "alibi": "he was preparing eggs for breakfast.", "character": "cook", "duration": 3}
            ]
        }
    },
    {
        "id": "002",
        "title": "The Snowy Footprints",
        "answer": "The Wife",
        "data": {
            "suspects": [
                {"name": "wife", "alibi": "she just got back from the store.", "character": "wife", "duration": 3},
                {"name": "gardener", "alibi": "he was trimming trees.", "character": "brother", "duration": 3},
                {"name": "neighbor", "alibi": "he saw everything from his window.", "character": "son", "duration": 3},
                {"name": "butler", "alibi": "he was inside preparing tea.", "character": "cook", "duration": 3}
            ]
        }
    },
    {
        "id": "003",
        "title": "The Lighthouse Murder",
        "answer": "The Brother",
        "data": {
            "suspects": [
                {"name": "wife", "alibi": "she was reading in the library.", "character": "wife", "duration": 3},
                {"name": "brother", "alibi": "he visited at 3 PM and left before the murder.", "character": "brother", "duration": 3},
                {"name": "keeper", "alibi": "he was maintaining the lighthouse lamp.", "character": "cook", "duration": 3},
                {"name": "sailor", "alibi": "he was docking his boat.", "character": "son", "duration": 3}
            ]
        }
    },
]

def get_riddle_by_id(riddle_id):
    for riddle in RIDDLE_DATABASE:
        if riddle["id"] == riddle_id:
            return riddle
    return None

if __name__ == "__main__":
    print("Riddle database loaded: " + str(len(RIDDLE_DATABASE)) + " riddles")
    for r in RIDDLE_DATABASE:
        print("  - " + r["id"] + ": " + r["title"] + " (Answer: " + r["answer"] + ")")

"""
Riddle Generator
Produces unique mystery riddles from a combinatorial template pool instead of
a fixed list, so an hourly pipeline doesn't repeat the same case.

Uniqueness strategy:
  - Victim, setting, weapon/cause, and 4-5 suspects are drawn from pools.
  - Each generated riddle gets a signature (sorted suspect roles + setting + cause).
  - A rolling history file (riddles/history.json) stores signatures of the last
    N riddles used. New riddles are re-rolled (up to a retry cap) if their
    signature collides with recent history.
  - The pool sizes below give tens of thousands of possible combinations, so
    collisions are rare and the retry loop resolves them almost immediately.

Hook generation:
  - Previously pulled from a fixed pool of generic lines ("Detectives say if
    you can solve this...") that said nothing about the actual case. Average
    view duration data showed viewers dropping off within ~6 seconds -- right
    around where the generic hook line was still playing before any real
    crime detail arrived. generate_hook() now builds the opening line from
    THIS riddle's actual setting/cause/suspect count, so the specific stakes
    are the very first thing said, not a warm-up sentence before them.
"""

import json
import random
from pathlib import Path

HISTORY_PATH = Path(__file__).parent / "history.json"
HISTORY_SIZE = 200          # how many past signatures to remember
MAX_RETRIES = 30            # attempts to find a non-repeating combo

SETTINGS = [
    "a countryside manor", "a beachside villa", "a mountain cabin",
    "a downtown penthouse", "a quiet suburban house", "a lighthouse keeper's cottage",
    "an old bookshop", "a vineyard estate", "a riverside cottage", "a ski lodge",
    "a rooftop apartment", "a train car", "an art gallery", "a hotel suite",
    "a farmhouse", "a houseboat", "a countryside inn", "a university office",
]

CAUSES = [
    "poisoned tea", "a locked-room stabbing", "a fall from the balcony",
    "a gas leak", "a mysterious fire", "an overdose", "a strangling",
    "a hit-and-run in the driveway", "a drowning in the pool",
    "an electrocution", "a shooting heard at midnight", "a knife in the kitchen",
]

VICTIM_ROLES = [
    "the homeowner", "the wealthy uncle", "the business partner", "the landlord",
    "the retired professor", "the family patriarch", "the chef", "the art collector",
]

# Each suspect role has a character sprite key (matches assets/characters) and
# a pool of alibi phrasings to keep suspects varied even when the role repeats.
SUSPECT_POOL = [
    {"role": "wife", "character": "wife", "alibis": [
        "she was outside getting groceries",
        "she was on a phone call in the garden",
        "she was upstairs packing for a trip",
        "she was at the neighbor's house borrowing sugar",
    ]},
    {"role": "brother", "character": "brother", "alibis": [
        "he was walking the dog in the rain",
        "he was fixing his car in the garage",
        "he was at the gym across town",
        "he was asleep after a night shift",
    ]},
    {"role": "son", "character": "son", "alibis": [
        "he was showering in his room",
        "he was gaming with friends online",
        "he was studying for an exam upstairs",
        "he was out on a late-night jog",
    ]},
    {"role": "maid", "character": "maid", "alibis": [
        "she was gathering laundry from outside since it started raining",
        "she was cleaning the west wing on the second floor",
        "she was ironing clothes in the utility room",
        "she was polishing silverware in the pantry",
    ]},
    {"role": "cook", "character": "cook", "alibis": [
        "he was preparing dinner in the kitchen",
        "he was tasting a sauce on the stove",
        "he was unloading groceries from the car",
        "he was cleaning knives in the sink",
    ]},
    {"role": "gardener", "character": "brother", "alibis": [
        "he was trimming the hedges by the gate",
        "he was watering plants in the greenhouse",
        "he was repairing the fence out back",
    ]},
    {"role": "neighbor", "character": "son", "alibis": [
        "he was watching from his window the whole time",
        "he was walking past around that hour",
        "he was hosting a small dinner next door",
    ]},
    {"role": "business partner", "character": "cook", "alibis": [
        "he was reviewing contracts in the study",
        "he was on a video call with an investor",
        "he was pacing the hallway, upset about a deal",
    ]},
    {"role": "assistant", "character": "maid", "alibis": [
        "she was filing paperwork in the office",
        "she was answering emails downstairs",
        "she was organizing the bookshelf",
    ]},
    {"role": "old friend", "character": "wife", "alibis": [
        "she had just arrived and was unpacking",
        "she was chatting on the porch",
        "she was looking at old photographs in the den",
    ]},
]

# Templates below get filled with THIS riddle's actual setting/cause/suspect
# count -- no generic filler line before the real stakes arrive.
HOOK_TEMPLATES = [
    "Found dead at {setting}. Killed by {cause}. {num_suspects} suspects — only one is lying.",
    "{cause_cap} at {setting}. {num_suspects} suspects. One of them is lying.",
    "A body. {cause}. {num_suspects} suspects — can you catch the liar?",
    "{num_suspects} suspects. One killer. Death by {cause} at {setting}.",
]


def _strip_article(text):
    if text.startswith("an "):
        return text[3:]
    if text.startswith("a "):
        return text[2:]
    return text


def generate_hook(setting, cause, num_suspects):
    setting_short = _strip_article(setting)
    cause_short = _strip_article(cause)
    cause_cap = cause_short[0].upper() + cause_short[1:]

    template = random.choice(HOOK_TEMPLATES)
    return template.format(
        setting=setting_short,
        cause=cause_short,
        cause_cap=cause_cap,
        num_suspects=num_suspects,
    )


def _signature(setting, cause, suspects):
    roles = tuple(sorted(s["name"] for s in suspects))
    return f"{setting}|{cause}|{roles}"


def _load_history():
    if HISTORY_PATH.exists():
        try:
            return json.loads(HISTORY_PATH.read_text())
        except Exception:
            return []
    return []


def _save_history(history):
    HISTORY_PATH.write_text(json.dumps(history[-HISTORY_SIZE:]))


def generate_riddle(riddle_id=None):
    """Generate one riddle dict, avoiding recent repeats via history.json."""
    history = _load_history()

    for _ in range(MAX_RETRIES):
        setting = random.choice(SETTINGS)
        cause = random.choice(CAUSES)
        victim = random.choice(VICTIM_ROLES)
        num_suspects = random.randint(4, 5)
        chosen = random.sample(SUSPECT_POOL, num_suspects)

        suspects = []
        for s in chosen:
            suspects.append({
                "name": s["role"],
                "alibi": random.choice(s["alibis"]),
                "character": s["character"],
                "duration": random.choice([3, 3, 4]),
            })

        sig = _signature(setting, cause, suspects)
        if sig not in history:
            break
    else:
        # exhausted retries (extremely unlikely) — accept anyway
        pass

    guilty = random.choice(suspects)
    title = f"The {cause.split()[-1].title()} at {setting.split()[-1].title()}" \
        if len(cause.split()) else "The Mystery Case"

    riddle = {
        "id": riddle_id or f"gen_{random.randint(100000, 999999)}",
        "title": f"Murder at {setting.title()}",
        "hook": generate_hook(setting, cause, num_suspects),
        "victim": victim,
        "setting": setting,
        "cause": cause,
        "answer": guilty["name"].title(),
        "data": {
            "victim": victim,
            "setting": setting,
            "cause": cause,
            "suspects": suspects,
        },
    }

    history.append(sig)
    _save_history(history)
    return riddle


if __name__ == "__main__":
    seen_titles = set()
    for i in range(10):
        r = generate_riddle()
        print(f"{i+1}. HOOK: {r['hook']}")
        print(f"   {r['title']} — cause: {r['cause']} — answer: {r['answer']}")
        for s in r["data"]["suspects"]:
            print(f"     {s['name']}: {s['alibi']}")
        seen_titles.add(r["title"])
    print(f"\n{len(seen_titles)} unique titles out of 10 generated")

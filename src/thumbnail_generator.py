"""
Thumbnail Generator

Previously showed the same static detective.png + generic riddle title on
every single thumbnail. Now pulls the actual case-specific cause/setting
text and shows the real suspect character sprites for THIS riddle, so the
thumbnail promises something specific instead of looking identical across
every video in Studio (which gives a viewer no reason to pick this one).
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

MAX_SUSPECT_ICONS = 4
ICON_SIZE = 220
ICON_GAP = 30


class ThumbnailGenerator:
    def __init__(self, assets_dir="assets"):
        self.assets_dir = Path(assets_dir)
        self.width = 1080
        self.height = 1920

    def _short_cause(self, cause):
        text = cause[2:] if cause.startswith("a ") else cause
        return text.upper()

    def _short_setting(self, setting):
        text = setting
        if text.startswith("an "):
            text = text[3:]
        elif text.startswith("a "):
            text = text[2:]
        return ("AT " + text).upper()

    def create_thumbnail(self, riddle, output_path):
        riddle_data = riddle.get("data", {})
        cause = riddle_data.get("cause", "")
        setting = riddle_data.get("setting", "")
        suspects = riddle_data.get("suspects", [])

        # Dark gradient background (mystery theme)
        img = Image.new('RGB', (self.width, self.height))
        draw = ImageDraw.Draw(img)
        for y in range(self.height):
            r = int(20 + (y / self.height) * 40)
            g = int(20 + (y / self.height) * 30)
            b = int(40 + (y / self.height) * 60)
            draw.line([(0, y), (self.width, y)], fill=(r, g, b))

        # Load fonts
        font_path = self.assets_dir / "fonts" / "bold_font.ttf"
        try:
            if not font_path.exists():
                raise FileNotFoundError(f"font not found at {font_path}")
            font_large = ImageFont.truetype(str(font_path), 120)
            font_medium = ImageFont.truetype(str(font_path), 80)
            font_small = ImageFont.truetype(str(font_path), 56)
            font_tiny = ImageFont.truetype(str(font_path), 44)
        except Exception as e:
            print(f"  [thumbnail_generator] WARNING: could not load custom font ({e}), falling back to default font -- thumbnail text will look small/plain")
            font_large = font_medium = font_small = font_tiny = ImageFont.load_default()

        # Large question mark watermark
        qm = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
        qm_draw = ImageDraw.Draw(qm)
        qm_draw.text((self.width // 2, 340), "?", font=font_large, fill=(255, 255, 255, 30), anchor="mm")
        img = Image.alpha_composite(img.convert('RGBA'), qm).convert('RGB')
        draw = ImageDraw.Draw(img)

        # Main hook
        self._draw_text_with_glow(draw, "WHO DID IT?", (self.width // 2, 540), font_medium,
                                   text_color=(255, 50, 50), glow_color=(255, 0, 0))

        # Case-specific cause line (e.g. "POISONED TEA")
        if cause:
            self._draw_text_with_glow(draw, self._short_cause(cause), (self.width // 2, 700), font_small,
                                       text_color=(255, 255, 255), glow_color=(100, 100, 255))

        # Case-specific setting line (e.g. "AT A COUNTRYSIDE MANOR")
        if setting:
            self._draw_text_with_glow(draw, self._short_setting(setting), (self.width // 2, 820), font_tiny,
                                       text_color=(220, 220, 220), glow_color=(80, 80, 150))

        # Suspect count / urgency line
        if suspects:
            urgency_text = f"{len(suspects)} SUSPECTS. ONLY 1 LIES."
        else:
            urgency_text = "SOLVE IN 10s"
        self._draw_text_with_glow(draw, urgency_text, (self.width // 2, 1000), font_small,
                                   text_color=(255, 255, 0), glow_color=(255, 200, 0))

        # Suspect character row — the actual suspects from THIS riddle,
        # not a fixed detective.png every time.
        self._draw_suspect_row(img, suspects)

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        img.save(output_path)
        print("Thumbnail saved: " + output_path)
        return output_path

    def _draw_suspect_row(self, img, suspects):
        icons_to_show = suspects[:MAX_SUSPECT_ICONS] if suspects else []
        if not icons_to_show:
            self._paste_character(img, "detective", (self.width // 2 - ICON_SIZE // 2, 1400))
            return

        count = len(icons_to_show)
        total_width = count * ICON_SIZE + (count - 1) * ICON_GAP
        start_x = (self.width - total_width) // 2
        y = 1400

        for i, suspect in enumerate(icons_to_show):
            char_key = suspect.get("character", "detective")
            x = start_x + i * (ICON_SIZE + ICON_GAP)
            self._paste_character(img, char_key, (x, y))

    def _paste_character(self, img, char_key, position):
        char_path = self.assets_dir / "characters" / f"{char_key}.png"
        try:
            if not char_path.exists():
                raise FileNotFoundError(f"character image not found at {char_path}")
            char = Image.open(char_path).convert("RGBA")
            char = char.resize((ICON_SIZE, ICON_SIZE))
            img.paste(char, position, char)
        except Exception as e:
            print(f"  [thumbnail_generator] WARNING: could not add character '{char_key}' ({e}) -- thumbnail will have a blank area where it should appear")

    def _draw_text_with_glow(self, draw, text, position, font, text_color, glow_color, glow_radius=3):
        x, y = position
        for dx in range(-glow_radius, glow_radius + 1):
            for dy in range(-glow_radius, glow_radius + 1):
                if dx != 0 or dy != 0:
                    draw.text((x + dx, y + dy), text, font=font, fill=glow_color, anchor="mm")
        draw.text((x, y), text, font=font, fill=text_color, anchor="mm")


if __name__ == "__main__":
    gen = ThumbnailGenerator()
    test_riddle = {
        "title": "The Coffee Murder",
        "data": {
            "cause": "poisoned tea",
            "setting": "a countryside manor",
            "suspects": [
                {"name": "maid", "character": "maid"},
                {"name": "wife", "character": "wife"},
                {"name": "cook", "character": "cook"},
                {"name": "son", "character": "son"},
            ],
        },
    }
    gen.create_thumbnail(test_riddle, "output/thumbnail_test.png")
    print("Thumbnail test complete!")
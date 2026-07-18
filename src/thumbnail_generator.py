"""Thumbnail Generator"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

class ThumbnailGenerator:
    def __init__(self, assets_dir="assets"):
        self.assets_dir = Path(assets_dir)
        self.width = 1080
        self.height = 1920

    def create_thumbnail(self, riddle_data, output_path):
        # Dark gradient background (mystery theme)
        img = Image.new('RGB', (self.width, self.height))
        draw = ImageDraw.Draw(img)

        # Gradient from dark blue to dark purple
        for y in range(self.height):
            r = int(20 + (y / self.height) * 40)
            g = int(20 + (y / self.height) * 30)
            b = int(40 + (y / self.height) * 60)
            draw.line([(0, y), (self.width, y)], fill=(r, g, b))

        # Load font
        font_path = self.assets_dir / "fonts" / "bold_font.ttf"
        try:
            if not font_path.exists():
                raise FileNotFoundError(f"font not found at {font_path}")
            font_large = ImageFont.truetype(str(font_path), 120)
            font_medium = ImageFont.truetype(str(font_path), 80)
            font_small = ImageFont.truetype(str(font_path), 60)
        except Exception as e:
            print(f"  [thumbnail_generator] WARNING: could not load custom font ({e}), falling back to default font — thumbnail text will look small/plain")
            font_large = ImageFont.load_default()
            font_medium = ImageFont.load_default()
            font_small = ImageFont.load_default()

        # Large question mark (semi-transparent)
        qm = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
        qm_draw = ImageDraw.Draw(qm)
        qm_draw.text((self.width//2, 400), "?", font=font_large, fill=(255, 255, 255, 30), anchor="mm")
        img = Image.alpha_composite(img.convert('RGBA'), qm).convert('RGB')
        draw = ImageDraw.Draw(img)

        # Main text: "WHO DID IT?"
        self._draw_text_with_glow(draw, "WHO DID IT?", (self.width//2, 600), font_medium, text_color=(255, 50, 50), glow_color=(255, 0, 0))

        # Riddle title
        title = riddle_data.get("title", "Mystery Riddle")
        self._draw_text_with_glow(draw, title, (self.width//2, 900), font_small, text_color=(255, 255, 255), glow_color=(100, 100, 255))

        # Urgency text
        self._draw_text_with_glow(draw, "SOLVE IN 10s", (self.width//2, 1200), font_small, text_color=(255, 255, 0), glow_color=(255, 200, 0))

        # Add detective character if available
        char_path = self.assets_dir / "characters" / "detective.png"
        try:
            if not char_path.exists():
                raise FileNotFoundError(f"character image not found at {char_path}")
            char = Image.open(char_path).convert("RGBA")
            char = char.resize((400, 400))
            img.paste(char, (self.width//2 - 200, 1300), char)
        except Exception as e:
            print(f"  [thumbnail_generator] WARNING: could not add detective character ({e}) — thumbnail will have a blank area where it should appear")

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        img.save(output_path)
        print("Thumbnail saved: " + output_path)
        return output_path

    def _draw_text_with_glow(self, draw, text, position, font, text_color, glow_color, glow_radius=3):
        x, y = position
        for dx in range(-glow_radius, glow_radius+1):
            for dy in range(-glow_radius, glow_radius+1):
                if dx != 0 or dy != 0:
                    draw.text((x + dx, y + dy), text, font=font, fill=glow_color, anchor="mm")
        draw.text((x, y), text, font=font, fill=text_color, anchor="mm")

if __name__ == "__main__":
    gen = ThumbnailGenerator()
    gen.create_thumbnail({"title": "The Coffee Murder"}, "output/thumbnail_test.png")
    print("Thumbnail test complete!")
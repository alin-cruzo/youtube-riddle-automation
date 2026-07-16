"""
Caption Engine
Word-by-word karaoke-style captions: current word highlighted yellow,
rest in dark gray. No background box, no stroke — matches the style
you asked for. Text is wrapped ahead of time so it NEVER overflows
the 1080x1920 frame; captions display one wrapped line at a time and
advance to the next line automatically when the spoken word crosses
into it.
"""

from PIL import Image, ImageDraw, ImageFont

NORMAL_COLOR = (45, 45, 45, 255)
HIGHLIGHT_COLOR = (255, 196, 0, 255)
SAFE_WIDTH = 900          # max caption width in px (1080 frame, generous margin)
DEFAULT_FONT_SIZE = 64
MIN_FONT_SIZE = 34


class CaptionEngine:
    def __init__(self, width=1080, height=1920, font_path="assets/fonts/bold_font.ttf"):
        self.width = width
        self.height = height
        self.font_path = str(font_path)

    def _font(self, size):
        try:
            return ImageFont.truetype(self.font_path, size)
        except Exception:
            return ImageFont.load_default()

    def _word_width(self, font, word):
        bbox = font.getbbox(word)
        return (bbox[2] - bbox[0]) if bbox else len(word) * font.size * 0.6

    def _space_width(self, font):
        bbox = font.getbbox(" ")
        return (bbox[2] - bbox[0]) if bbox else int(font.size * 0.3)

    def build_lines(self, full_text, font_size=DEFAULT_FONT_SIZE, max_width=SAFE_WIDTH):
        """
        Wrap full_text into lines that each fit max_width at font_size.
        Returns (lines, word_to_line_index) where word_to_line_index maps
        each word's global index (in full_text.split()) to which line it's on.
        Auto-shrinks font_size if even a single word doesn't fit.
        """
        words = full_text.split()
        font = self._font(font_size)

        # shrink font until the single longest word fits, so wrapping is always possible
        while font_size > MIN_FONT_SIZE and words:
            longest = max(self._word_width(font, w) for w in words)
            if longest <= max_width:
                break
            font_size -= 2
            font = self._font(font_size)

        space_w = self._space_width(font)
        lines, current_line, current_width = [], [], 0
        word_to_line = []

        for word in words:
            w = self._word_width(font, word)
            extra = space_w if current_line else 0
            if current_width + w + extra <= max_width:
                current_line.append(word)
                current_width += w + extra
            else:
                lines.append(current_line)
                current_line = [word]
                current_width = w
            word_to_line.append(len(lines))  # index of the line this word will end up on

        if current_line:
            lines.append(current_line)

        return lines, word_to_line, font_size

    def render_frame(self, background_img, full_text, active_word_index,
                      y_fraction=0.16, font_size=DEFAULT_FONT_SIZE):
        """
        Draws the caption line containing active_word_index onto background_img
        (a PIL RGB/RGBA Image) and returns the composited image.
        """
        lines, word_to_line, resolved_size = self.build_lines(full_text, font_size)
        words = full_text.split()
        if not words:
            return background_img

        active_word_index = max(0, min(active_word_index, len(words) - 1))
        active_line_idx = word_to_line[active_word_index]
        line_words = lines[active_line_idx]

        # figure out which word within this line is the active one
        words_before_line = sum(len(l) for l in lines[:active_line_idx])
        active_in_line = active_word_index - words_before_line

        font = self._font(resolved_size)
        overlay = Image.new("RGBA", background_img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        space_w = self._space_width(font)
        widths = [self._word_width(font, w) for w in line_words]
        total_w = sum(widths) + space_w * (len(line_words) - 1)

        x = (self.width - total_w) // 2
        y = int(self.height * y_fraction)

        for i, word in enumerate(line_words):
            color = HIGHLIGHT_COLOR if i == active_in_line else NORMAL_COLOR
            draw.text((x, y), word, font=font, fill=color, anchor="lm")
            x += widths[i] + space_w

        base = background_img.convert("RGBA")
        composed = Image.alpha_composite(base, overlay)
        return composed.convert("RGB")


if __name__ == "__main__":
    from pathlib import Path
    Path("output").mkdir(exist_ok=True)

    engine = CaptionEngine()
    bg = Image.new("RGB", (1080, 1920), (245, 240, 230))

    test_text = "The maid said she was gathering laundry from outside since it started raining"
    words = test_text.split()
    lines, word_to_line, size = engine.build_lines(test_text)
    print(f"Wrapped into {len(lines)} lines at font size {size}:")
    for l in lines:
        print("  ", " ".join(l))

    # render a frame with the 3rd word highlighted
    frame = engine.render_frame(bg, test_text, active_word_index=3)
    frame.save("output/caption_test.png")
    print("Saved output/caption_test.png")

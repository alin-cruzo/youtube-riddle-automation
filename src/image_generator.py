"""
Image Generator — Pollinations.ai (free, no API key, no rate-limit key needed)
Generates one illustration per scene (victim, each suspect, detective/conclusion)
in a consistent noir/mysterious flat-illustration style so the whole video
feels visually coherent instead of a mismatched grab-bag of styles.
"""

import time
import urllib.parse
from io import BytesIO
from pathlib import Path

import requests
from PIL import Image, ImageDraw

BASE_URL = "https://image.pollinations.ai/prompt/"
STYLE_SUFFIX = (
    ", moody noir mystery illustration, muted dark teal and amber palette, "
    "dramatic single light source, flat vector shading, cinematic composition, "
    "vertical portrait framing, no text, no watermark"
)


class ImageGenerator:
    def __init__(self, output_dir="output/images", width=1080, height=1920, timeout=45):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.width = width
        self.height = height
        self.timeout = timeout

    def _fallback_image(self, filename):
        """Plain dotted background used only if generation fails, so the
        pipeline can still finish a video rather than crash."""
        img = Image.new("RGB", (self.width, self.height), (28, 32, 38))
        draw = ImageDraw.Draw(img)
        for x in range(0, self.width, 40):
            for y in range(0, self.height, 40):
                draw.ellipse([x - 1, y - 1, x + 1, y + 1], fill=(55, 60, 68))
        path = self.output_dir / filename
        img.save(path)
        return path

    def generate_image(self, prompt, filename, seed=None, retries=2):
        full_prompt = prompt + STYLE_SUFFIX
        encoded = urllib.parse.quote(full_prompt)
        url = f"{BASE_URL}{encoded}?width={self.width}&height={self.height}&nologo=true"
        if seed is not None:
            url += f"&seed={seed}"

        for attempt in range(retries + 1):
            try:
                resp = requests.get(url, timeout=self.timeout)
                resp.raise_for_status()
                img = Image.open(BytesIO(resp.content)).convert("RGB")
                path = self.output_dir / filename
                img.save(path, "PNG")
                return path
            except Exception as e:
                if attempt < retries:
                    time.sleep(2)
                    continue
                print(f"  [image_generator] falling back for {filename}: {e}")
                return self._fallback_image(filename)

    def generate_riddle_images(self, riddle_data, riddle_id):
        """
        riddle_data: {"victim": str, "setting": str, "cause": str, "suspects": [...]}
        Returns dict of scene_key -> image path.
        """
        seed_base = abs(hash(riddle_id)) % 100000
        images = {}

        images["hook"] = self.generate_image(
            "a detective silhouette holding a magnifying glass, examining a clue in "
            f"{riddle_data['setting']}",
            f"{riddle_id}_hook.png", seed=seed_base + 1,
        )
        images["victim"] = self.generate_image(
            f"a crime scene showing the aftermath of {riddle_data['cause']} in "
            f"{riddle_data['setting']}, no visible gore, implied tension",
            f"{riddle_id}_victim.png", seed=seed_base + 2,
        )

        for i, suspect in enumerate(riddle_data["suspects"]):
            images[f"suspect_{i}"] = self.generate_image(
                f"a person in the role of {suspect['name']}, standing nervously in "
                f"{riddle_data['setting']}, guarded expression",
                f"{riddle_id}_suspect_{i}.png", seed=seed_base + 10 + i,
            )

        images["conclusion"] = self.generate_image(
            f"a confident detective revealing the culprit, dramatic reveal pose, "
            f"{riddle_data['setting']} in the background",
            f"{riddle_id}_conclusion.png", seed=seed_base + 50,
        )
        return images


if __name__ == "__main__":
    gen = ImageGenerator()
    # local-only smoke test of the fallback path (no network call)
    path = gen._fallback_image("fallback_test.png")
    print("Fallback image written to:", path)

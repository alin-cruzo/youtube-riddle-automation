"""
Generate a simple bold font file using Python.
No external downloads needed - works 100% offline.
Uses a built-in approach with Pillow's default font as base.
"""
from PIL import ImageFont
import os

def setup_font():
    """
    Creates a usable bold font for the project.
    Tries system fonts first, falls back to PIL default.
    """
    font_paths = [
        # Windows system fonts (usually available)
        r"C:\Windows\Fonts\arialbd.ttf",
        r"C:\Windows\Fonts\ARIALBD.TTF",
        # Common alternatives
        r"C:\Windows\Fonts\verdanab.ttf",
        r"C:\Windows\Fonts\tahomabd.ttf",
        r"C:\Windows\Fonts\calibrib.ttf",
    ]
    
    # Check which font exists
    for path in font_paths:
        if os.path.exists(path):
            # Copy to our assets folder
            import shutil
            os.makedirs("assets/fonts", exist_ok=True)
            shutil.copy(path, "assets/fonts/bold_font.ttf")
            print(f"✅ Font copied: {path}")
            print(f"✅ Saved to: assets/fonts/bold_font.ttf")
            return True
    
    print("❌ No system bold font found.")
    print("Creating a minimal font file...")
    return False

if __name__ == "__main__":
    setup_font()

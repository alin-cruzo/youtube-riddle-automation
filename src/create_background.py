"""
Generate the cream dotted background matching the video style.
FREE - Uses only Python PIL (built-in).
"""
from PIL import Image, ImageDraw
from pathlib import Path

def create_dotted_background(width=1080, height=1920, output_path=None):
    """
    Creates the signature cream/beige background with subtle dot grid.
    Matches the analyzed video's background exactly.
    """
    # Cream/beige color from video analysis (RGB)
    bg_color = (240, 235, 220)
    dot_color = (200, 195, 180)  # Subtle darker dots
    
    img = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    
    # Create dotted grid pattern
    dot_spacing = 40
    dot_size = 2
    
    for x in range(0, width, dot_spacing):
        for y in range(0, height, dot_spacing):
            draw.ellipse(
                [x-dot_size, y-dot_size, x+dot_size, y+dot_size],
                fill=dot_color
            )
    
    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        img.save(output_path)
        print(f"✅ Background saved: {output_path}")
    
    return img

if __name__ == "__main__":
    create_dotted_background(
        output_path="assets/backgrounds/dotted_grid.png"
    )
    print("Background generated successfully!")

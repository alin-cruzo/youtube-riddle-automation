"""
Generate ALL character illustrations using Python PIL.
100% FREE - No AI tools, no stock images, no paid resources.
Style: Flat 2D cartoon with muted earth tones (matches video).
"""
from PIL import Image, ImageDraw
from pathlib import Path

def create_character(name, draw_func, size=(400, 600), output_path=None):
    """Base function to create a character image."""
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_func(draw, size[0], size[1])
    
    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        img.save(output_path)
        print(f"Created: {output_path}")
    
    return img

def draw_detective(draw, w, h):
    """Detective in trench coat with magnifying glass."""
    draw.polygon([(w//2, 80), (w//2-60, h-100), (w//2+60, h-100)], fill=(139, 90, 43))
    draw.rectangle([w//2-50, 150, w//2+50, h-100], fill=(160, 110, 60))
    draw.ellipse([w//2-35, 40, w//2+35, 110], fill=(255, 220, 180))
    draw.polygon([(w//2-50, 50), (w//2, 20), (w//2+50, 50)], fill=(120, 80, 40))
    draw.ellipse([w//2-50, 40, w//2+50, 70], fill=(120, 80, 40))
    draw.ellipse([w//2-10, 70, w//2-5, 75], fill=(0, 0, 0))
    draw.ellipse([w//2+5, 70, w//2+10, 75], fill=(0, 0, 0))
    draw.ellipse([w//2+40, 100, w//2+80, 140], outline=(100, 100, 100), width=4)
    draw.line([(w//2+70, 135), (w//2+90, 170)], fill=(80, 80, 80), width=6)
    draw.rectangle([w//2-30, h-100, w//2-10, h-20], fill=(80, 60, 40))
    draw.rectangle([w//2+10, h-100, w//2+30, h-20], fill=(80, 60, 40))
    draw.ellipse([w//2-35, h-30, w//2-5, h-10], fill=(60, 40, 20))
    draw.ellipse([w//2+5, h-30, w//2+35, h-10], fill=(60, 40, 20))

def draw_victim(draw, w, h):
    """Man in striped pajamas lying down."""
    draw.ellipse([50, h//2-40, w-50, h//2+40], fill=(180, 190, 210))
    for i in range(5):
        y = h//2 - 30 + i * 15
        draw.line([(60, y), (w-60, y)], fill=(150, 160, 180), width=3)
    draw.ellipse([w//2-30, h//2-70, w//2+30, h//2-10], fill=(255, 220, 180))
    draw.line([(w//2-15, h//2-45), (w//2-5, h//2-45)], fill=(0, 0, 0), width=2)
    draw.line([(w//2+5, h//2-45), (w//2+15, h//2-45)], fill=(0, 0, 0), width=2)
    draw.polygon([(80, h-80), (100, h-120), (120, h-80)], fill=(200, 200, 200))
    draw.ellipse([70, h-70, 130, h-50], fill=(139, 90, 43))

def draw_police(draw, w, h):
    """Police officer in uniform with notepad."""
    draw.rectangle([w//2-45, 130, w//2+45, h-100], fill=(50, 80, 150))
    draw.ellipse([w//2-30, 50, w//2+30, 110], fill=(255, 220, 180))
    draw.rectangle([w//2-35, 30, w//2+35, 60], fill=(40, 60, 120))
    draw.ellipse([w//2-40, 50, w//2+40, 70], fill=(40, 60, 120))
    draw.ellipse([w//2-5, 40, w//2+5, 50], fill=(255, 215, 0))
    draw.ellipse([w//2-8, 75, w//2-3, 80], fill=(0, 0, 0))
    draw.ellipse([w//2+3, 75, w//2+8, 80], fill=(0, 0, 0))
    draw.rectangle([w//2+30, 140, w//2+70, 200], fill=(255, 255, 230))
    draw.line([(w//2+35, 150), (w//2+65, 150)], fill=(0, 0, 0), width=1)
    draw.line([(w//2+35, 160), (w//2+65, 160)], fill=(0, 0, 0), width=1)
    draw.line([(w//2+35, 170), (w//2+65, 170)], fill=(0, 0, 0), width=1)
    draw.rectangle([w//2-25, h-100, w//2-5, h-20], fill=(40, 60, 100))
    draw.rectangle([w//2+5, h-100, w//2+25, h-20], fill=(40, 60, 100))
    draw.ellipse([w//2-30, h-25, w//2, h-10], fill=(30, 30, 30))
    draw.ellipse([w//2, h-25, w//2+30, h-10], fill=(30, 30, 30))

def draw_wife(draw, w, h):
    """Woman in beige dress holding carrot."""
    draw.polygon([(w//2, 120), (w//2-50, h-100), (w//2+50, h-100)], fill=(210, 190, 170))
    draw.ellipse([w//2-28, 50, w//2+28, 106], fill=(255, 220, 180))
    draw.ellipse([w//2-32, 40, w//2+32, 80], fill=(80, 50, 30))
    draw.ellipse([w//2-8, 75, w//2-3, 80], fill=(0, 0, 0))
    draw.ellipse([w//2+3, 75, w//2+8, 80], fill=(0, 0, 0))
    draw.arc([w//2-10, 82, w//2+10, 95], 0, 180, fill=(100, 50, 50), width=2)
    draw.polygon([(w//2+60, 140), (w//2+90, 130), (w//2+85, 180)], fill=(255, 140, 0))
    draw.polygon([(w//2+85, 130), (w//2+95, 125), (w//2+90, 135)], fill=(50, 150, 50))
    draw.polygon([(w//2+88, 128), (w//2+98, 128), (w//2+92, 138)], fill=(50, 150, 50))
    draw.rectangle([w//2-20, h-100, w//2-5, h-30], fill=(255, 220, 180))
    draw.rectangle([w//2+5, h-100, w//2+20, h-30], fill=(255, 220, 180))
    draw.ellipse([w//2-25, h-25, w//2-5, h-10], fill=(150, 100, 80))
    draw.ellipse([w//2+5, h-25, w//2+25, h-10], fill=(150, 100, 80))

def draw_brother(draw, w, h):
    """Young man with wet dog."""
    draw.rectangle([w//2-35, 130, w//2+35, h-100], fill=(100, 130, 100))
    draw.ellipse([w//2-25, 55, w//2+25, 105], fill=(255, 220, 180))
    draw.polygon([(w//2-25, 60), (w//2, 40), (w//2+25, 60)], fill=(80, 60, 40))
    draw.ellipse([w//2-8, 75, w//2-3, 80], fill=(0, 0, 0))
    draw.ellipse([w//2+3, 75, w//2+8, 80], fill=(0, 0, 0))
    for pos in [(w//2-20, 140), (w//2+15, 160), (w//2, 180)]:
        draw.ellipse([pos[0], pos[1], pos[0]+5, pos[1]+8], fill=(150, 200, 255))
    draw.ellipse([w//2-80, h-150, w//2+20, h-80], fill=(139, 110, 80))
    draw.ellipse([w//2-90, h-170, w//2-40, h-120], fill=(139, 110, 80))
    draw.ellipse([w//2-85, h-160, w//2-75, h-150], fill=(0, 0, 0))
    draw.polygon([(w//2-70, h-140), (w//2-60, h-140), (w//2-65, h-130)], fill=(100, 80, 60))
    for pos in [(w//2-60, h-140), (w//2-30, h-110)]:
        draw.ellipse([pos[0], pos[1], pos[0]+4, pos[1]+6], fill=(150, 200, 255))
    draw.rectangle([w//2-20, h-100, w//2-5, h-20], fill=(80, 100, 80))
    draw.rectangle([w//2+5, h-100, w//2+20, h-20], fill=(80, 100, 80))

def draw_son(draw, w, h):
    """Teenage boy, wet from shower."""
    draw.rectangle([w//2-30, 130, w//2+30, h-100], fill=(230, 240, 250))
    draw.ellipse([w//2-25, 55, w//2+25, 105], fill=(255, 220, 180))
    draw.polygon([(w//2-25, 65), (w//2-15, 45), (w//2-5, 60), (w//2+5, 45), (w//2+15, 60), (w//2+25, 65)], fill=(60, 50, 40))
    draw.ellipse([w//2-8, 75, w//2-3, 80], fill=(0, 0, 0))
    draw.ellipse([w//2+3, 75, w//2+8, 80], fill=(0, 0, 0))
    for pos in [(w//2-15, 140), (w//2+10, 160), (w//2, 180), (w//2-20, 200)]:
        draw.ellipse([pos[0], pos[1], pos[0]+4, pos[1]+7], fill=(180, 220, 255))
    draw.rectangle([w//2-25, h-100, w//2-5, h-20], fill=(60, 90, 140))
    draw.rectangle([w//2+5, h-100, w//2+25, h-20], fill=(60, 90, 140))
    draw.ellipse([w//2-30, h-25, w//2-5, h-10], fill=(200, 200, 200))
    draw.ellipse([w//2+5, h-25, w//2+30, h-10], fill=(200, 200, 200))

def draw_maid(draw, w, h):
    """Maid in uniform with wet laundry basket."""
    draw.rectangle([w//2-40, 130, w//2+40, h-100], fill=(40, 40, 40))
    draw.rectangle([w//2-25, 140, w//2+25, h-120], fill=(255, 255, 255))
    draw.ellipse([w//2-25, 55, w//2+25, 105], fill=(255, 220, 180))
    draw.ellipse([w//2-30, 45, w//2+30, 75], fill=(60, 40, 30))
    draw.ellipse([w//2-10, 35, w//2+10, 55], fill=(60, 40, 30))
    draw.polygon([(w//2-20, 50), (w//2, 35), (w//2+20, 50)], fill=(255, 255, 255))
    draw.ellipse([w//2-8, 75, w//2-3, 80], fill=(0, 0, 0))
    draw.ellipse([w//2+3, 75, w//2+8, 80], fill=(0, 0, 0))
    draw.arc([w//2-10, 82, w//2+10, 95], 0, 180, fill=(100, 50, 50), width=2)
    draw.rectangle([w//2+30, 150, w//2+90, 220], fill=(100, 150, 200))
    draw.ellipse([w//2+35, 140, w//2+55, 160], fill=(255, 100, 100))
    draw.ellipse([w//2+50, 135, w//2+70, 155], fill=(100, 255, 100))
    draw.ellipse([w//2+65, 140, w//2+85, 160], fill=(255, 255, 100))
    for pos in [(w//2+40, 225), (w//2+60, 230), (w//2+80, 225)]:
        draw.ellipse([pos[0], pos[1], pos[0]+3, pos[1]+5], fill=(150, 200, 255))
    draw.rectangle([w//2-20, h-100, w//2-5, h-30], fill=(255, 220, 180))
    draw.rectangle([w//2+5, h-100, w//2+20, h-30], fill=(255, 220, 180))
    draw.ellipse([w//2-25, h-25, w//2-5, h-10], fill=(50, 50, 50))
    draw.ellipse([w//2+5, h-25, w//2+25, h-10], fill=(50, 50, 50))

def draw_cook(draw, w, h):
    """Chef in white coat with frying pan."""
    draw.rectangle([w//2-40, 130, w//2+40, h-100], fill=(255, 255, 255))
    for y in [150, 170, 190, 210]:
        draw.ellipse([w//2-3, y, w//2+3, y+6], fill=(0, 0, 0))
    draw.ellipse([w//2-25, 55, w//2+25, 105], fill=(255, 220, 180))
    draw.rectangle([w//2-30, 20, w//2+30, 55], fill=(255, 255, 255))
    draw.ellipse([w//2-35, 10, w//2+35, 30], fill=(255, 255, 255))
    draw.ellipse([w//2-8, 75, w//2-3, 80], fill=(0, 0, 0))
    draw.ellipse([w//2+3, 75, w//2+8, 80], fill=(0, 0, 0))
    draw.line([(w//2+40, 160), (w//2+100, 160)], fill=(60, 60, 60), width=6)
    draw.ellipse([w//2+90, 145, w//2+130, 175], fill=(80, 80, 80))
    draw.rectangle([w//2-20, h-100, w//2-5, h-20], fill=(50, 50, 50))
    draw.rectangle([w//2+5, h-100, w//2+20, h-20], fill=(50, 50, 50))
    draw.ellipse([w//2-25, h-25, w//2-5, h-10], fill=(30, 30, 30))
    draw.ellipse([w//2+5, h-25, w//2+25, h-10], fill=(30, 30, 30))

def draw_two_brains(draw, w, h):
    """Two heads: one with gears, one with scribbles."""
    draw.ellipse([40, 100, 180, 240], fill=(255, 220, 180), outline=(0,0,0), width=2)
    draw.ellipse([80, 140, 110, 170], fill=(150, 200, 220), outline=(80, 130, 150), width=2)
    draw.ellipse([110, 150, 140, 180], fill=(150, 200, 220), outline=(80, 130, 150), width=2)
    draw.ellipse([95, 170, 125, 200], fill=(150, 200, 220), outline=(80, 130, 150), width=2)
    draw.ellipse([220, 100, 360, 240], fill=(255, 220, 180), outline=(0,0,0), width=2)
    for i in range(8):
        x1, y1 = 250 + i*10, 130 + (i%3)*20
        x2, y2 = 280 + i*8, 160 + (i%4)*15
        draw.line([(x1, y1), (x2, y2)], fill=(80, 80, 80), width=2)
        draw.line([(x2, y1), (x1, y2)], fill=(80, 80, 80), width=2)

CHARACTERS = {
    "detective": draw_detective,
    "victim": draw_victim,
    "police": draw_police,
    "wife": draw_wife,
    "brother": draw_brother,
    "son": draw_son,
    "maid": draw_maid,
    "cook": draw_cook,
    "two_brains": draw_two_brains,
}

if __name__ == "__main__":
    print("=" * 50)
    print("GENERATING FREE CHARACTER ILLUSTRATIONS")
    print("100% Python-generated, no paid tools used")
    print("=" * 50)
    
    for name, draw_func in CHARACTERS.items():
        output_path = f"assets/characters/{name}.png"
        create_character(name, draw_func, output_path=output_path)
    
    print("\n" + "=" * 50)
    print("ALL CHARACTERS GENERATED!")
    print("=" * 50)

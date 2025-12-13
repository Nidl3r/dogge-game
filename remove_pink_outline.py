from PIL import Image
import os

# Directory
assets_dir = "assets"

# All sprite files to process
files = [
    "processed_idle",
    "processed_walk_1", "processed_walk_2", "processed_walk_3", "processed_walk_4",
    "processed_walk_5", "processed_walk_6", "processed_walk_7",
    "processed_sit_1", "processed_sit_2",
    "processed_poop_1", "processed_poop_2", "processed_poop_3", "processed_poop_4"
]

# Pink/magenta colors to remove
pink_colors = [
    (255, 0, 255),    # Pure magenta
    (255, 1, 255),    # Near magenta
    (254, 0, 254),    # Near magenta
    (255, 0, 254),    # Near magenta
    (254, 0, 255),    # Near magenta
]

def is_pink_color(r, g, b):
    """Check if a color is pink/magenta"""
    for pink_r, pink_g, pink_b in pink_colors:
        if abs(r - pink_r) <= 5 and abs(g - pink_g) <= 5 and abs(b - pink_b) <= 5:
            return True
    return False

def remove_pink_outline(img_path):
    """Remove pink/magenta outline from sprite"""
    img = Image.open(img_path).convert("RGBA")
    pixels = img.load()
    width, height = img.size
    
    # Process each pixel
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            
            # If pixel is pink/magenta, make it transparent
            if a > 0 and is_pink_color(r, g, b):
                pixels[x, y] = (r, g, b, 0)  # Make transparent
    
    return img

# Process each file
print("Removing pink outlines from sprites...")
for name in files:
    filename = name + ".png"
    path = os.path.join(assets_dir, filename)
    
    if not os.path.exists(path):
        print(f"⚠ Skipping {filename}, not found")
        continue
    
    print(f"Processing {filename}...")
    cleaned = remove_pink_outline(path)
    cleaned.save(path)
    print(f"✓ Cleaned {filename}")

print("\n✅ All sprites processed! Pink outlines removed.")

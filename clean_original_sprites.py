from PIL import Image
import os

# Directory
assets_dir = "assets"

# ORIGINAL sprite files (not the processed ones)
files = [
    "idle",
    "walk_1", "walk_2", "walk_3", "walk_4", "walk_5", "walk_6", "walk_7",
    "sit_1", "sit_2",
    "poop_1", "poop_2", "poop_3", "poop_4"
]

# Pink/magenta colors to remove (expanded range)
def is_pink_outline(r, g, b):
    """Check if a color is pink/magenta outline color"""
    # Pure magenta and close variants
    if abs(r - 255) <= 10 and abs(g - 0) <= 10 and abs(b - 255) <= 10:
        return True
    # Also check for lighter magenta/pink
    if abs(r - 255) <= 20 and abs(g - 0) <= 50 and abs(b - 255) <= 20:
        return True
    return False

def remove_pink_outline(img_path):
    """Remove pink/magenta outline from sprite"""
    img = Image.open(img_path).convert("RGBA")
    pixels = img.load()
    width, height = img.size
    
    pink_count = 0
    
    # Process each pixel
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            
            # If pixel is pink/magenta, make it transparent
            if a > 0 and is_pink_outline(r, g, b):
                pixels[x, y] = (r, g, b, 0)  # Make transparent
                pink_count += 1
    
    return img, pink_count

# Process each file
print("Cleaning ORIGINAL sprite files...")
total_removed = 0
for name in files:
    filename = name + ".png"
    path = os.path.join(assets_dir, filename)
    
    if not os.path.exists(path):
        print(f"⚠ Skipping {filename}, not found")
        continue
    
    print(f"Processing {filename}...", end=" ")
    cleaned, pink_count = remove_pink_outline(path)
    cleaned.save(path)
    total_removed += pink_count
    print(f"✓ Removed {pink_count} pink pixels")

print(f"\n✅ Done! Removed {total_removed} total pink pixels from original sprites.")

from PIL import Image
import os

# Directory
assets_dir = "assets"

# ALL processed sprite files
files = [
    "processed_idle",
    "processed_walk_1", "processed_walk_2", "processed_walk_3", "processed_walk_4",
    "processed_walk_5", "processed_walk_6", "processed_walk_7",
    "processed_sit_1", "processed_sit_2",
    "processed_poop_1", "processed_poop_2", "processed_poop_3", "processed_poop_4"
]

def remove_all_pink(img_path):
    """Aggressively remove all pink/magenta pixels"""
    img = Image.open(img_path).convert("RGBA")
    pixels = img.load()
    width, height = img.size
    
    removed = 0
    
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            
            # If pixel has alpha and is pink/magenta (high R, low G, high B)
            if a > 0:
                # Very aggressive check - any pixel where R and B are high and G is low
                if r > 180 and b > 180 and g < 100:
                    pixels[x, y] = (0, 0, 0, 0)  # Make fully transparent
                    removed += 1
    
    return img, removed

# Process each file
print("Aggressively removing ALL pink/magenta pixels from processed sprites...")
total_removed = 0

for name in files:
    filename = name + ".png"
    path = os.path.join(assets_dir, filename)
    
    if not os.path.exists(path):
        print(f"⚠ Skipping {filename}, not found")
        continue
    
    print(f"Processing {filename}...", end=" ")
    cleaned, pink_count = remove_all_pink(path)
    
    if pink_count > 0:
        cleaned.save(path)
        total_removed += pink_count
        print(f"✓ REMOVED {pink_count} pink pixels!")
    else:
        print(f"✓ Already clean (0 pink pixels)")

print(f"\n{'='*60}")
print(f"✅ Done! Removed {total_removed} total pink pixels.")
print(f"{'='*60}\n")

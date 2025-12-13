from PIL import Image
import os

# Check a sample processed sprite to see what colors are present
assets_dir = "assets"
filename = "processed_walk_1.png"
path = os.path.join(assets_dir, filename)

img = Image.open(path).convert("RGBA")
pixels = img.load()
width, height = img.size

# Collect all unique colors with their pixel counts
color_counts = {}
for y in range(height):
    for x in range(width):
        r, g, b, a = pixels[x, y]
        if a > 0:  # Only non-transparent pixels
            color_key = (r, g, b, a)
            color_counts[color_key] = color_counts.get(color_key, 0) + 1

# Sort by count and show top colors
sorted_colors = sorted(color_counts.items(), key=lambda x: x[1], reverse=True)

print(f"Analyzing {filename}...")
print(f"Image size: {width}x{height}")
print(f"\nTop colors found (R, G, B, A) : pixel_count")
print("=" * 50)

for i, (color, count) in enumerate(sorted_colors[:20]):
    r, g, b, a = color
    # Highlight if it's pink/magenta
    if abs(r - 255) <= 20 and abs(b - 255) <= 20 and g < 100:
        marker = " ⚠ PINK/MAGENTA!"
    else:
        marker = ""
    print(f"{i+1}. ({r:3d}, {g:3d}, {b:3d}, {a:3d}) : {count:5d} pixels{marker}")

print("\n" + "=" * 50)
print(f"Total unique colors: {len(color_counts)}")

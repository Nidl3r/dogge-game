from PIL import Image
import os

# Check the ORIGINAL idle sprite
img = Image.open("assets/idle.png").convert("RGBA")
px = img.load()
width, height = img.size

# Find ALL pixels and their colors
all_colors = {}
pink_pixels = []

for y in range(height):
    for x in range(width):
        r, g, b, a = px[x, y]
        if a > 0:
            key = (r, g, b)
            all_colors[key] = all_colors.get(key, 0) + 1
            # Check if pink/magenta
            if r > 180 and b > 180 and g < 100:
                pink_pixels.append((x, y, r, g, b))

print(f"Analyzing ORIGINAL idle.png sprite")
print(f"Image size: {width}x{height}")
print(f"=" * 60)

# Show all colors sorted by count
sorted_colors = sorted(all_colors.items(), key=lambda x: x[1], reverse=True)
print(f"\nAll colors in sprite ({len(all_colors)} unique):")
for i, ((r, g, b), count) in enumerate(sorted_colors[:25]):
    marker = " ⚠ PINK/MAGENTA!" if (r > 180 and b > 180 and g < 100) else ""
    print(f"{i+1}. RGB({r:3d}, {g:3d}, {b:3d}): {count:5d} pixels{marker}")

if pink_pixels:
    print(f"\n⚠ Found {len(pink_pixels)} pink/magenta pixels in the ORIGINAL sprite!")
    print(f"First 10 pink pixels:")
    for x, y, r, g, b in pink_pixels[:10]:
        print(f"  Position ({x},{y}): RGB({r},{g},{b})")
else:
    print(f"\n✓ No pink pixels found in original sprite!")

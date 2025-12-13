from PIL import Image
import os

# Let's check ALL colors in the sprite, not just top ones
assets_dir = "assets"
filename = "processed_walk_1.png"
path = os.path.join(assets_dir, filename)

img = Image.open(path).convert("RGBA")
pixels = img.load()
width, height = img.size

# Find all magenta/pink pixels
magenta_pixels = []
for y in range(height):
    for x in range(width):
        r, g, b, a = pixels[x, y]
        if a > 0:  # Only non-transparent pixels
            # Check if it's pink/magenta (high R, low G, high B)
            if r > 200 and b > 200 and g < 100:
                magenta_pixels.append((x, y, r, g, b, a))

print(f"Analyzing {filename}...")
print(f"Image size: {width}x{height}")
print(f"\nFound {len(magenta_pixels)} magenta/pink pixels:")
print("=" * 70)

if magenta_pixels:
    # Show first 30 pixels
    for i, (x, y, r, g, b, a) in enumerate(magenta_pixels[:30]):
        print(f"  Pixel at ({x:3d}, {y:3d}): RGB({r},{g},{b}) Alpha={a}")
    if len(magenta_pixels) > 30:
        print(f"  ... and {len(magenta_pixels) - 30} more")
    
    print("\nThese ARE the pink outline pixels! Removing them now...")
    
    # Remove them
    for x, y, *_ in magenta_pixels:
        pixels[x, y] = (0, 0, 0, 0)
    
    # Save
    img.save(path)
    print(f"✓ Saved {filename} with {len(magenta_pixels)} pink pixels removed!")
else:
    print("No pink pixels found - sprite is clean!")

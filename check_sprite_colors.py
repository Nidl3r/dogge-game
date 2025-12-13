from PIL import Image

# Load and display the colors in one sprite
img = Image.open("assets/processed_idle.png").convert("RGBA")
px = img.load()

# Sample the edge pixels to see what colors are there
print("Sampling edge pixels from processed_idle.png")
print("=" * 60)

# Check perimeter of the image
width, height = img.size
edge_colors = {}

# Sample top, bottom, left, right edges
for x in range(width):
    for y in [0, 1, height-2, height-1]:
        r, g, b, a = px[x, y]
        if a > 0:
            key = (r, g, b)
            edge_colors[key] = edge_colors.get(key, 0) + 1

for y in range(height):
    for x in [0, 1, width-2, width-1]:
        r, g, b, a =px[x, y]
        if a > 0:
            key = (r, g, b)
            edge_colors[key] = edge_colors.get(key, 0) + 1

# Show all edge colors
sorted_edges = sorted(edge_colors.items(), key=lambda x: x[1], reverse=True)
print(f"Edge colors found ({len(sorted_edges)} unique):")
for (r, g, b), count in sorted_edges[:15]:
    # Mark if pink/magenta
    marker = " ⚠ PINK!" if (r > 180 and b > 180 and g < 100) else ""
    print(f"  RGB({r:3d}, {g:3d}, {b:3d}): {count:4d} pixels{marker}")

# Now check what the dog pixels are
dog_colors = {}
for y in range(height):
    for x in range(width):
        r, g, b, a = px[x, y]
        if a > 0:
            key = (r, g, b)
            dog_colors[key] = dog_colors.get(key, 0) + 1

print(f"\nAll sprite colors ({len(dog_colors)} unique):")
sorted_colors = sorted(dog_colors.items(), key=lambda x: x[1], reverse=True)[:20]
for (r, g, b), count in sorted_colors:
    marker = " ⚠ PINK!" if (r > 180 and b > 180 and g < 100) else ""
    print(f"  RGB({r:3d}, {g:3d}, {b:3d}): {count:5d} pixels{marker}")

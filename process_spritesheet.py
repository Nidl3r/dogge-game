import pygame
import os
import math

# Path to the uploaded image
image_path = r"C:/Users/HullingerLandon/.gemini/antigravity/brain/cc198623-47eb-48ec-bbd0-86036398463b/uploaded_image_1765589543621.png"
output_file = "schnauzer_art.py"

def process():
    if not os.path.exists(image_path):
        print(f"Error: Image not found at {image_path}")
        return

    pygame.init()
    try:
        img = pygame.image.load(image_path)
    except Exception as e:
        print(f"Error loading image: {e}")
        return

    width, height = img.get_size()
    print(f"Image Size: {width}x{height}")
    
    # Assume grid based on dimensions
    # If width is 1024 -> 8 cols -> 128px
    # If height is ~500 -> 4 rows -> ~128px
    # With the new image we need to check if it matches the 128x128 expectations.
    
    cols = 8
    rows = 4
    
    grid_w = width // cols
    grid_h = height // rows
    
    # Heuristic: force 128x128 if close to avoid padding issues
    # 558 / 4 = 139.5, which is close to 128 but likely has padding.
    # Standard sprite sheets are usually power-of-2 or square.
    if abs(grid_w - 128) < 10: grid_w = 128
    
    # If width is 128, likely height is too (square tiles)
    # The user's image is 558 high. 4 * 128 = 512. 
    # This leaves 46 pixels of empty space at the bottom.
    # We should ignore that padding and just use 128.
    grid_h = 128
    
    print(f"Using Grid: {grid_w}x{grid_h}")
    
    frames_data = {}
    
    anim_map = {
        0: 'idle',
        1: 'walk',
        2: 'sit',
        3: 'poop' 
    }
    
    # Check for transparency
    has_alpha = img.get_flags() & pygame.SRCALPHA
    print(f"Has Alpha Channel: {bool(has_alpha)}")
    
    print("Extracting frames...")
    
    for r in range(rows):
        anim_name = anim_map.get(r, f'row_{r}')
        for c in range(cols):
            cell_x = c * grid_w
            cell_y = r * grid_h
            
            pixels = []
            
            for y in range(grid_h):
                for x in range(grid_w):
                    px = cell_x + x
                    py = cell_y + y
                    
                    if px >= width or py >= height: continue
                    
                    color = img.get_at((px, py))
                    
                    # Transparency check
                    if has_alpha and color.a < 20: 
                        continue
                        
                    pixels.append((x, y, (color.r, color.g, color.b)))
            
            if not pixels: continue
            if len(pixels) < 20: continue # Empty frame

            frame_key = f"{anim_name}_{c}"
            frames_data[frame_key] = pixels
            # print(f"  Extracted {frame_key}: {len(pixels)} pixels")

    print(f"Total frames: {len(frames_data)}")
    
    # Write output
    with open(output_file, 'w') as f:
        f.write("import pygame\n\n")
        f.write("# Generated sprite data from sheet\n")
        f.write(f"GRID_SIZE = ({grid_w}, {grid_h})\n\n")
        
        f.write("FRAMES = {\n")
        for key, px_list in frames_data.items():
            f.write(f"    '{key}': [\n")
            chunk_size = 8
            for i in range(0, len(px_list), chunk_size):
                chunk = px_list[i:i+chunk_size]
                f.write("        " + ", ".join(str(p) for p in chunk) + ",\n")
            f.write("    ],\n")
        f.write("}\n\n")
        
        f.write("def draw_frame(surface, anim_name, frame_idx, x, y, scale=1):\n")
        f.write("    key = f'{anim_name}_{frame_idx}'\n")
        f.write("    if key not in FRAMES:\n")
        f.write("        return\n")
        f.write("\n")
        f.write("    pixels = FRAMES[key]\n")
        f.write("    for px, py, color in pixels:\n")
        f.write("        pygame.draw.rect(surface, color, (x + px*scale, y + py*scale, scale, scale))\n")

    print(f"Done. Saved to {output_file}")
    pygame.quit()

if __name__ == "__main__":
    process()

import pygame
import os

pygame.init()

image_path = r"C:/Users/HullingerLandon/.gemini/antigravity/brain/cc198623-47eb-48ec-bbd0-86036398463b/uploaded_image_1765587447337.jpg"
output_file = "generated_sprite_data.py"

def generate():
    if not os.path.exists(image_path):
        print("Image not found")
        return

    img = pygame.image.load(image_path)
    width, height = img.get_size()
    
    # Heuristic for "unit size": smallest run length
    min_run = 100
    for y in range(0, height, 20):
        prev = img.get_at((0, y))
        count = 1
        for x in range(1, width):
            c = img.get_at((x, y))
            if c != prev:
                if count > 2 and count < min_run:
                    min_run = count
                count = 1
                prev = c
            else:
                count += 1
    
    # If min_run is still huge or 1, clamp it reasonable
    print(f"Detected pixel scale: {min_run}")
    if min_run < 3: min_run = 10 # Default to something reasonable if detection fails
    
    scale = min_run
    w_grid = width // scale
    h_grid = height // scale
    
    print(f"Grid: {w_grid}x{h_grid}")
    
    # Sample background colors from 4 corners
    corners = [
        img.get_at((0, 0)),
        img.get_at((width-1, 0)),
        img.get_at((0, height-1)),
        img.get_at((width-1, height-1))
    ]
    
    # Identify background colors (checkerboard might have two)
    bg_colors = set()
    for c in corners:
        bg_colors.add((c[0], c[1], c[2]))
        
    print(f"Background colors to exclude: {bg_colors}")
    
    # Open output file
    with open(output_file, 'w') as f:
        f.write('import pygame\n\n')
        f.write('def draw_new_schnauzer(surface, x_offset=0, y_offset=0, scale=1):\n')
        f.write('    """Generated sprite drawing code"""\n')
        
        # We need to center the sprite.
        # Find bounds of non-bg pixels
        min_gx, max_gx = w_grid, 0
        min_gy, max_gy = h_grid, 0
        
        pixel_data = []
        
        for y in range(h_grid):
            for x in range(w_grid):
                sample_x = int(x * scale + scale / 2)
                sample_y = int(y * scale + scale / 2)
                
                if sample_x >= width or sample_y >= height: continue
                
                c = img.get_at((sample_x, sample_y))
                rgb = (c[0], c[1], c[2])
                
                # Check if background
                is_bg = False
                for bg in bg_colors:
                    if abs(rgb[0]-bg[0]) < 15 and abs(rgb[1]-bg[1]) < 15 and abs(rgb[2]-bg[2]) < 15:
                        is_bg = True
                        break
                
                if not is_bg:
                    pixel_data.append((x, y, rgb))
                    if x < min_gx: min_gx = x
                    if x > max_gx: max_gx = x
                    if y < min_gy: min_gy = y
                    if y > max_gy: max_gy = y
        
        # Write commands centered
        w_sprite = max_gx - min_gx + 1
        h_sprite = max_gy - min_gy + 1
        
        print(f"Sprite logical size: {w_sprite}x{h_sprite}")
        
        for (x, y, rgb) in pixel_data:
            # Adjust x,y to be relative to sprite origin (0,0)
            rel_x = x - min_gx
            rel_y = y - min_gy
            f.write(f'    pygame.draw.rect(surface, {rgb}, (x_offset + {rel_x}*scale, y_offset + {rel_y}*scale, scale, scale))\n')
            
    print(f"Done. Written to {output_file}")

generate()

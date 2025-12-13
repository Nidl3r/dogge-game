import pygame
import os

pygame.init()

image_path = r"C:/Users/HullingerLandon/.gemini/antigravity/brain/cc198623-47eb-48ec-bbd0-86036398463b/uploaded_image_1765587447337.jpg"

def analyze():
    if not os.path.exists(image_path):
        print("Image not found")
        return

    img = pygame.image.load(image_path)
    width, height = img.get_size()
    print(f"Original Size: {width}x{height}")

    # Analyze a center row to find pixel transitions
    # This helps guess the "pixel size" (scaling factor)
    row_y = height // 2
    transitions = []
    last_color = img.get_at((0, row_y))
    run_length = 0
    
    for x in range(width):
        color = img.get_at((x, row_y))
        if color != last_color:
            transitions.append(run_length)
            run_length = 0
            last_color = color
        run_length += 1
    
    # Simple mode or min of transitions might indicate pixel size
    if transitions:
        # Filter small noise
        transitions = [t for t in transitions if t > 2]
        if transitions:
            est_pixel_size = min(transitions)
            print(f"Estimated pixel unit size: {est_pixel_size}px")
        else:
            print("Could not estimate pixel size (no clear transitions)")
            est_pixel_size = 1 # Fallback
    else:
        print("No transitions found")
        est_pixel_size = 1

    # If the image is large, let's assume a grid of maybe 32x32 or 48x48
    # Let's try to verify if we can downscale
    
    # Visual check: Sample the center of each "block"
    # effective width/height in "pet pixels"
    
    # If the dog is "schnauzer" sized, usually 20-40 pixels wide.
    # If image is 1000px, and dog is 40px, scale is ~25.
    
    scale = 0
    # Let's try to find the GCD of run lengths? No, too complex.
    # Let's just pick a reasonable target size for a desktop pet.
    # The current pet is 48px size.
    # If detailed pixel art, maybe 32x32?
    
    # Let's try scanning for the smallest run length again, more robustly.
    # Horizontal and vertical.
    
    min_run = 1000
    for y in range(0, height, 10):
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
                
    print(f"Robust estimated unit size: {min_run}")
    
    scale = min_run
    w_grid = width // scale
    h_grid = height // scale
    
    print(f"Grid size: {w_grid}x{h_grid}")
    
    # Now generate a color map
    # We will sample the center of each grid cell
    
    print("\nColor Map Sample (Middle 10x10 area):")
    start_x = w_grid // 2 - 5
    start_y = h_grid // 2 - 5
    
    final_commands = []
    
    # Identify background color (usually corners)
    bg_color = img.get_at((0, 0))
    print(f"Assumed Background Color: {bg_color}")
    
    # Generate draw commands
    # We'll normalize colors to rounded RGB to group them
    palette = {}
    
    for y in range(h_grid):
        for x in range(w_grid):
            sample_x = x * scale + scale // 2
            sample_y = y * scale + scale // 2
            if sample_x >= width or sample_y >= height: continue
            
            c = img.get_at((sample_x, sample_y))
            # Rough equality for background
            if abs(c[0]-bg_color[0]) < 10 and abs(c[1]-bg_color[1]) < 10 and abs(c[2]-bg_color[2]) < 10:
                continue # Skip background
                
            rgb = (c[0], c[1], c[2])
            
            # Map detailed colors to keys
            # (Just strict for now)
            
            final_commands.append(f"pygame.draw.rect(surface, {rgb}, ({x}*s, {y}*s, 1*s, 1*s))")

    print(f"\nGenerated {len(final_commands)} draw commands.")
    print("Example commands:")
    for cmd in final_commands[:5]:
        print(cmd)

analyze()

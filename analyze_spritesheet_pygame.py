import pygame
import sys

# Initialize pygame
pygame.init()

image_path = r'C:/Users/HullingerLandon/.gemini/antigravity/brain/cc198623-47eb-48ec-bbd0-86036398463b/uploaded_image_1765588599180.jpg'

try:
    img = pygame.image.load(image_path)
    width, height = img.get_width(), img.get_height()
    print(f"Image Size: {width}x{height}")
    
    # Lock for pixel access
    img.lock()
    
    bg_color = img.get_at((0, 0))
    print(f"Background color (0,0): {bg_color}")
    
    # Try to determine grid size by walking diagonal? 
    # Or just output some sample checks.
    
    # Count rows of sprites?
    # Simple heuristic: Scan vertical center line, change in color from BG might indicate sprite
    
    print("Vertical scan middle:")
    mid_x = width // 2
    changes = 0
    in_sprite = False
    
    # scan vertical
    for y in range(height):
        c = img.get_at((mid_x, y))
        # Simple diff
        diff = abs(c.r - bg_color.r) + abs(c.g - bg_color.g) + abs(c.b - bg_color.b)
        is_bg = diff < 30 # Tolerance for JPG
        
        if not is_bg and not in_sprite:
            in_sprite = True
            changes += 1
            # print(f"Sprite start at y={y}")
        elif is_bg and in_sprite:
            in_sprite = False
            # print(f"Sprite end at y={y}")
            
    print(f"Found approx {changes} sprite rows based on center line.")

    img.unlock()
    
except Exception as e:
    print(f"Error: {e}")
pygame.quit()

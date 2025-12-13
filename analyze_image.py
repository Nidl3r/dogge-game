import pygame
import os

# Initialize pygame
pygame.init()

# Path to the uploaded image
image_path = r"C:/Users/HullingerLandon/.gemini/antigravity/brain/cc198623-47eb-48ec-bbd0-86036398463b/uploaded_image_1765587447337.jpg"

try:
    if os.path.exists(image_path):
        img = pygame.image.load(image_path)
        width, height = img.get_size()
        print(f"Image Size: {width}x{height}")
        
        # approximate grid size
        # assuming the image is pixel art scaled up or raw
        # Let's just sample a grid.
        # If the original code used 16x16, let's see what this one looks like.
        # It looks like 24x24 or 32x32 maybe? 
        # I'll sample a central area or just print unique colors.
        
        # Let's just guess a grid size. If the image is like 480x480, and it's pixel art, 
        # the "pixels" might be 10x10 or something.
        
        # Simple color histogram
        colors = {}
        for x in range(width):
            for y in range(height):
                c = img.get_at((x, y))
                if c[3] > 0: # not transparent
                    rgb = (c[0], c[1], c[2])
                    colors[rgb] = colors.get(rgb, 0) + 1
        
        print("\nTop 10 Colors:")
        sorted_colors = sorted(colors.items(), key=lambda item: item[1], reverse=True)
        for c in sorted_colors[:10]:
            print(c)
            
    else:
        print("Image file not found.")

    pygame.quit()

except Exception as e:
    print(f"Error: {e}")

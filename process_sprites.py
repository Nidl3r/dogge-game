import pygame
import os

pygame.init()
assets_dir = "assets"
files = ["idle", "walk_1", "walk_2", "walk_3", "walk_4", "walk_5", "walk_6", "walk_7", "sit_1", "sit_2", "poop_1", "poop_2", "poop_3", "poop_4"]
ext = ".png"

TARGET_SIZE = (120, 120)

for name in files:
    filename = name + ext
    path = os.path.join(assets_dir, filename)
    if not os.path.exists(path):
        print(f"Skipping {filename}, not found")
        continue
        
    img = pygame.image.load(path)
    # Handle transparency or colorkey
    if img.get_at((0,0))[3] != 0:
        img.set_colorkey(img.get_at((0,0)))
        
    rect = img.get_bounding_rect()
    cropped = img.subsurface(rect)
    
    # Create target surface
    out_surf = pygame.Surface(TARGET_SIZE, pygame.SRCALPHA)
    out_surf.fill((0,0,0,0))
    
    # Calculate position: Center horizontally, Bottom aligned
    # padding from bottom: 10px? 
    x = (TARGET_SIZE[0] - rect.width) // 2
    y = (TARGET_SIZE[1] - rect.height)
    
    # Clamp to ensure it doesn't go off screen if too big
    if x < 0: x = 0
    if y < 0: y = 0
    
    out_surf.blit(cropped, (x, y))
    
    out_path = os.path.join(assets_dir, f"processed_{filename}")
    pygame.image.save(out_surf, out_path)
    print(f"Processed {filename} -> {out_path} (Content size: {rect.width}x{rect.height})")

pygame.quit()

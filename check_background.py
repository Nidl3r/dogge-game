import pygame
import os

pygame.init()
assets_dir = "assets"
target = "idle.png"
path = os.path.join(assets_dir, target)

if os.path.exists(path):
    img = pygame.image.load(path)
    print(f"Image mode: {img.get_alpha()}")
    # Check top-left pixel
    tl = img.get_at((0, 0))
    print(f"Top-left pixel: {tl}")
    
    # Find bounding box if we assume top-left is background
    # Pygame's get_bounding_rect can work if we set colorkey or if it's alpha
    if tl[3] == 0:
        print("Background is transparent")
        rect = img.get_bounding_rect()
        print(f"Content rect: {rect}")
    else:
        print("Background is NOT transparent. Setting colorkey to top-left pixel.")
        img.set_colorkey(tl)
        rect = img.get_bounding_rect()
        print(f"Content rect with colorkey: {rect}")

pygame.quit()

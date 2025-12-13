import pygame
import os

pygame.init()
assets_dir = "assets"
files = ["idle.png", "walk_1.png", "walk_2.png", "sit_1.png", "sit_2.png", "poop_1.png", "poop_2.png", "poop_3.png", "poop_4.png"]

for f in files:
    path = os.path.join(assets_dir, f)
    if os.path.exists(path):
        img = pygame.image.load(path)
        # Check if transparent
        if img.get_at((0,0))[3] == 0:
            rect = img.get_bounding_rect()
            print(f"{f}: {rect}")
        else:
            img.set_colorkey(img.get_at((0,0)))
            rect = img.get_bounding_rect()
            print(f"{f}: {rect} (colorkeyed)")
pygame.quit()

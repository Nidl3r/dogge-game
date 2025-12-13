import pygame
import os

pygame.init()
assets_dir = "assets"
files = ["idle.png", "walk_1.png", "walk_2.png", "sit_1.png", "sit_2.png", "poop_1.png", "poop_2.png", "poop_3.png", "poop_4.png"]

for f in files:
    path = os.path.join(assets_dir, f)
    if os.path.exists(path):
        try:
            img = pygame.image.load(path)
            print(f"{f}: {img.get_width()}x{img.get_height()}")
        except Exception as e:
            print(f"{f}: Error loading - {e}")
    else:
        print(f"{f}: Not found")
pygame.quit()

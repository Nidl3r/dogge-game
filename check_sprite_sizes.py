import pygame
import os

pygame.init()

ASSETS_DIR = "assets"

print("Checking dog sprite sizes...\n")

# Check idle sprite
path = os.path.join(ASSETS_DIR, "processed_idle.png")
if os.path.exists(path):
    img = pygame.image.load(path)
    print(f"Dog idle sprite: {img.get_width()}x{img.get_height()}")

# Check walk sprite
path = os.path.join(ASSETS_DIR, "processed_walk_1.png")
if os.path.exists(path):
    img = pygame.image.load(path)
    print(f"Dog walk sprite: {img.get_width()}x{img.get_height()}")

# Check portal sprite  
path = os.path.join(ASSETS_DIR, "portal_in_1.png")
if os.path.exists(path):
    img = pygame.image.load(path)
    print(f"Portal (original): {img.get_width()}x{img.get_height()}")

print(f"\nPET_WIDTH x PET_HEIGHT constants: 120x120")

pygame.quit()

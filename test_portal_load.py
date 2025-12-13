import pygame
import os

pygame.init()

ASSETS_DIR = "assets"

print("Testing portal image loading...\n")

for i in range(1, 5):
    path = os.path.join(ASSETS_DIR, f"portal_out_{i}.png")
    print(f"Loading {path}...")
    if os.path.exists(path):
        try:
            img = pygame.image.load(path)
            print(f"  ✓ Loaded successfully")
            print(f"  Size: {img.get_width()}x{img.get_height()}")
            print(f"  Has alpha: {img.get_flags() & pygame.SRCALPHA}")
            print(f"  Bits per pixel: {img.get_bitsize()}")
        except Exception as e:
            print(f"  ✗ Error: {e}")
    else:
        print(f"  ✗ File not found!")
    print()

for i in range(1, 6):
    path = os.path.join(ASSETS_DIR, f"portal_in_{i}.png")
    print(f"Loading {path}...")
    if os.path.exists(path):
        try:
            img = pygame.image.load(path)
            print(f"  ✓ Loaded successfully")
            print(f"  Size: {img.get_width()}x{img.get_height()}")
            print(f"  Has alpha: {img.get_flags() & pygame.SRCALPHA}")
            print(f"  Bits per pixel: {img.get_bitsize()}")
        except Exception as e:
            print(f"  ✗ Error: {e}")
    else:
        print(f"  ✗ File not found!")
    print()

pygame.quit()

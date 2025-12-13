import pygame
import os

img_path = r"C:/Users/HullingerLandon/.gemini/antigravity/brain/cc198623-47eb-48ec-bbd0-86036398463b/uploaded_image_1765589543621.png"

pygame.init()
try:
    img = pygame.image.load(img_path)
    print(f"Size: {img.get_size()}")
    print(f"Flags: {img.get_flags()}")
    print(f"Alpha: {img.get_alpha()}")
    print(f"Color key: {img.get_colorkey()}")
    
    # Check top-left pixel
    p = img.get_at((0, 0))
    print(f"Top-left pixel: {p}")
    
    # Check a few random pixels to see if we have alpha
    has_transparency = False
    for x in range(0, img.get_width(), 10):
        for y in range(0, img.get_height(), 10):
            if img.get_at((x, y))[3] == 0:
                has_transparency = True
                break
    print(f"Has transparent pixels: {has_transparency}")
    
except Exception as e:
    print(f"Error: {e}")

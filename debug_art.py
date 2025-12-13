import schnauzer_art
import pygame

def inspect():
    print(f"GRID_SIZE: {schnauzer_art.GRID_SIZE}")
    print(f"Total Frames: {len(schnauzer_art.FRAMES)}")
    
    if not schnauzer_art.FRAMES:
        print("ERROR: No frames found!")
        return

    # Inspect first frame
    first_key = list(schnauzer_art.FRAMES.keys())[0]
    pixels = schnauzer_art.FRAMES[first_key]
    
    print(f"\nFrame '{first_key}':")
    print(f"  Pixel Count: {len(pixels)}")
    
    if not pixels:
        print("  ERROR: Frame has no pixels!")
        return
        
    # Bounding box
    xs = [p[0] for p in pixels]
    ys = [p[1] for p in pixels]
    print(f"  X Range: {min(xs)} - {max(xs)}")
    print(f"  Y Range: {min(ys)} - {max(ys)}")
    
    # Check colors
    colors = set([p[2] for p in pixels])
    print(f"  Unique Colors: {len(colors)}")
    print(f"  Sample Colors: {list(colors)[:5]}")

if __name__ == "__main__":
    try:
        inspect()
    except Exception as e:
        print(f"Error inspecting art: {e}")

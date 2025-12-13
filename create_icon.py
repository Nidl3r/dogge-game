"""
Create .ico icon file from dog sprite for executable icons
"""
from PIL import Image
import os

# Load the idle dog sprite
assets_dir = "assets"
sprite_path = os.path.join(assets_dir, "processed_idle.png")

try:
    # Load the image
    img = Image.open(sprite_path)
    
    # Convert to RGBA if needed
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    # Create icon with multiple sizes (standard Windows icon sizes)
    icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    
    # Save as .ico file
    output_path = "dog_icon.ico"
    img.save(output_path, format='ICO', sizes=icon_sizes)
    
    print(f"✓ Created {output_path} successfully!")
    print(f"  Icon includes sizes: {', '.join([f'{w}x{h}' for w, h in icon_sizes])}")
    
except Exception as e:
    print(f"✗ Error creating icon: {e}")

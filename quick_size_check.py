from PIL import Image
import os

assets = "assets"

# Check dog sprite
dog_img = Image.open(os.path.join(assets, "processed_idle.png"))
print(f"Dog sprite size: {dog_img.size}")

# Check portal
portal_img = Image.open(os.path.join(assets, "portal_in_1.png"))
print(f"Portal original size: {portal_img.size}")

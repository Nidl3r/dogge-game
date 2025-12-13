"""
Build script for creating standalone Schnauzer Pet executable
Uses PyInstaller to bundle Python, pygame, and all dependencies
"""

import subprocess
import sys
import os
import shutil

# Get paths
VENV_PYTHON = os.path.join("venv", "Scripts", "python.exe")
VENV_PYINSTALLER = os.path.join("venv", "Scripts", "pyinstaller.exe")

def clean_build():
    """Remove previous build artifacts"""
    print("Cleaning previous builds...")
    dirs_to_remove = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"   Removed {dir_name}/")
    
    # Remove spec file
    if os.path.exists("SchnauzerPet.spec"):
        os.remove("SchnauzerPet.spec")
        print("   Removed SchnauzerPet.spec")

def build_executable():
    """Build the standalone executable"""
    print("\nBuilding standalone executable...")
    print("   This may take a few minutes...\n")
    
    # PyInstaller command
    cmd = [
        VENV_PYINSTALLER,
        "--name=SchnauzerPet",
        "--windowed",  # No console window
        "--onedir",  # Single folder (easier to manage assets)
        "--add-data=assets;assets",  # Include assets folder
        "--add-data=schnauzer_art.py;.",  # Include sprite data
        "--add-data=schnauzer_settings.json;.",  # Include default settings
        "--hidden-import=pygame",  # Ensure pygame is included
        "--hidden-import=tkinter",  # Ensure tkinter is included
        "--noconfirm",  # Overwrite without asking
        "launcher_gui.py"  # Entry point
    ]
    
    # Run PyInstaller
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("[SUCCESS] Build successful!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Build failed!")
        print(f"Error: {e.stderr}")
        return False

def create_readme():
    """Create a simple README for distribution"""
    readme_content = """
# 🐕 Schnauzer Desktop Pet

Your adorable desktop companion!

## How to Run

1. **Double-click** `SchnauzerPet.exe`
2. Click "Launch Schnauzer Pet" in the window that appears
3. Enjoy your new desktop friend! 🎉

## What Can It Do?

- **Click the dog** to see tricks (backflip, sit, poop)
- **Right-click the dog** to add more dogs or edit zones
- **Press ESC** on the dog to close it

## Controls

From the launcher window:
- 🚀 Launch Schnauzer Pet - Start your first dog
- ➕ Add Another Dog - Get more dogs
- 📍 Edit Walking Zones - Choose where dogs can walk

## Tips

💡 You can have multiple dogs running at once!
💡 Use the zone editor to control where dogs appear
💡 Dogs will randomly walk, sit, and do tricks

---
Made with ❤️ | No installation required!
"""
    
    dist_readme = os.path.join("dist", "SchnauzerPet", "README.txt")
    with open(dist_readme, 'w') as f:
        f.write(readme_content.strip())
    print("Created README.txt in dist folder")

def main():
    print("=" * 60)
    print("  SCHNAUZER PET - STANDALONE EXECUTABLE BUILDER")
    print("=" * 60)
    
    # Check if venv exists
    if not os.path.exists(VENV_PYTHON):
        print("[ERROR] Virtual environment not found!")
        print("   Please run this from the schnauzer_pet directory")
        return 1
    
    # Check if PyInstaller is installed
    if not os.path.exists(VENV_PYINSTALLER):
        print("[ERROR] PyInstaller not found in venv!")
        print("   Installing PyInstaller...")
        subprocess.run([VENV_PYTHON, "-m", "pip", "install", "pyinstaller"], check=True)
    
    # Clean previous builds
    clean_build()
    
    # Build executable
    if not build_executable():
        return 1
    
    # Create README
    create_readme()
    
    print("\n" + "=" * 60)
    print("BUILD COMPLETE!")
    print("=" * 60)
    print("\nYour standalone application is ready in:")
    print(f"   dist\\SchnauzerPet\\")
    print("\nTo distribute:")
    print("   1. Zip the entire 'SchnauzerPet' folder")
    print("   2. Share the ZIP file via email or cloud storage")
    print("   3. Users extract and double-click SchnauzerPet.exe")
    print("\nNo Python installation needed!")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

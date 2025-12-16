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
    print("\nBuilding executables...")
    print("   This may take a few minutes...\n")

    # 1. Build Dog Instance (single file)
    print("   [1/2] Building Dog Instance...")
    cmd_dog = [
        VENV_PYINSTALLER,
        "--name=DogInstance",
        "--noconsole",
        "--onefile", 
        "--add-data=assets;assets",
        "--add-data=schnauzer_art.py;.",
        "--add-data=schnauzer_settings.json;.",
        "--hidden-import=pygame",
        "--noconfirm",
        "--icon=dog_icon.ico",
        "dog_instance.py"
    ]
    
    try:
        subprocess.run(cmd_dog, check=True, capture_output=True, text=True)
        print("         Dog Instance built successfully.")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Dog Instance build failed!")
        print(f"Error: {e.stderr}")
        return False

    # 2. Build Launcher (directory)
    print("   [2/2] Building Launcher...")
    cmd_launcher = [
        VENV_PYINSTALLER,
        "--name=SchnauzerPet",
        "--windowed",
        "--onedir", 
        "--add-data=assets;assets",
        "--add-data=schnauzer_art.py;.",
        "--add-data=schnauzer_settings.json;.",
        "--hidden-import=pygame",
        "--hidden-import=tkinter",
        "--noconfirm",
        "--icon=dog_icon.ico",
        "launcher_gui.py"
    ]
    
    try:
        subprocess.run(cmd_launcher, check=True, capture_output=True, text=True)
        print("         Launcher built successfully.")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Launcher build failed!")
        print(f"Error: {e.stderr}")
        return False
        
    # 3. Move DogInstance.exe to SchnauzerPet folder
    print("   Finalizing...")
    try:
        src = os.path.join("dist", "DogInstance.exe")
        dst = os.path.join("dist", "SchnauzerPet", "DogInstance.exe")
        
        # Check if src exists (it might be in dist/DogInstance if not onefile, but we used --onefile)
        if os.path.exists(src):
            shutil.move(src, dst)
            print(f"         Moved DogInstance.exe to distribution folder.")
        else:
            print(f"[ERROR] Could not find {src} to move!")
            return False
            
        print("[SUCCESS] Build successful!")
        return True
    except Exception as e:
         print(f"[ERROR] Failed to move executable: {e}")
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
    with open(dist_readme, 'w', encoding='utf-8') as f:
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

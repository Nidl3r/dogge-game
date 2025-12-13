"""
Schnauzer Desktop Pet Launcher
A gift for your brother - launches schnauzer desktop pets!

Each dog runs in its own process so you can have multiple dogs.

Right-click on any dog to see context menu with option to add more dogs.
"""

import subprocess
import sys
import os
import time

DOG_INSTANCE_SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dog_instance.py")
PYTHON_EXE = sys.executable


def main():
    print("="*50)
    print("  SCHNAUZER DESKTOP PET LAUNCHER")
    print("="*50)
    print("  Starting first dog...")
    print("  Right-click on dog for context menu")
    print("  to add more dogs or edit zones!")
    print("="*50)
    
    # Start the first dog
    subprocess.Popen([PYTHON_EXE, DOG_INSTANCE_SCRIPT], creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0)
    
    print("\\nFirst dog launched!")
    print("To add more dogs, right-click on the dog and select 'Add Another Dog'")
    print("Press Ctrl+C to stop the launcher (dogs will continue running)")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\\nLauncher stopped. Dogs are still running.")
        print("To close all dogs, press ESC on each dog window.")


if __name__ == "__main__":
    main()

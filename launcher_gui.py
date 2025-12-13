"""
Schnauzer Desktop Pet - GUI Launcher
User-friendly launcher for non-technical users
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import os
import json

# Check for pygame dependency
def check_pygame():
    """Check if pygame is installed"""
    try:
        import pygame
        return True
    except ImportError:
        return False

def install_pygame():
    """Install pygame using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
        return True
    except:
        return False

# Paths
DOG_INSTANCE_SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dog_instance.py")
SETTINGS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "schnauzer_settings.json")

# Determine which Python executable to use (prefer venv)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
VENV_PYTHON = os.path.join(SCRIPT_DIR, "venv", "Scripts", "python.exe")
if os.path.exists(VENV_PYTHON):
    PYTHON_EXE = VENV_PYTHON
else:
    PYTHON_EXE = sys.executable


class SchnauzerLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("🐕 Schnauzer Desktop Pet")
        self.root.geometry("500x650")
        self.root.resizable(False, False)
        
        # Configure colors
        self.bg_color = "#f0f4f8"
        self.primary_color = "#4a90e2"
        self.success_color = "#52c41a"
        self.warning_color = "#fa8c16"
        
        self.root.configure(bg=self.bg_color)
        
        # Track running dog processes
        self.dog_processes = []
        
        # Load settings
        self.settings = self.load_settings()
        
        # Build UI
        self.create_ui()
        
        # Center window
        self.center_window()
    
    def load_settings(self):
        """Load settings from file"""
        default = {
            'zones': [[50, 500, 800, 60], [1000, 1800, 800, 60]],
            'stay_on_top': True
        }
        try:
            if os.path.exists(SETTINGS_FILE):
                with open(SETTINGS_FILE, 'r') as f:
                    return json.load(f)
        except:
            pass
        return default
    
    def save_settings(self):
        """Save settings to file"""
        try:
            with open(SETTINGS_FILE, 'w') as f:
                json.dump(self.settings, f, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {e}")
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_ui(self):
        """Create the user interface"""
        
        # Header
        header_frame = tk.Frame(self.root, bg="#4a90e2", height=120)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="🐕 Schnauzer Desktop Pet",
            font=("Arial", 24, "bold"),
            bg="#4a90e2",
            fg="white"
        )
        title_label.pack(pady=20)
        
        subtitle_label = tk.Label(
            header_frame,
            text="Your adorable desktop companion!",
            font=("Arial", 11),
            bg="#4a90e2",
            fg="#e6f7ff"
        )
        subtitle_label.pack()
        
        # Main content area
        content_frame = tk.Frame(self.root, bg=self.bg_color)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # Quick Start Section
        quick_start_label = tk.Label(
            content_frame,
            text="Quick Start",
            font=("Arial", 14, "bold"),
            bg=self.bg_color,
            fg="#262626"
        )
        quick_start_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Large Launch Button
        self.launch_btn = tk.Button(
            content_frame,
            text="🚀 Launch Schnauzer Pet",
            font=("Arial", 16, "bold"),
            bg=self.success_color,
            fg="white",
            activebackground="#73d13d",
            activeforeground="white",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.launch_dog,
            height=2
        )
        self.launch_btn.pack(fill=tk.X, pady=(0, 15))
        
        # Add Another Dog Button
        self.add_dog_btn = tk.Button(
            content_frame,
            text="➕ Add Another Dog",
            font=("Arial", 12, "bold"),
            bg=self.primary_color,
            fg="white",
            activebackground="#69b1ff",
            activeforeground="white",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.add_dog,
            height=2
        )
        self.add_dog_btn.pack(fill=tk.X, pady=(0, 20))
        
        # Separator
        separator = ttk.Separator(content_frame, orient='horizontal')
        separator.pack(fill=tk.X, pady=10)
        
        # Settings Section
        settings_label = tk.Label(
            content_frame,
            text="Settings",
            font=("Arial", 14, "bold"),
            bg=self.bg_color,
            fg="#262626"
        )
        settings_label.pack(anchor=tk.W, pady=(10, 10))
        
        # Zone Editor Button
        zone_btn = tk.Button(
            content_frame,
            text="📍 Edit Walking Zones",
            font=("Arial", 11),
            bg="#ffffff",
            fg="#262626",
            activebackground="#f0f0f0",
            relief=tk.SOLID,
            borderwidth=1,
            cursor="hand2",
            command=self.open_zone_editor,
            height=2
        )
        zone_btn.pack(fill=tk.X, pady=(0, 10))
        
        # Always on Top Toggle
        self.always_on_top_var = tk.BooleanVar(value=self.settings.get('stay_on_top', True))
        
        toggle_frame = tk.Frame(content_frame, bg=self.bg_color)
        toggle_frame.pack(fill=tk.X, pady=(0, 20))
        
        toggle_check = tk.Checkbutton(
            toggle_frame,
            text="Keep dogs always on top of other windows",
            variable=self.always_on_top_var,
            font=("Arial", 10),
            bg=self.bg_color,
            activebackground=self.bg_color,
            command=self.toggle_always_on_top
        )
        toggle_check.pack(anchor=tk.W)
        
        # Separator
        separator2 = ttk.Separator(content_frame, orient='horizontal')
        separator2.pack(fill=tk.X, pady=10)
        
        # Help Section
        help_label = tk.Label(
            content_frame,
            text="How to Use",
            font=("Arial", 14, "bold"),
            bg=self.bg_color,
            fg="#262626"
        )
        help_label.pack(anchor=tk.W, pady=(10, 10))
        
        help_text = """• Left-click on dog to make it do tricks!
• Right-click on dog for options menu
• Press ESC on dog window to close it
• Use "Edit Walking Zones" to set where dogs can walk"""
        
        help_content = tk.Label(
            content_frame,
            text=help_text,
            font=("Arial", 10),
            bg=self.bg_color,
            fg="#595959",
            justify=tk.LEFT
        )
        help_content.pack(anchor=tk.W, pady=(0, 10))
        
        # Footer
        footer_frame = tk.Frame(self.root, bg="#f0f0f0", height=50)
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X)
        footer_frame.pack_propagate(False)
        
        footer_label = tk.Label(
            footer_frame,
            text="Made with ❤️ | Enjoy your desktop pet!",
            font=("Arial", 9),
            bg="#f0f0f0",
            fg="#8c8c8c"
        )
        footer_label.pack(expand=True)
    
    def launch_dog(self):
        """Launch the first schnauzer pet"""
        # Check for pygame first
        if not check_pygame():
            response = messagebox.askyesno(
                "Missing Dependency",
                "pygame is required but not installed.\n\n"
                "Would you like to install it now?\n"
                "(This will take about 30 seconds)"
            )
            if response:
                messagebox.showinfo("Installing", "Installing pygame...\nPlease wait.")
                if install_pygame():
                    messagebox.showinfo("Success!", "pygame installed successfully!\nYou can now launch dogs.")
                else:
                    messagebox.showerror(
                        "Installation Failed",
                        "Could not install pygame automatically.\n\n"
                        "Please open Command Prompt and run:\n"
                        "pip install pygame"
                    )
                    return
            else:
                messagebox.showinfo(
                    "Cannot Launch",
                    "pygame is required to run the desktop pet.\n\n"
                    "Please install it by opening Command Prompt and typing:\n"
                    "pip install pygame"
                )
                return
        
        try:
            # Start dog process
            process = subprocess.Popen(
                [PYTHON_EXE, DOG_INSTANCE_SCRIPT],
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            self.dog_processes.append(process)
            
            # Update button text
            self.launch_btn.config(
                text="✅ Dog Launched!",
                bg="#95de64"
            )
            
            # Reset button after 2 seconds
            self.root.after(2000, self.reset_launch_button)
            
            messagebox.showinfo(
                "Success!",
                "Your schnauzer is now running on your desktop!\n\n"
                "• Click on it to see tricks\n"
                "• Right-click for more options\n"
                "• Press ESC to close it"
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch dog: {e}")
    
    def reset_launch_button(self):
        """Reset launch button to original state"""
        self.launch_btn.config(
            text="🚀 Launch Another Dog",
            bg=self.success_color
        )
    
    def add_dog(self):
        """Add another dog to the desktop"""
        # Check for pygame first
        if not check_pygame():
            messagebox.showerror(
                "Missing Dependency",
                "pygame is required but not installed.\n\n"
                "Please use the 'Launch Schnauzer Pet' button first."
            )
            return
        
        try:
            process = subprocess.Popen(
                [PYTHON_EXE, DOG_INSTANCE_SCRIPT],
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            self.dog_processes.append(process)
            
            messagebox.showinfo(
                "Dog Added!",
                "Another schnauzer has joined the party! 🎉"
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add dog: {e}")
    
    def open_zone_editor(self):
        """Open the zone editor"""
        try:
            # Import here to avoid circular dependencies
            import dog_instance
            
            # Close this window temporarily
            self.root.withdraw()
            
            # Open zone editor
            editor = dog_instance.ZoneEditor(
                self.settings.get('zones', []),
                self.settings.get('stay_on_top', True)
            )
            
            result = editor.run()
            
            # Show window again
            self.root.deiconify()
            
            if result is not None:
                # Save zones
                self.settings['zones'] = result
                self.save_settings()
                
                messagebox.showinfo(
                    "Zones Saved!",
                    "Walking zones have been updated.\n"
                    "New dogs will use these zones.\n"
                    "Existing dogs will update automatically."
                )
            
        except Exception as e:
            self.root.deiconify()
            messagebox.showerror("Error", f"Failed to open zone editor: {e}")
    
    def toggle_always_on_top(self):
        """Toggle always on top setting"""
        self.settings['stay_on_top'] = self.always_on_top_var.get()
        self.save_settings()
        
        status = "enabled" if self.always_on_top_var.get() else "disabled"
        messagebox.showinfo(
            "Setting Updated",
            f"'Always on top' has been {status}.\n"
            "This will apply to newly launched dogs."
        )


def main():
    """Main entry point"""
    root = tk.Tk()
    app = SchnauzerLauncher(root)
    root.mainloop()


if __name__ == "__main__":
    main()

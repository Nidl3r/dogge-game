"""
Single dog instance - spawned as separate process
"""
import pygame
import sys
import os
import random
import math
import json
import subprocess

# Initialize pygame
pygame.init()

# Get screen dimensions
screen_info = pygame.display.Info()
SCREEN_WIDTH = screen_info.current_w
SCREEN_HEIGHT = screen_info.current_h

# Pet settings
PET_WIDTH = 120
PET_HEIGHT = 120
TASKBAR_HEIGHT = 60
GROUND_Y = SCREEN_HEIGHT - PET_HEIGHT - TASKBAR_HEIGHT

# Colors
TRANSPARENT = (255, 0, 255)
BROWN = (101, 67, 33)
WHITE = (255, 255, 255)

# Settings file path
SETTINGS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "schnauzer_settings.json")
DOG_INSTANCE_SCRIPT = os.path.abspath(__file__)
PYTHON_EXE = sys.executable


class SchauzerSprites:
    """Generate pixel art schnauzer sprites"""
    
    _frame_cache = {}
    ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")

    @staticmethod
    def get_disk_frame(name):
        """Load processed frame from disk"""
        if name not in SchauzerSprites._frame_cache:
            path = os.path.join(SchauzerSprites.ASSETS_DIR, f"processed_{name}.png")
            try:
                img = pygame.image.load(path)
                SchauzerSprites._frame_cache[name] = img
            except Exception as e:
                print(f"Error loading {name}: {e}")
                s = pygame.Surface((PET_WIDTH, PET_HEIGHT), pygame.SRCALPHA)
                s.fill((0,0,0,0))
                SchauzerSprites._frame_cache[name] = s
        return SchauzerSprites._frame_cache[name]

    @staticmethod
    def create_idle_frames():
        return [SchauzerSprites.get_disk_frame('idle')]
    
    @staticmethod
    def create_walk_frames():
        return [
            SchauzerSprites.get_disk_frame('walk_1'),
            SchauzerSprites.get_disk_frame('walk_2'),
            SchauzerSprites.get_disk_frame('walk_3'),
            SchauzerSprites.get_disk_frame('walk_4'),
            SchauzerSprites.get_disk_frame('walk_5'),
            SchauzerSprites.get_disk_frame('walk_6'),
            SchauzerSprites.get_disk_frame('walk_7')
        ]
    
    @staticmethod
    def create_sit_frames():
        f1 = SchauzerSprites.get_disk_frame('sit_1')
        f2 = SchauzerSprites.get_disk_frame('sit_2')
        return [f1, f2, f2, f2, f2, f2, f2, f1]

    @staticmethod
    def create_backflip_frames():
        frames = []
        base = SchauzerSprites.get_disk_frame('idle')
        num_frames = 12
        
        for i in range(num_frames):
            surf = pygame.Surface((PET_WIDTH, PET_HEIGHT), pygame.SRCALPHA)
            surf.fill(TRANSPARENT)
            
            angle = (i / num_frames) * 360
            rotated = pygame.transform.rotate(base, angle)
            hop_offset = -abs(math.sin(math.radians(angle))) * 30
            
            rect = rotated.get_rect(center=(PET_WIDTH//2, PET_HEIGHT//2))
            rect.y += int(hop_offset)
            
            surf.blit(rotated, rect)
            frames.append(surf)
        
        return frames
    
    @staticmethod
    def create_poop_frames():
        return [
            SchauzerSprites.get_disk_frame('poop_1'),
            SchauzerSprites.get_disk_frame('poop_2'),
            SchauzerSprites.get_disk_frame('poop_2'),
            SchauzerSprites.get_disk_frame('poop_2'),
            SchauzerSprites.get_disk_frame('poop_3'),
            SchauzerSprites.get_disk_frame('poop_4')
        ]
    
    @staticmethod
    def create_portal_out_frames():
        """Portal out animation"""
        dog_idle = SchauzerSprites.get_disk_frame('idle')
        dog_width = dog_idle.get_width()
        dog_height = dog_idle.get_height()
        
        frame_images = []
        for i in range(1, 14):
            path = os.path.join(SchauzerSprites.ASSETS_DIR, f"portal out {i}.png")
            try:
                portal_img = pygame.image.load(path).convert_alpha()
                scaled_width = dog_width
                scaled_height = dog_height
                scaled_portal = pygame.transform.scale(portal_img, (scaled_width, scaled_height))
                
                composite = pygame.Surface((dog_width, dog_height), pygame.SRCALPHA)
                
                if i <= 3:
                    composite.blit(dog_idle, (0, 0))
                
                portal_x = (dog_width - scaled_width) // 2
                portal_y = (dog_height - scaled_height) // 2
                composite.blit(scaled_portal, (portal_x, portal_y))
                
                if i <= 3:
                    composite.blit(dog_idle, (0, 0))
                
                frame_images.append(composite)
            except Exception as e:
                print(f"Error loading portal out {i}: {e}")
        
        return frame_images if frame_images else [pygame.Surface((PET_WIDTH, PET_HEIGHT), pygame.SRCALPHA)]
    
    @staticmethod
    def create_portal_in_frames():
        """Portal in animation"""
        dog_idle = SchauzerSprites.get_disk_frame('idle')
        dog_width = dog_idle.get_width()
        dog_height = dog_idle.get_height()
        
        frames = []
        for i in range(1, 4):
            path = os.path.join(SchauzerSprites.ASSETS_DIR, f"portal_in_{i}.png")
            try:
                portal_img = pygame.image.load(path).convert_alpha()
                scaled_width = dog_width
                scaled_height = dog_height
                scaled_portal = pygame.transform.scale(portal_img, (scaled_width, scaled_height))
                
                composite = pygame.Surface((dog_width, dog_height), pygame.SRCALPHA)
                composite.blit(dog_idle, (0, 0))
                
                portal_x = (dog_width - scaled_width) // 2
                portal_y = (dog_height - scaled_height) // 2
                composite.blit(scaled_portal, (portal_x, portal_y))
                composite.blit(dog_idle, (0, 0))
                
                frames.append(composite)
            except Exception as e:
                print(f"Error loading portal_in_{i}: {e}")
        return frames if frames else [pygame.Surface((PET_WIDTH, PET_HEIGHT), pygame.SRCALPHA)]


def load_settings():
    """Load settings from file"""
    default = {
        'zones': [[50, 500, GROUND_Y, 60], [SCREEN_WIDTH - 500, SCREEN_WIDTH - 50, GROUND_Y, 60]],
        'stay_on_top': True
    }
    try:
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r') as f:
                data = json.load(f)
                if 'zones' in data and len(data['zones']) > 0:
                    if 'stay_on_top' not in data:
                        data['stay_on_top'] = True
                    return data
    except:
        pass
    return default


def save_settings(settings):
    """Save settings to file"""
    try:
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(settings, f)
    except:
        pass


class ZoneEditor:
    """Full-screen overlay for editing visible zones"""
    
    def __init__(self, zones, stay_on_top=True):
        # Create fullscreen window
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
        pygame.display.set_caption("Zone Editor")
        
        # Copy and validate zones
        self.zones = []
        for z in zones:
            if len(z) >= 2 and z[0] < z[1] and z[0] >= 0 and z[1] <= SCREEN_WIDTH:
                if len(z) >= 4:
                    self.zones.append([int(z[0]), int(z[1]), int(z[2]), int(z[3])])
                else:
                    self.zones.append([int(z[0]), int(z[1]), GROUND_Y, 60])
        
        if not self.zones:
            self.zones = [[100, 600, GROUND_Y, 60]]
        
        self.dragging = None
        self.hover = None
        self.drag_offset = 0
        self.running = True
        self.stay_on_top = stay_on_top
        self.result = None  # Will store 'save', 'add_dog', or None
        self.handle_width = 20
        
        # Make window topmost
        try:
            import ctypes
            hwnd = pygame.display.get_wm_info()['window']
            
            GWL_EXSTYLE = -20
            WS_EX_LAYERED = 0x00080000
            LWA_ALPHA = 0x00000002
            
            style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
            ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style | WS_EX_LAYERED)
            ctypes.windll.user32.SetLayeredWindowAttributes(hwnd, 0, 180, LWA_ALPHA)
            
            HWND_TOPMOST = -1
            SWP_NOMOVE = 0x0002
            SWP_NOSIZE = 0x0001
            ctypes.windll.user32.SetWindowPos(hwnd, HWND_TOPMOST, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE)
        except:
            pass
        
        self.font = pygame.font.SysFont('Arial', 16)
        self.title_font = pygame.font.SysFont('Arial', 24, bold=True)
        
        # Buttons
        self.save_btn = pygame.Rect(SCREEN_WIDTH//2 - 180, 100, 100, 40)
        self.cancel_btn = pygame.Rect(SCREEN_WIDTH//2 + 80, 100, 100, 40)
        self.add_zone_btn = pygame.Rect(SCREEN_WIDTH//2 - 60, 150, 120, 35)
        self.add_dog_btn = pygame.Rect(SCREEN_WIDTH//2 - 100, 200, 200, 45)  # New button
    
    def get_handle_rects(self, zone_idx):
        """Get the draggable handle rectangles for a zone"""
        zone = self.zones[zone_idx]
        x1, x2, y, height = zone[0], zone[1], zone[2], zone[3]
        
        left_handle = pygame.Rect(x1 - self.handle_width//2, y, self.handle_width, height)
        right_handle = pygame.Rect(x2 - self.handle_width//2, y, self.handle_width, height)
        delete_btn = pygame.Rect(x1 + (x2 - x1)//2 - 10, y + 5, 20, 20)
        
        return left_handle, right_handle, delete_btn
    
    def run(self):
        clock = pygame.time.Clock()
        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return None
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        return None
                    elif event.key == pygame.K_RETURN:
                        self.result = 'save'
                        self.running = False
                        return self.zones
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mx, my = event.pos
                        
                        # Check buttons
                        if self.save_btn.collidepoint(mx, my):
                            self.result = 'save'
                            self.running = False
                            return self.zones
                        elif self.cancel_btn.collidepoint(mx, my):
                            self.running = False
                            return None
                        elif self.add_zone_btn.collidepoint(mx, my):
                            new_start = SCREEN_WIDTH // 2 - 200
                            new_end = SCREEN_WIDTH // 2 + 200
                            new_y = SCREEN_HEIGHT // 2 - 30
                            new_height = 60
                            self.zones.append([new_start, new_end, new_y, new_height])
                        elif self.add_dog_btn.collidepoint(mx, my):  # New button handler
                            self.result = 'add_dog'
                            self.running = False
                            return self.zones
                        
                        # Check zone handles
                        for i, zone in enumerate(self.zones):
                            left_h, right_h, delete_btn = self.get_handle_rects(i)
                            zone_body = pygame.Rect(zone[0], zone[2], zone[1] - zone[0], zone[3])
                            
                            if delete_btn.collidepoint(mx, my) and len(self.zones) > 1:
                                self.zones.pop(i)
                                break
                            elif left_h.collidepoint(mx, my):
                                self.dragging = (i, 'left')
                                break
                            elif right_h.collidepoint(mx, my):
                                self.dragging = (i, 'right')
                                break
                            elif zone_body.collidepoint(mx, my):
                                self.dragging = (i, 'body')
                                self.drag_offset = (mx - zone[0], my - zone[2])
                                break
                
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.dragging = None
                
                elif event.type == pygame.MOUSEMOTION:
                    mx, my = event.pos
                    
                    # Update hover state
                    self.hover = None
                    if not self.dragging:
                        for i, zone in enumerate(self.zones):
                            left_h, right_h, delete_btn = self.get_handle_rects(i)
                            zone_body = pygame.Rect(zone[0], zone[2], zone[1] - zone[0], zone[3])
                            
                            if left_h.collidepoint(mx, my):
                                self.hover = (i, 'left')
                                break
                            elif right_h.collidepoint(mx, my):
                                self.hover = (i, 'right')
                                break
                            elif zone_body.collidepoint(mx, my):
                                self.hover = (i, 'body')
                                break
                    
                    if self.dragging:
                        zone_idx, side = self.dragging
                        zone = self.zones[zone_idx]
                        
                        if side == 'left':
                            new_val = max(0, min(mx, zone[1] - 50))
                            zone[0] = new_val
                        elif side == 'right':
                            new_val = min(SCREEN_WIDTH, max(mx, zone[0] + 50))
                            zone[1] = new_val
                        elif side == 'body':
                            zone_width = zone[1] - zone[0]
                            zone_height = zone[3]
                            offset_x, offset_y = self.drag_offset
                            
                            new_x = mx - offset_x
                            new_y = my - offset_y
                            
                            new_x = max(0, min(new_x, SCREEN_WIDTH - zone_width))
                            new_y = max(0, min(new_y, SCREEN_HEIGHT - zone_height))
                            
                            zone[0] = new_x
                            zone[1] = new_x + zone_width
                            zone[2] = new_y
                            zone[3] = zone_height
            
            self.draw()
            clock.tick(60)
        
        return None
    
    def draw(self):
        self.screen.fill((20, 20, 30))
        
        # Draw taskbar reference
        taskbar_rect = pygame.Rect(0, SCREEN_HEIGHT - 60, SCREEN_WIDTH, 60)
        pygame.draw.rect(self.screen, (40, 40, 50), taskbar_rect)
        pygame.draw.rect(self.screen, (100, 100, 100), taskbar_rect, 2)
        
        # Title
        title = self.title_font.render("ZONE EDITOR - Set where the dog can walk", True, WHITE)
        self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 20))
        
        instructions1 = self.font.render("Drag handles to resize | Drag zone to move | Click X to delete", True, (180, 180, 180))
        instructions2 = self.font.render("Green zones = where dog is visible | Place zones anywhere on screen!", True, (120, 220, 120))
        self.screen.blit(instructions1, (SCREEN_WIDTH//2 - instructions1.get_width()//2, 52))
        self.screen.blit(instructions2, (SCREEN_WIDTH//2 - instructions2.get_width()//2, 72))
        
        # Buttons
        pygame.draw.rect(self.screen, (40, 120, 40), self.save_btn, border_radius=5)
        pygame.draw.rect(self.screen, (120, 40, 40), self.cancel_btn, border_radius=5)
        pygame.draw.rect(self.screen, (60, 60, 120), self.add_zone_btn, border_radius=5)
        pygame.draw.rect(self.screen, (120, 80, 200), self.add_dog_btn, border_radius=5)  # Purple button
        
        save_text = self.font.render("SAVE", True, WHITE)
        cancel_text = self.font.render("CANCEL", True, WHITE)
        add_zone_text = self.font.render("+ Add Zone", True, WHITE)
        add_dog_text = self.title_font.render("+ Add Another Dog", True, WHITE)
        
        self.screen.blit(save_text, (self.save_btn.centerx - save_text.get_width()//2, self.save_btn.centery - save_text.get_height()//2))
        self.screen.blit(cancel_text, (self.cancel_btn.centerx - cancel_text.get_width()//2, self.cancel_btn.centery - cancel_text.get_height()//2))
        self.screen.blit(add_zone_text, (self.add_zone_btn.centerx - add_zone_text.get_width()//2, self.add_zone_btn.centery - add_zone_text.get_height()//2))
        self.screen.blit(add_dog_text, (self.add_dog_btn.centerx - add_dog_text.get_width()//2, self.add_dog_btn.centery - add_dog_text.get_height()//2))
        
        # Draw zones
        for i, zone in enumerate(self.zones):
            if len(zone) < 2 or zone[0] >= zone[1]:
                continue
            
            x1, x2, y, height = zone[0], zone[1], zone[2], zone[3]
            zone_width = x2 - x1
            zone_rect = pygame.Rect(x1, y, zone_width, height)
            
            is_active = self.dragging == (i, 'body') or self.hover == (i, 'body')
            zone_color = (60, 140, 60) if is_active else (40, 100, 40)
            border_color = (100, 255, 100) if is_active else (80, 200, 80)
            border_width = 4 if is_active else 3
            
            pygame.draw.rect(self.screen, zone_color, zone_rect)
            pygame.draw.rect(self.screen, border_color, zone_rect, border_width)
            
            # Zone number
            zone_num_text = self.title_font.render(str(i+1), True, (255, 255, 0))
            self.screen.blit(zone_num_text, (x1 + zone_width//2 - 10, y - 30))
            
            # Handles
            left_h, right_h, delete_btn = self.get_handle_rects(i)
            
            is_left_active = self.dragging == (i, 'left') or self.hover == (i, 'left')
            handle_color = (255, 220, 120) if is_left_active else (200, 150, 50)
            pygame.draw.rect(self.screen, handle_color, left_h, border_radius=4)
            pygame.draw.rect(self.screen, WHITE, left_h, 3 if is_left_active else 2, border_radius=4)
            
            is_right_active = self.dragging == (i, 'right') or self.hover == (i, 'right')
            handle_color = (255, 220, 120) if is_right_active else (200, 150, 50)
            pygame.draw.rect(self.screen, handle_color, right_h, border_radius=4)
            pygame.draw.rect(self.screen, WHITE, right_h, 3 if is_right_active else 2, border_radius=4)
            
            # Delete button
            if len(self.zones) > 1:
                pygame.draw.rect(self.screen, (150, 50, 50), delete_btn, border_radius=3)
                x_text = self.font.render("×", True, WHITE)
                self.screen.blit(x_text, (delete_btn.centerx - x_text.get_width()//2, delete_btn.centery - x_text.get_height()//2 - 2))
            
            # Zone label
            label_text = f"Zone {i+1}: x:{x1}-{x2} y:{y} h:{height}"
            label = self.font.render(label_text, True, WHITE)
            label_x = max(x1 + 10, min(x1 + 10, x2 - label.get_width() - 10))
            label_y = y + height // 2 - label.get_height() // 2
            self.screen.blit(label, (label_x, label_y))
        
        pygame.display.flip()



class Dog:
    """Single dog instance"""
    def __init__(self, start_x=None, start_y=None):
        settings = load_settings()
        
        # Visible zones
        zones = settings.get('zones', [[0, 450, GROUND_Y, 60], [SCREEN_WIDTH - 300, SCREEN_WIDTH, GROUND_Y, 60]])
        self.visible_zones = []
        for z in zones:
            if len(z) >= 4:
                self.visible_zones.append(list(z))
            else:
                self.visible_zones.append([z[0], z[1], GROUND_Y, 60])
        
        self.stay_on_top = settings.get('stay_on_top', True)
        
        # Position
        if start_x is None or start_y is None:
            if self.visible_zones:
                first_zone = self.visible_zones[0]
                self.x = first_zone[0] + 50
                if len(first_zone) >= 4:
                    zone_y = first_zone[2]
                    zone_h = first_zone[3]
                    self.y = zone_y + zone_h - PET_HEIGHT
                else:
                    self.y = GROUND_Y + 60 - PET_HEIGHT
            else:
                self.x = 100
                self.y = GROUND_Y
        else:
            self.x = start_x
            self.y = start_y
        
        # Create window
        os.environ['SDL_VIDEO_WINDOW_POS'] = f'{int(self.x)},{int(self.y)}'
        self.screen = pygame.display.set_mode((PET_WIDTH, PET_HEIGHT), pygame.NOFRAME)
        pygame.display.set_caption(f"Schnauzer Pet")
        
        # Set window properties
        try:
            import ctypes
            hwnd = pygame.display.get_wm_info()['window']

            GWL_EXSTYLE = -20
            WS_EX_LAYERED = 0x00080000
            WS_EX_TOOLWINDOW = 0x00000080
            LWA_COLORKEY = 0x00000001

            style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
            style = style | WS_EX_LAYERED | WS_EX_TOOLWINDOW
            ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)

            ctypes.windll.user32.SetLayeredWindowAttributes(
                hwnd,
                0x00FF00FF,
                0,
                LWA_COLORKEY
            )
            
            HWND_TOPMOST = -1
            HWND_NOTOPMOST = -2
            SWP_NOMOVE = 0x0002
            SWP_NOSIZE = 0x0001
            SWP_NOACTIVATE = 0x0010

            if self.stay_on_top:
                ctypes.windll.user32.SetWindowPos(
                    hwnd, HWND_TOPMOST, 0, 0, 0, 0,
                    SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE
                )
            else:
                ctypes.windll.user32.SetWindowPos(
                    hwnd, HWND_NOTOPMOST, 0, 0, 0, 0,
                    SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE
                )
            
            self.hwnd = hwnd
            self.can_move_window = True
        except Exception as e:
            print(f"Compatibility mode: {e}")
            self.can_move_window = False
            self.hwnd = None
        
        # State
        self.state = "idle"
        self.direction = 1
        self.frame = 0
        self.frame_timer = 0
        self.state_timer = 0
        
        # Load animations
        self.animations = {
            'idle': SchauzerSprites.create_idle_frames(),
            'walk': SchauzerSprites.create_walk_frames(),
            'sit': SchauzerSprites.create_sit_frames(),
            'backflip': SchauzerSprites.create_backflip_frames(),
            'poop': SchauzerSprites.create_poop_frames(),
            'portal_out': SchauzerSprites.create_portal_out_frames(),
            'portal_in': SchauzerSprites.create_portal_in_frames(),
        }
        
        self.tricks = ['backflip', 'sit', 'poop']
        self.trick_index = 0
        
        self.teleporting = False
        self.teleport_target_x = None
        self.teleport_target_y = None
        
        self.poops = []
        self.clock = pygame.time.Clock()
        
        # Track settings file modification time for zone sharing
        self.settings_mtime = os.path.getmtime(SETTINGS_FILE) if os.path.exists(SETTINGS_FILE) else 0
        self.zone_check_timer = 0  # Check for zone updates every 2 seconds
    
    def is_in_visible_zone(self):
        for zone in self.visible_zones:
            if len(zone) >= 4:
                zone_start, zone_end, zone_y, zone_height = zone[0], zone[1], zone[2], zone[3]
                x_in_range = zone_start <= self.x <= zone_end - PET_WIDTH
                y_in_range = zone_y <= self.y < zone_y + zone_height
                if x_in_range and y_in_range:
                    return True
            else:
                zone_start, zone_end = zone[0], zone[1]
                if zone_start <= self.x <= zone_end - PET_WIDTH:
                    return True
        return False
    
    def move_window(self, x, y):
        if self.can_move_window and self.hwnd:
            try:
                import ctypes
                SWP_NOSIZE = 0x0001
                SWP_NOZORDER = 0x0004
                SWP_NOACTIVATE = 0x0010
                SWP_ASYNCWINDOWPOS = 0x4000

                if not hasattr(self, '_last_window_pos'):
                    self._last_window_pos = (None, None)

                if (int(x), int(y)) != self._last_window_pos:
                    ctypes.windll.user32.SetWindowPos(
                        self.hwnd,
                        0,
                        int(x),
                        int(y),
                        0,
                        0,
                        SWP_NOSIZE | SWP_NOZORDER | SWP_NOACTIVATE | SWP_ASYNCWINDOWPOS
                    )
                    self._last_window_pos = (int(x), int(y))
            except Exception as e:
                print(f"Error moving window: {e}")
    
    def teleport_to_random_zone(self):
        """Teleport to a random zone"""
        if len(self.visible_zones) <= 1:
            return

        current_zone_idx = None
        for i, zone in enumerate(self.visible_zones):
            if len(zone) >= 4:
                zone_start, zone_end = zone[0], zone[1]
            else:
                zone_start, zone_end = zone[0], zone[1]

            if zone_start <= self.x <= zone_end - PET_WIDTH:
                current_zone_idx = i
                break

        available_zones = [i for i in range(len(self.visible_zones)) if i != current_zone_idx]
        if not available_zones:
            available_zones = list(range(len(self.visible_zones)))

        new_zone_idx = random.choice(available_zones)
        new_zone = self.visible_zones[new_zone_idx]

        if len(new_zone) >= 4:
            zone_start, zone_end, zone_y, zone_height = new_zone[0], new_zone[1], new_zone[2], new_zone[3]
        else:
            zone_start, zone_end = new_zone[0], new_zone[1]
            zone_y = GROUND_Y
            zone_height = 60

        zone_width = zone_end - zone_start - PET_WIDTH
        if zone_width > 100:
            target_x = zone_start + random.randint(50, zone_width - 50)
        else:
            target_x = zone_start + zone_width // 2

        target_y = zone_y + zone_height - PET_HEIGHT

        self.teleporting = True
        self.teleport_target_x = target_x
        self.teleport_target_y = target_y
        self.state = 'portal_out'
        self.frame = 0
        self.frame_timer = 0

    def do_trick(self):
        trick = self.tricks[self.trick_index]
        self.state = trick
        self.frame = 0
        self.frame_timer = 0
        self.trick_index = (self.trick_index + 1) % len(self.tricks)
    
    def spawn_new_dog(self):
        """Spawn a new dog process at a random position"""
        if self.visible_zones:
            zone = random.choice(self.visible_zones)
            if len(zone) >= 4:
                zone_start, zone_end, zone_y, zone_height = zone[0], zone[1], zone[2], zone[3]
            else:
                zone_start, zone_end = zone[0], zone[1]
                zone_y = GROUND_Y
                zone_height = 60
            
            # Random position within zone
            zone_width = zone_end - zone_start - PET_WIDTH
            if zone_width > 100:
                new_x = zone_start + random.randint(50, zone_width - 50)
            else:
                new_x = zone_start + zone_width // 2
            new_y = zone_y + zone_height - PET_HEIGHT
            
            # Spawn new process
            try:
                subprocess.Popen(
                    [PYTHON_EXE, DOG_INSTANCE_SCRIPT, str(new_x), str(new_y)],
                    creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
                )
                print(f"Spawned new dog at ({new_x}, {new_y})")
            except Exception as e:
                print(f"Failed to spawn new dog: {e}")
                
    def update(self, dt):
        # Check for zone updates from other dog instances (every 2 seconds)
        self.zone_check_timer += dt
        if self.zone_check_timer >= 2000:  # Check every 2 seconds
            self.zone_check_timer = 0
            try:
                if os.path.exists(SETTINGS_FILE):
                    current_mtime = os.path.getmtime(SETTINGS_FILE)
                    if current_mtime > self.settings_mtime:
                        # Settings file has been updated, reload zones
                        self.settings_mtime = current_mtime
                        settings = load_settings()
                        new_zones = settings.get('zones', [])
                        if new_zones:
                            # Before updating zones, find which zone the dog is currently in
                            current_zone_index = None
                            relative_x = None
                            relative_y = None
                            
                            # Find the dog's current zone
                            for i, zone in enumerate(self.visible_zones):
                                if len(zone) >= 4:
                                    zone_start, zone_end, zone_y, zone_height = zone[0], zone[1], zone[2], zone[3]
                                else:
                                    zone_start, zone_end = zone[0], zone[1]
                                    zone_y = GROUND_Y
                                    zone_height = 60
                                
                                if zone_start <= self.x <= zone_end - PET_WIDTH:
                                    current_zone_index = i
                                    # Calculate relative position within zone
                                    relative_x = self.x - zone_start
                                    relative_y = self.y - (zone_y + zone_height - PET_HEIGHT)
                                    break
                            
                            # Convert zones to proper format
                            self.visible_zones = []
                            for z in new_zones:
                                if len(z) >= 4:
                                    self.visible_zones.append(list(z))
                                else:
                                    self.visible_zones.append([z[0], z[1], GROUND_Y, 60])
                            
                            # If dog was in a zone, move it to maintain relative position in that zone
                            # Only reposition if dog is not walking (prevents vibration during zone editing)
                            if current_zone_index is not None and current_zone_index < len(self.visible_zones):
                                if self.state != 'walk':  # Only reposition when idle/sitting
                                    new_zone = self.visible_zones[current_zone_index]
                                    if len(new_zone) >= 4:
                                        zone_start, zone_end, zone_y, zone_height = new_zone[0], new_zone[1], new_zone[2], new_zone[3]
                                    else:
                                        zone_start, zone_end = new_zone[0], new_zone[1]
                                        zone_y = GROUND_Y
                                        zone_height = 60
                                    
                                    # Move dog to same relative position in the updated zone
                                    new_x = zone_start + relative_x
                                    new_y = zone_y + zone_height - PET_HEIGHT + relative_y
                                    
                                    # Ensure dog stays within zone bounds
                                    if new_x < zone_start:
                                        new_x = zone_start
                                    elif new_x > zone_end - PET_WIDTH:
                                        new_x = zone_end - PET_WIDTH
                                    
                                    self.x = new_x
                                    self.y = new_y
                                    self.move_window(self.x, self.y)
                            
                            print(f"Zones updated from settings file: {len(self.visible_zones)} zones loaded")
            except Exception as e:
                print(f"Error checking for zone updates: {e}")
        
        self.frame_timer += dt
        self.state_timer += dt
        
        frame_duration = 100 if self.state == 'walk' else 150
        if self.state == 'backflip':
            frame_duration = 50
        elif self.state == 'portal_out':
            frame_duration = 50
        elif self.state == 'portal_in':
            frame_duration = 100
        
        if self.frame_timer >= frame_duration:
            self.frame_timer = 0
            self.frame += 1
            
            frames = self.animations[self.state]
            
            if self.frame >= len(frames):
                if self.state in ['backflip', 'sit', 'poop']:
                    if self.state == 'poop':
                        self.poops.append({
                            'x': self.x + 40,
                            'y': self.y + 52,
                            'timer': 5000
                        })
                    self.state = 'idle'
                    self.state_timer = 0
                elif self.state == 'portal_out':
                    self.x = self.teleport_target_x
                    self.y = self.teleport_target_y
                    self.move_window(self.x, self.y)
                    self.state = 'portal_in'
                    self.frame = 0
                elif self.state == 'portal_in':
                    self.state = 'idle'
                    self.state_timer = 0
                    self.teleporting = False
                    self.teleport_target_x = None
                    self.teleport_target_y = None
                self.frame = 0
        
        if self.state == 'idle':
            if self.state_timer > 2000:
                rand = random.random()
                if rand < 0.02:
                    self.state = 'walk'
                    self.state_timer = 0
                    self.direction = random.choice([-1, 1])
                elif rand < 0.03 and len(self.visible_zones) > 1:
                    self.teleport_to_random_zone()
                    self.state_timer = 0

        elif self.state == 'walk':
            speed = 2
            old_x = self.x
            self.x += speed * self.direction

            in_any_zone = False
            current_zone_y = self.y

            for zone in self.visible_zones:
                if len(zone) >= 4:
                    zone_start, zone_end, zone_y, zone_height = zone[0], zone[1], zone[2], zone[3]
                else:
                    zone_start, zone_end = zone[0], zone[1]
                    zone_y = GROUND_Y
                    zone_height = 60

                if zone_start <= self.x <= zone_end - PET_WIDTH:
                    in_any_zone = True
                    current_zone_y = zone_y + zone_height - PET_HEIGHT
                    break

            self.y = current_zone_y

            if not in_any_zone:
                self.direction *= -1
                self.x = old_x

            if self.x < 0:
                self.direction = 1
                self.x = 0
            elif self.x > SCREEN_WIDTH - PET_WIDTH:
                self.direction = -1
                self.x = SCREEN_WIDTH - PET_WIDTH

            if self.state_timer > 1500 and random.random() < 0.01:
                self.state = 'idle'
                self.state_timer = 0

        if self.state not in ['portal_out', 'portal_in']:
            self.move_window(self.x, self.y)
        
        for poop in self.poops[:]:
            poop['timer'] -= dt
            if poop['timer'] <= 0:
                self.poops.remove(poop)
    
    def draw(self):
        self.screen.fill(TRANSPARENT)

        frames = self.animations[self.state]
        frame_img = frames[self.frame % len(frames)]

        if self.direction == -1 and self.state not in['backflip', 'portal_out', 'portal_in']:
            frame_img = pygame.transform.flip(frame_img, True, False)

        self.screen.blit(frame_img, (0, 0))
        pygame.display.flip()
    
    def run(self):
        running = True
        
        while running:
            dt = self.clock.tick(60)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        if self.state not in ['backflip', 'poop']:
                            self.do_trick()
                    elif event.button == 3:  # Right click - show zone editor
                        #Save current position
                        save_x, save_y = self.x, self.y
                        
                        # Close current display to show editor
                        pygame.display.quit()
                        pygame.display.init()
                        
                        # Show zone editor
                        editor = ZoneEditor(self.visible_zones, self.stay_on_top)
                        result_zones = editor.run()
                        
                        # Check what action was taken
                        if result_zones is not None and editor.result == 'save':
                            # User clicked Save - update zones
                            self.visible_zones = result_zones
                            settings = load_settings()
                            settings['zones'] = result_zones
                            save_settings(settings)
                            print(f"Zones saved: {result_zones}")
                        
                        # Check if user wants to add another dog
                        spawn_dog = (result_zones is not None and editor.result == 'add_dog')
                        
                        # Recreate dog window
                        pygame.display.init()
                        os.environ['SDL_VIDEO_WINDOW_POS'] = f'{int(save_x)},{int(save_y)}'
                        self.screen = pygame.display.set_mode((PET_WIDTH, PET_HEIGHT), pygame.NOFRAME)
                        
                        # Reapply window properties
                        try:
                            import ctypes
                            hwnd = pygame.display.get_wm_info()['window']
                            
                            GWL_EXSTYLE = -20
                            WS_EX_LAYERED = 0x00080000
                            WS_EX_TOOLWINDOW = 0x00000080
                            LWA_COLORKEY = 0x00000001
                            
                            style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
                            style = style | WS_EX_LAYERED | WS_EX_TOOLWINDOW
                            ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
                            
                            ctypes.windll.user32.SetLayeredWindowAttributes(
                                hwnd,
                                0x00FF00FF,
                                0,
                                LWA_COLORKEY
                            )
                            
                            HWND_TOPMOST = -1
                            SWP_NOMOVE = 0x0002
                            SWP_NOSIZE = 0x0001
                            SWP_NOACTIVATE = 0x0010
                            
                            if self.stay_on_top:
                                ctypes.windll.user32.SetWindowPos(
                                    hwnd, HWND_TOPMOST, 0, 0, 0, 0,
                                    SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE
                                )
                            
                            self.hwnd = hwnd
                        except:
                            pass
                        
                        # Handle add dog action after window is recreated
                        if spawn_dog:
                            self.spawn_new_dog()
                            
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            
            self.update(dt)
            self.draw()
        
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    # Get position from command line args if provided
    # Handle both PyInstaller bundle and normal execution
    start_x = None
    start_y = None
    
    try:
        if len(sys.argv) > 1:
            start_x = int(sys.argv[1])
        if len(sys.argv) > 2:
            start_y = int(sys.argv[2])
    except (ValueError, IndexError):
        # Arguments not provided or invalid, use defaults
        pass
    
    dog = Dog(start_x, start_y)
    dog.run()


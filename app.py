import pyautogui
import threading
import time
import random
import math
import ctypes
import ctypes.wintypes
import winsound
from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw, ImageFont
from queue import Queue

# --- 💤 Detect Idle Time ---
def get_idle_duration():
    class LASTINPUTINFO(ctypes.Structure):
        _fields_ = [('cbSize', ctypes.wintypes.UINT),
                    ('dwTime', ctypes.wintypes.DWORD)]
    lii = LASTINPUTINFO()
    lii.cbSize = ctypes.sizeof(lii)
    ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii))
    millis = ctypes.windll.kernel32.GetTickCount() - lii.dwTime
    return millis / 1000.0

# # --- 🎨 Create Tray Icon ---
def create_icon_image(color="green", status_symbol="✔", size=300):
    img = Image.new('RGB', (size, size), color='white')
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, size, size], fill=color)
    try:
        font = ImageFont.truetype("seguiemj.ttf", size=size // 2)
    except IOError:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), status_symbol, font=font)
    symbol_width = bbox[2] - bbox[0]
    symbol_height = bbox[3] - bbox[1]
    symbol_position = ((size - symbol_width) // 2, (size - symbol_height) // 2)
    draw.text(symbol_position, status_symbol, font=font, fill='white')
    return img

# --- 🚫 Sleep Blocker Tray App ---
class SleepSlapperTrayApp:
    def __init__(self):
        self.running_mode = "Stopped"
        self.pattern = "Square"
        self.notifications_enabled = True
        self.simulate_keyboard = False
        self.simulate_click = False
        self.icon = self.create_icon()
        pyautogui.FAILSAFE = True
        self.update_queue = Queue()
    
    def toggle_keyboard(self, icon, item):
        self.simulate_keyboard = not self.simulate_keyboard
        state = "enabled" if self.simulate_keyboard else "disabled"
        print(f"⌨️ Keyboard simulation {state}")
        self.show_balloon("Keyboard Simulation", f"Keyboard input is now {state}.")

    def toggle_mouse_click(self, icon, item):
        self.simulate_click = not self.simulate_click
        state = "enabled" if self.simulate_click else "disabled"
        print(f"🖱️ Mouse click simulation {state}")
        self.show_balloon("Mouse Click Simulation", f"Mouse clicks are now {state}.")

    def create_icon(self):
        image = create_icon_image("green", "✔")
        return Icon("SleepSlapper", image, "SleepSlapper By Manoj", menu=Menu(
            MenuItem("Start (Manual)", lambda icon, item: self.set_mode("Manual")(icon, item), checked=lambda item: self.running_mode == "Manual"),
            MenuItem("AutoDetect", lambda icon, item: self.set_mode("Auto")(icon, item), checked=lambda item: self.running_mode == "Auto"),
            MenuItem("Stop", lambda icon, item: self.set_mode("Stopped")(icon, item), checked=lambda item: self.running_mode == "Stopped"),
            Menu.SEPARATOR,
            MenuItem("Pattern", Menu(
                MenuItem("Square", lambda icon, item: self.set_pattern("Square")(icon, item), checked=lambda item: self.pattern == "Square"),
                MenuItem("Random", lambda icon, item: self.set_pattern("Random")(icon, item), checked=lambda item: self.pattern == "Random"),
                MenuItem("Circle", lambda icon, item: self.set_pattern("Circle")(icon, item), checked=lambda item: self.pattern == "Circle"),
                MenuItem("Triangle", lambda icon, item: self.set_pattern("Triangle")(icon, item), checked=lambda item: self.pattern == "Triangle"),
            )),
            Menu.SEPARATOR,
            MenuItem("Simulate Keyboard Input", self.toggle_keyboard, checked=lambda item: self.simulate_keyboard),
            MenuItem("Simulate Mouse Click", self.toggle_mouse_click, checked=lambda item: self.simulate_click),
            MenuItem("Toggle Notifications and Sound", self.toggle_notifications, checked=lambda item: self.notifications_enabled),
            Menu.SEPARATOR,
            MenuItem("Exit", self.exit)
        ))

    def toggle_notifications(self, icon, item):
        self.notifications_enabled = not self.notifications_enabled
        status = "enabled" if self.notifications_enabled else "disabled"
        print(f"🔔 Notifications and sound have been {status}")

    def show_balloon(self, title, message):
        if self.notifications_enabled:
            print(f"🔔 {title}: {message}")
            self.icon.notify(message, title=title)

    def set_pattern(self, pattern_name):
        def handler(icon, item):
            print(f"🔁 Pattern set to: {pattern_name}")
            self.pattern = pattern_name
        return handler

    def set_mode(self, mode_name):
        def handler(icon, item):
            print(f"🛠 Mode changed to: {mode_name}")
            self.running_mode = mode_name
            if mode_name == "Auto":
                self.show_balloon("AutoDetect Activated", "Mouse movement will start when idle.")
            elif mode_name == "Stopped":
                self.show_balloon("AutoDetect Stopped", "Mouse movement has been disabled.")
            elif mode_name == "Manual":
                self.show_balloon("Manual Mode Activated", "Mouse movement is constant.")
        return handler

    def play_sound(self):
        if self.notifications_enabled:
            print("🔊 Playing sound (Idle detected)")
            # winsound.Beep(1000, 500)

    def move_mouse(self):
        while True:
            try:
                idle_time = get_idle_duration()
                status_symbol = "✔" if idle_time < 60 else "❌"
                color = "green" if idle_time < 60 else "red"
                self.update_icon(color, status_symbol)

                if self.running_mode == "Manual":
                    print("🟢 Manual Mode - Moving Mouse")
                    self.do_movement()
                elif self.running_mode == "Auto":
                    if idle_time >= 60:
                        print("🔴 Auto Mode - Idle detected, moving mouse")
                        self.do_movement()
                        self.play_sound()
                    else:
                        print(f"💤 User is active ({int(idle_time)}s idle) - Waiting")
                time.sleep(random.randint(5, 10))
            except pyautogui.FailSafeException:
                print("🛑 Fail-safe triggered. Stopping...")
                self.running_mode = "Stopped"

    def do_movement(self):
        if self.pattern == "Square":
            self.move_in_square()
        elif self.pattern == "Random":
            dx, dy = random.randint(-5, 5), random.randint(-5, 5)
            pyautogui.moveRel(dx, dy, duration=0.1)
        elif self.pattern == "Circle":
            self.move_in_circle()
        elif self.pattern == "Triangle":
            self.move_in_triangle()

        if self.simulate_keyboard:
            pyautogui.press('shift')
            print("⌨️ Simulated Shift key press")

        if self.simulate_click:
            pyautogui.click()
            print("🖱️ Simulated mouse click")
        

    def move_in_square(self, size=50):
        print("🔷 Moving in Square")
        for _ in range(2):
            pyautogui.moveRel(size, 0, duration=0.1)
            pyautogui.moveRel(0, size, duration=0.1)
            pyautogui.moveRel(-size, 0, duration=0.1)
            pyautogui.moveRel(0, -size, duration=0.1)

    def move_in_circle(self, radius=50, steps=12):
        print("⚪ Moving in Circle")
        for angle in range(0, 360, int(360/steps)):
            x = radius * math.cos(math.radians(angle))
            y = radius * math.sin(math.radians(angle))
            pyautogui.moveRel(x, y, duration=0.05)

    def move_in_triangle(self, size=100):
        print("🔺 Moving in Triangle")
        for angle in [0, 120, 240]:
            x = size * math.cos(math.radians(angle))
            y = size * math.sin(math.radians(angle))
            pyautogui.moveRel(x, y, duration=0.1)

    def update_icon(self, color, status):
        self.update_queue.put((color, status))

    def update_gui(self):
        while not self.update_queue.empty():
            color, status = self.update_queue.get()
            new_icon = create_icon_image(color, status)
            self.icon.icon = new_icon

    def periodic_gui_update(self):
        while True:
            if self.icon.visible:
                self.update_gui()
            time.sleep(1)

    def exit(self, icon, item):
        print("🚪 Exiting application")
        self.running_mode = "Stopped"
        icon.stop()

    def run(self):
        threading.Thread(target=self.move_mouse, daemon=True).start()
        threading.Thread(target=self.periodic_gui_update, daemon=True).start()
        print("🚀 SleepSlapper Tray App started")
        self.icon.run()

if __name__ == "__main__":
    app = SleepSlapperTrayApp()
    app.run()

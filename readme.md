# 💤 SleepSlapper

**SleepSlapper** is a lightweight, tray-based Python app that prevents your system from going idle by simulating mouse movements, keyboard input, or clicks — so your PC stays awake while you doze off 😴 or focus elsewhere 💻.

> ⚙️ Built with Python + PyStray + PyAutoGUI — no intrusive UI, just pure anti-sleep power in your system tray.

---

## 🚀 Features

- ✅ Manual or AutoDetect mode (triggers when you're idle)
- ✅ Multiple movement patterns (Circle, Triangle, Square, Random)
- ✅ System tray icon with live status color (✔ Green = Active, ❌ Red = Idle)
- ✅ Toggle notifications and sounds
- ✅ Lightweight and works silently in the background

---

# 📦 Changelog

All notable changes to **SleepSlapper** will be documented here.

---
## [1.0.0] - 2025-04-10
### Added
- Initial release
- Auto/Manual mode support
- Mouse movement patterns (Random, Square, Circle, Triangle)
- Tray icon with live status

## 🛠 Requirements

Install the required dependencies with:

```bash
pip install -r requirements.txt
```

## 📋 Dependencies

- `pyautogui`
- `pystray`
- `Pillow`
- `winsound` (Windows-only, built-in)
- `ctypes` (built-in)

---

## 🧠 How It Works

**SleepSlapper** checks how long you've been idle (no keyboard or mouse activity):

- **Auto Mode**: Starts moving the mouse when idle > 60s.
- **Manual Mode**: Always keeps your machine active.

The tray icon updates in real time with:

- 🟢 **Green ✔** = Active
- 🔴 **Red ❌** = Idle detected

---

## 🎛 Tray Controls

Right-click the tray icon to access:

- **Start (Manual)**
- **AutoDetect**
- **Stop**
- **Movement Patterns**
- **Toggle Notifications and Sound**
- **Exit**

---

## 🖼 Icon Customization

You can generate a custom emoji-based icon using tools like Adobe Firefly, DALL·E, or any emoji font. The tray icon is dynamically generated via **Pillow (PIL)** with color + symbol (✔ / ❌).

---

## 📦 Build Executable (Optional)

Use **PyInstaller** to create a Windows `.exe`:

```bash
pyinstaller --noconfirm --onefile --windowed app.py
```

You can add a custom icon with:

```bash
--icon=your_icon.ico
```

---

## 👨‍💻 Author

**Manoj** — your friendly developer who doesn’t like his screen going dark 🌙

---

## 📃 License

This project is licensed under the **MIT License**.

Enjoy keeping your screen awake with style! 😎
import tkinter as tk
import sys
import os
import ctypes
from PIL import Image, ImageTk

def blue_screen():
# Für PyInstaller / auto-py-to-exe
    def resource_path(path):
        if hasattr(sys, "_MEIPASS"):
            return os.path.join(sys._MEIPASS, path)
        return path

    root = tk.Tk()

# Vollbild ohne Taskleiste
    root.attributes("-fullscreen", True)
    root.attributes("-topmost", True)
    root.overrideredirect(True)
    root.config(cursor='none')

# Bildschirmgröße
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

# Bild laden
    img = Image.open(resource_path("bsodmaker.png"))
    img = img.resize((screen_width, screen_height))
    photo = ImageTk.PhotoImage(img)

    label = tk.Label(root, image=photo)
    label.pack()

# ---------------- MAUS FREEZE ----------------
    user32 = ctypes.windll.user32
    center_x = screen_width // 2
    center_y = screen_height // 2

    def freeze_mouse():
        user32.SetCursorPos(center_x, center_y)
        root.after(1, freeze_mouse)  # extrem schnell, stabil

    freeze_mouse()
# --------------------------------------------

# Maus & Fokus im Fenster halten
    root.grab_set()

    def disable_close_event(event):
        return "break"

# Tasten
    root.bind("<Control-Shift-KeyPress-F>", lambda e: root.destroy())
    root.bind("<Control-w>", disable_close_event)
    root.bind("<Alt-F4>", disable_close_event)

    root.mainloop()

if __name__ == "__main__":
    blue_screen()

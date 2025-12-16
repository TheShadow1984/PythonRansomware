import tkinter as tk
import sys
import os
from PIL import Image, ImageTk

def resource_path(path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, path)
    return path

root = tk.Tk()

# Vollbild ohne Taskleiste
root.attributes("-fullscreen", True)
root.attributes("-topmost", True)
root.overrideredirect(True)

# Bildschirmgröße ermitteln
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Bild laden und an Bildschirmgröße anpassen
img = Image.open(resource_path("bsodmaker.png"))
img = img.resize((screen_width, screen_height))
photo = ImageTk.PhotoImage(img)

label = tk.Label(root, image=photo)
label.pack()

def disable_close_event(event):
    return "break"

# Tasten
root.bind("<Control-Shift-KeyPress-F>", lambda e: root.destroy())
root.bind("<Control-w>", disable_close_event)
root.bind("<Alt-F4>", disable_close_event)

root.mainloop()

import ctypes
from blue_screen import blue_screen

ctypes.windll.user32.MessageBoxW(
    0,
    "Ein unerwarteter Fehler ist aufgetreten.",
    "Fehler",
    0x10  # Fehler-Icon
)

blue_screen()
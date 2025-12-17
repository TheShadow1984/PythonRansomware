import os
import random

def file_rename(debug=False, path="."):
    files = []

    for name in os.listdir(path):
        full_path = os.path.join(path, name)
        if os.path.isfile(full_path):
            files.append(name)

    for file in files:
        try:
            new_name = f"{random.randint(100000, 999999)}.{random.randint(85719, 1836745986713)}"
            os.rename(
                os.path.join(path, file),
                os.path.join(path, new_name)
            )
        except OSError as e:
            if debug == True:
                print(f"Fehler bei Datei {file}: {e}")

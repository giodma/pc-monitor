import os
import subprocess
import urllib.parse
import requests

TARGET_IP = os.environ["TARGET_IP"]
PHONE = os.environ["PHONE"]
APIKEY = os.environ["APIKEY"]
STATE_FILE = "state.txt"

def ping(ip):
    result = subprocess.run(
        ["ping", "-c", "3", "-W", "2", ip],
        capture_output=True
    )
    return result.returncode == 0

def send_whatsapp(text):
    encoded = urllib.parse.quote(text)
    url = f"https://api.callmebot.com/whatsapp.php?phone={PHONE}&text={encoded}&apikey={APIKEY}"
    try:
        r = requests.get(url, timeout=15)
        print("Risposta CallMeBot:", r.status_code, r.text[:200])
    except Exception as e:
        print("Errore invio WhatsApp:", e)

def read_previous_state():
    if os.path.exists(STATE_FILE):
        return open(STATE_FILE).read().strip()
    return "online"

def write_state(state):
    with open(STATE_FILE, "w") as f:
        f.write(state)

online_now = ping(TARGET_IP)
current_state = "online" if online_now else "offline"
previous_state = read_previous_state()

print(f"Stato precedente: {previous_state} | Stato attuale: {current_state}")

if current_state != previous_state:
    if current_state == "offline":
        send_whatsapp("🔴 Il PC di casa risulta OFFLINE (non raggiungibile su Tailscale).")
    else:
        send_whatsapp("✅ Il PC di casa è tornato ONLINE.")
    write_state(current_state)
else:
    print("Nessun cambio di stato, nessuna notifica inviata.")

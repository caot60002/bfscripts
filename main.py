import requests
import websocket
import json
import time
import threading
import os
import ssl
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

EMAIL = ""
PASSWORD = ""
WEBHOOK_URL = ""
BOT_NAME = "HYPER-HUB HOSTING AFK"
BOT_AVATAR = "https://media.discordapp.net/attachments/1312682558781132831/1468315614744412234/favicon.jpg"

MSG_ID_FILE = "webhook_msg_id.txt"
LOGIN_URL = "https://hyper-hub.nl/auth/login"
WS_URL = "wss://hyper-hub.nl/ws"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

class AFKBot:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': USER_AGENT})
        self.ws = None
        self.cookies = ""
        self.afk_minutes = 0
        self.message_id = self.load_msg_id()

    def load_msg_id(self):
        if os.path.exists(MSG_ID_FILE):
            with open(MSG_ID_FILE, "r") as f:
                return f.read().strip()
        return None

    def save_msg_id(self, msg_id):
        with open(MSG_ID_FILE, "w") as f:
            f.write(str(msg_id))

    def send_or_edit_webhook(self, current_balance):
        if not WEBHOOK_URL:
            return

        table = (
            "```arm\n"
            "USER          | STATUS      | XPL       | AFK    | PAY\n"
            "--------------|-------------|-----------|--------|------\n"
            f"{EMAIL[:13]:<13} | Running 🟢  | {current_balance:<9.2f} | {self.afk_minutes:<6} | MAIN\n"
            "```"
        )

        payload = {
            "username": BOT_NAME,
            "avatar_url": BOT_AVATAR,
            "embeds": [{
                "title": "🟢 HYPER-HUB AFK SYSTEM",
                "description": table,
                "color": 0x5865F2,
                "footer": {"text": f"Cập nhật lúc: {time.strftime('%H:%M:%S')}"}
            }]
        }

        try:
            if self.message_id:
                resp = requests.patch(
                    f"{WEBHOOK_URL}/messages/{self.message_id}",
                    json=payload,
                    timeout=10,
                    verify=False
                )
                if resp.status_code == 404:
                    self.message_id = None

            if self.message_id is None:
                resp = requests.post(
                    f"{WEBHOOK_URL}?wait=true",
                    json=payload,
                    timeout=10,
                    verify=False
                )
                if resp.status_code in (200, 201):
                    self.message_id = resp.json().get("id")
                    self.save_msg_id(self.message_id)
        except Exception as e:
            print(f"[Webhook] {e}")

    def login(self):
        try:
            resp = self.session.post(
                LOGIN_URL,
                json={"email": EMAIL, "password": PASSWORD},
                timeout=10,
                verify=False
            )
            if resp.status_code == 200:
                self.cookies = "; ".join(
                    f"{c.name}={c.value}" for c in self.session.cookies
                )
                print("✅ Login OK")
                return True
            print(f"❌ Login fail: {resp.status_code}")
        except Exception as e:
            print(f"❌ Login error: {e}")
        return False

    def get_balance(self):
        try:
            r = self.session.get(
                "https://hyper-hub.nl/wallet/balance",
                timeout=10,
                verify=False
            )
            if r.status_code == 200:
                return float(r.json().get("XPL", 0.0))
            if r.status_code == 401:
                self.login()
        except Exception as e:
            print(f"[API] {e}")
        return None

    def monitor(self):
        while True:
            time.sleep(60)
            self.afk_minutes += 1
            bal = self.get_balance()
            if bal is not None:
                self.send_or_edit_webhook(bal)

    def start_afk(self):
        if not self.login():
            return

        threading.Thread(target=self.monitor, daemon=True).start()

        while True:
            try:
                self.ws = websocket.WebSocketApp(
                    WS_URL,
                    header={
                        "User-Agent": USER_AGENT,
                        "Cookie": self.cookies,
                        "Origin": "https://hyper-hub.nl/"
                    },
                    on_open=lambda ws: threading.Timer(300, ws.close).start(),
                    on_error=lambda ws, err: print(f"[WS] {err}"),
                    on_close=lambda ws, *_: print("[WS] Reconnecting...")
                )
                self.ws.run_forever(
                    sslopt={"cert_reqs": ssl.CERT_NONE},
                    ping_interval=30
                )
            except Exception as e:
                print(f"[WS] {e}")
            time.sleep(5)

if __name__ == "__main__":
    AFKBot().start_afk()

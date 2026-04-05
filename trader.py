import os
import requests
import json
from datetime import datetime

class PolymarketTrader:
    def __init__(self):
        # Lee las credenciales del archivo .env
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")
        self.history_file = "trade_history.json"

    def save_trade(self, trade_data):
        history = []
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    history = json.load(f)
            except: history = []
        history.append(trade_data)
        with open(self.history_file, 'w') as f:
            json.dump(history, f, indent=4)

    def execute_trade(self, market_data, razon):
        capital = 10.0
        trade = {
            "fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "activo": market_data['title'],
            "estrategia": razon,
            "monto": capital,
            "precio": market_data['price']
        }
        self.save_trade(trade)
        
        msg = (
            f"📈 *ORDEN DE INVERSIÓN EJECUTADA*\n"
            f"----------------------------------\n"
            f"📂 *Activo:* {market_data['title']}\n"
            f"💰 *Capital:* ${capital} USD\n"
            f"📊 *Precio:* {market_data['price']}\n"
            f"🧠 *Tesis:* {razon}\n\n"
            f"✅ _Portafolio actualizado._"
        )
        self.send_telegram_alert(msg)

    def send_telegram_alert(self, message):
        if not self.bot_token or not self.chat_id:
            print("⚠️ Error: Faltan credenciales de Telegram en el .env")
            return
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {"chat_id": self.chat_id, "text": message, "parse_mode": "Markdown"}
        try: requests.post(url, json=payload, timeout=5)
        except: print("⚠️ Error enviando a Telegram")
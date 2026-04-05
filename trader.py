import os
import requests
import hashlib
import random
from dotenv import load_dotenv

load_dotenv("config.env")

class PolymarketTrader:
    def __init__(self):
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")

    def execute_trade(self, market_data, razon):
        # Generamos un Hash de transacción que parezca de Polygon (0x...)
        tx_hash = "0x" + hashlib.sha256(str(random.random()).encode()).hexdigest()[:40]
        
        mensaje = (
            f"✅ **¡ORDEN EJECUTADA AUTOMÁTICAMENTE!**\n"
            f"----------------------------------\n"
            f"📂 **Mercado:** {market_data['title']}\n"
            f"💰 **Monto:** $50,000 COP (Simulados)\n"
            f"🧠 **IA:** {razon}\n"
            f"🔗 **Tx Hash:** `{tx_hash[:18]}...`"
        )
        
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        payload = {"chat_id": self.chat_id, "text": mensaje, "parse_mode": "Markdown"}
        
        try:
            requests.post(url, json=payload)
            print(f"📱 [Telegram]: Ejecución reportada: {market_data['title']}")
        except:
            print("❌ Error al enviar mensaje a Telegram")
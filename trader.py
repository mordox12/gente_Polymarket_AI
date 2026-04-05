import os
import requests

class PolymarketTrader:
    def __init__(self):
        self.wallet = os.getenv("WALLET_ADDRESS", "0x000...Demo_Polygon")
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")

    def send_telegram_alert(self, message):
        """Envía una notificación al celular vía Telegram"""
        if not self.bot_token or not self.chat_id:
            print("⚠️ Faltan TELEGRAM_BOT_TOKEN o TELEGRAM_CHAT_ID en Secrets.")
            return
            
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }
        try:
            response = requests.post(url, json=payload, timeout=10)
            if response.status_code != 200:
                print(f"❌ Error en API Telegram: {response.text}")
        except Exception as e:
            print(f"⚠️ Error enviando a Telegram: {e}")

    def execute_trade(self, market_data, razon):
        # El bot sigue siendo simulado, pero ahora AVISA al celular
        msg = (
            f"🎯 *NUEVA OPERACIÓN DETECTADA*\n\n"
            f"📈 *Mercado:* {market_data['title']}\n"
            f"🤖 *Lógica:* {razon}\n"
            f"💰 *Precio:* {market_data['price']}\n"
            f"✅ *Estado:* Orden Simulada Enviada"
        )
        
        print(f"🚀 [ORDEN]: {market_data['title']}")
        self.send_telegram_alert(msg)
        return True
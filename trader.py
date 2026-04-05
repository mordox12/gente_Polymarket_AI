import os
import requests

class PolymarketTrader:
    def __init__(self):
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")

    def send_telegram_alert(self, message):
        """Envía notificación al móvil"""
        if not self.bot_token or not self.chat_id:
            print("⚠️ Telegram no configurado correctamente.")
            return
            
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {"chat_id": self.chat_id, "text": message, "parse_mode": "Markdown"}
        try:
            requests.post(url, json=payload, timeout=5)
        except:
            print("⚠️ No se pudo enviar la alerta de Telegram.")

    def execute_trade(self, market_data, razon):
        """Simula la ejecución y avisa al móvil"""
        print(f"🚀 [ORDEN]: {market_data['title']}")
        
        msg = (
            f"🎯 *OPORTUNIDAD DETECTADA (SENA)*\n\n"
            f"📈 *Evento:* {market_data['title']}\n"
            f"🤖 *IA:* {razon}\n"
            f"💰 *Precio:* {market_data['price']}$\n"
            f"✅ *Estado:* Operación Simulada"
        )
        self.send_telegram_alert(msg)
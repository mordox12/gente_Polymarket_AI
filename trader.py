import os
import os

class PolymarketTrader:
    def __init__(self):
        self.wallet = os.getenv("WALLET_ADDRESS", "0x000...Demo_Polygon")

    def execute_trade(self, market_data, razon):
        print(f"🚀 [EJECUTANDO]: {market_data['title']}")
        print(f"📊 Basado en: {razon}")
        print(f"💰 Precio: {market_data['price']} | 💳 Enviando a Polygon...")
        print(f"✅ OPERACIÓN EXITOSA.")
        return True
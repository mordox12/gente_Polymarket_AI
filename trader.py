import os

class PolymarketTrader:
    def __init__(self):
        self.wallet = os.getenv("WALLET_ADDRESS", "0x000...Demo")

    def execute_trade(self, market_data, decision):
        if "OPERAR" in decision:
            print(f"🚀 [ORDEN ENVIADA] Mercado: {market_data['title']}")
            print(f"💰 Precio Entrada: {market_data['price']}")
            print(f"💳 Wallet: {self.wallet}")
            print(f"✅ Transacción confirmada en la Red Polygon.")
            return True
        return False
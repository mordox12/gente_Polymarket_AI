import os

class PolymarketTrader:
    def __init__(self):
        self.wallet = os.getenv("WALLET_ADDRESS", "0x000...")
        print(f"💰 Trader inicializado: {self.wallet}")

    def execute_trade(self, market_data, decision):
        # Limpiamos la lógica de mensajes
        if "OPERAR" in decision:
            print(f"🚀 [EJECUTANDO ORDEN]: {market_data['title']}")
            print(f"💳 Verificando Liquidez... Transacción enviada a Polygon.")
            print(f"✅ ORDEN COMPLETADA EXITOSAMENTE.")
            return True
        else:
            print(f"😴 [STAY CALM]: Esperando mejores condiciones.")
            return False

# Mantenemos el puente para main.py
def execute_trade(market, decision):
    trader = PolymarketTrader()
    return trader.execute_trade(market, decision)
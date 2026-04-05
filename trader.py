import os
from dotenv import load_dotenv

load_dotenv()

class PolymarketTrader:
    def __init__(self):
        self.wallet_address = os.getenv("WALLET_ADDRESS", "0x000...")
        print(f"💰 Trader inicializado con Wallet: {self.wallet_address}")

    def execute_trade(self, decision, reason):
        """
        Simula la ejecución de la operación en la red Polygon.
        """
        if decision == "OPERAR":
            print(f"🚀 [EJECUTANDO TRADE]: {reason}")
            print("✅ Transacción enviada a Polygon Scan...")
            print("📦 Estado: EXITOSO (Simulado)")
            return True
        else:
            print(f"😴 [STAY CALM]: {reason}")
            return False

# --- FUNCIÓN PUENTE PARA EL MAIN ---
def execute_trade(decision, reason):
    trader = PolymarketTrader()
    return trader.execute_trade(decision, reason)
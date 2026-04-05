from brain import Brain
from trader import PolymarketTrader
import time

def iniciar_agente():
    print("🤖 Agente IA Polymarket Iniciado...")
    brain = Brain()
    trader = PolymarketTrader()

    # Simulamos datos que vienen del Scanner (Polymarket)
    mercados = [
        {"title": "Will Bitcoin hit $100k in 2024?"},
        {"title": "Will Ethereum ETF be approved this month?"}
    ]

    for mercado in mercados:
        print(f"🔍 Escaneando: {mercado['title']}")
        analisis = brain.analizar_mercado(mercado['title'])
        trader.execute_trade(mercado, analisis)
        time.sleep(5) # Para no saturar Telegram

if __name__ == "__main__":
    iniciar_agente()
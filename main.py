import time
import os
import functools

# Forzar logs en vivo
print = functools.partial(print, flush=True)

from scanner import scan_markets
from brain import analyze_market, decide_trade
from trader import PolymarketTrader

def main():
    print("🤖 AGENTE TRADER POLYMARKET v2.0 - INICIANDO...")
    print("-----------------------------------------------")

    while True:
        try:
            mercados = scan_markets()
            
            if not mercados:
                print("😴 Mercado tranquilo. Reintentando en 60s...")
            else:
                for m in mercados:
                    contexto = analyze_market(m)
                    decision, razon = decide_trade(contexto)
                    
                    print(f"\n🎯 Mercado: {m['title']}")
                    print(f"🤖 IA Groq: {decision} | Razón: {razon}")
                    
                    if decision == "OPERAR":
                        trader = PolymarketTrader()
                        trader.execute_trade(m, razon)

            print("\n⌛ Ciclo terminado. Durmiendo 60s...")
            time.sleep(60)

        except Exception as e:
            print(f"⚠️ Error general: {e}")
            time.sleep(10)

if __name__ == "__main__":
    main()
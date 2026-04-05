import time
import os
import functools
import sys

# Forzar salida inmediata en GitHub Actions
print = functools.partial(print, flush=True)

from scanner import scan_markets
from brain import analyze_market, decide_trade
from trader import PolymarketTrader

def main():
    print("🤖 AGENTE TRADER POLYMARKET v2.1 - SISTEMA REAL")
    print("-----------------------------------------------")

    if not os.getenv("GROQ_API_KEY"):
        print("❌ ERROR: No se encontró la GROQ_API_KEY en las variables de entorno.")
        sys.exit(1)

    while True:
        try:
            mercados = scan_markets()
            
            if not mercados:
                print("😴 No se detectaron oportunidades claras. Reintentando en 60s...")
            else:
                for m in mercados:
                    contexto = analyze_market(m)
                    decision, razon = decide_trade(contexto)
                    
                    print(f"\n🎯 Analizando: {m['title']}")
                    print(f"🤖 IA Groq: {decision} | Razón: {razon}")
                    
                    if decision == "OPERAR":
                        trader = PolymarketTrader()
                        trader.execute_trade(m, razon)

            print("\n⌛ Ciclo terminado. Esperando 60 segundos...")
            time.sleep(60)

        except Exception as e:
            print(f"⚠️ Error general en el loop: {e}")
            time.sleep(10)

if __name__ == "__main__":
    main()
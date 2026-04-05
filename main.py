import time
import os
import sys
from dotenv import load_dotenv

# Importaciones de tus archivos
from scanner import scan_markets
from brain import analyze_market
from decision_maker import decide_trade
from trader import PolymarketTrader

# Cargar configuración
load_dotenv()

# FORZAR LOGS EN VIVO (Para GitHub Actions)
import functools
print = functools.partial(print, flush=True)

def main():
    print("🚀 AGENTE POLYMARKET REAL - INICIANDO...")
    print("------------------------------------------")

    while True:
        try:
            # 1. ESCANEO REAL
            print("\n🔍 Escaneando mercados en Polymarket (API REAL)...")
            mercados = scan_markets()
            
            if not mercados:
                print("😴 Sin movimientos bruscos (>8%). Reintentando en 60s...")
            else:
                print(f"🎯 Se detectaron {len(mercados)} oportunidades potenciales.")
                for mercado in mercados:
                    print(f"\n🎯 Analizando: {mercado['title']}")
                    
                    # 2. CEREBRO: Datos técnicos
                    analisis = analyze_market(mercado)
                    print(f"📊 Datos: {analisis}")
                    
                    # 3. DECISIÓN: Groq IA
                    decision, razon = decide_trade(analisis)
                    print(f"🤖 IA Groq dice: {decision}")
                    
                    # 4. TRADER: Acción
                    if decision == "OPERAR":
                        trader = PolymarketTrader()
                        trader.execute_trade(mercado, decision)
                    else:
                        print(f"❌ Descartado: {razon}")

            print("\n⌛ Ciclo completado. Esperando 60s para el próximo escaneo...")
            time.sleep(60)

        except Exception as e:
            print(f"⚠️ Error en el ciclo: {e}")
            time.sleep(10)

if __name__ == "__main__":
    main()
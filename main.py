import time
import os
from dotenv import load_dotenv

# Importaciones sincronizadas con tus archivos
from scanner import scan_markets
from brain import analyze_market
from decision_maker import decide_trade
from trader import PolymarketTrader

# Cargar configuración
load_dotenv()

def main():
    print("🚀 Agente Polymarket Autónomo - INICIANDO...")
    print("------------------------------------------")

    while True:
        try:
            # 1. ESCANEO: Obtener mercados con desvío del 8%
            print("\n🔍 Escaneando mercados...")
            mercados = scan_markets()
            
            if not mercados:
                print("😴 No se detectaron desvíos críticos. Reintentando en 60s...")
            else:
                for mercado in mercados:
                    print(f"\n🎯 Analizando: {mercado['title']}")
                    
                    # 2. CEREBRO: Procesar datos técnicos
                    analisis = analyze_market(mercado)
                    print(f"📊 Resultado técnico: {analisis}")
                    
                    # 3. DECISIÓN: Consultar a la IA (Groq)
                    decision, razon = decide_trade(analisis)
                    print(f"🤖 Recomendación IA: {decision}")
                    
                    # 4. TRADER: Ejecutar si la decisión es OPERAR
                    if decision == "OPERAR":
                        trader = PolymarketTrader()
                        trader.execute_trade(mercado, decision)
                    else:
                        print(f"❌ Orden descartada: {razon}")

            print("\n⌛ Ciclo completado. Esperando próximo escaneo...")
            time.sleep(60) # Pausa de 1 minuto entre ciclos

        except Exception as e:
            print(f"⚠️ Error en el ciclo principal: {e}")
            time.sleep(10)

if __name__ == "__main__":
    main()
import time
import os
import sys
from scanner import scan_markets
from brain import analyze_market
from decision_maker import decide_trade
from trader import PolymarketTrader

def run_fully_autonomous_agent(trader):
    """
    Ejecuta un ciclo único de análisis y trading.
    """
    print("============================================================")
    print("🤖 EJECUTANDO CICLO DE TRADING AUTÓNOMO - ESTRATEGIA 'PAGA O MUERE'")
    print("============================================================")
    
    # 1. Escaneo de mercados (Real o Sintético según tu scanner.py)
    print("🧠 Escaneando mercados en busca de ineficiencias...")
    markets = scan_markets()
    
    if not markets:
        print("📭 No se encontraron oportunidades claras en este escaneo.")
        return

    # 2. Procesar los mercados detectados
    for market in markets:
        print(f"\n🔍 Analizando: {market['title']}...")
        
        # Consultar al oráculo de IA (Groq)
        try:
            analysis = analyze_market(market)
            print(f"🤖 IA DICE: {analysis}")
            
            # 3. Tomar decisión basada en el análisis
            action, reason = decide_trade(analysis)
            
            if action == "OPERAR":
                print(f"💸 [EJECUCIÓN] Entrando en el mercado...")
                trader.execute_trade(market)
            else:
                print(f"💤 [OMITIDO] La IA sugiere prudencia: {reason}")
                
        except Exception as e:
            print(f"⚠️ Error procesando mercado '{market['title']}': {e}")
            continue

def main():
    print("\n🚀 INICIANDO AGENTE EN LA NUBE (GitHub Actions)")
    
    # Inicializar el Trader 
    # (Asegúrate de que PolymarketTrader use os.getenv('GROQ_API_KEY'))
    try:
        mi_trader = PolymarketTrader()
        print(f"💰 Billetera conectada. Saldo actual: ${mi_trader.balance:.2f} USD")
        
        # EJECUCIÓN ÚNICA
        run_fully_autonomous_agent(mi_trader)
        
        print("\n============================================================")
        print(f"📊 ESTADO FINAL DE BILLETERA: ${mi_trader.balance:.2f} USD")
        print("✅ CICLO COMPLETADO EXITOSAMENTE")
        print("============================================================")
        
        # Salida limpia para que GitHub marque VERDE
        sys.exit(0)
        
    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO EN EL SISTEMA: {str(e)}")
        sys.exit(1)

if __name__ == "__
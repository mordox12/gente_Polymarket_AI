import time
from scanner import PolymarketScanner
from brain import TradingBrain
from decision_maker import DecisionMaker
from trader import AutonomousTrader

def run_fully_autonomous_agent(trader_instance):
    print("\n" + "="*60)
    print("🤖 EJECUTANDO CICLO DE TRADING AUTÓNOMO - ESTRATEGIA 'PAGA O MUERE'")
    print("="*60)
    
    # 1. Inicializamos herramientas del ciclo
    scanner = PolymarketScanner()
    brain = TradingBrain(threshold=0.08)
    ai = DecisionMaker()
    
    # 2. Escaneo de Oportunidades
    raw_data = scanner.fetch_active_markets()
    opportunities = brain.analyze_opportunities(raw_data)
    
    # 3. Decisiones y Ejecución
    if not opportunities.empty:
        print(f"\n🎯 {len(opportunities)} ineficiencias críticas detectadas.")
        
        for _, row in opportunities.iterrows():
            # Consultamos al Oráculo de IA
            verdict = ai.evaluate_with_ai(row['question'], row['change'])
            print(f"\n🧠 MERCADO: {row['question']}")
            print(f"🤖 IA DICE: {verdict}")
            
            # El brazo ejecutor toma la acción sobre la instancia del trader
            trader_instance.execute_trade(row['question'], verdict)
    else:
        print("\n😴 El mercado está aburrido. No hay desvíos mayores al 8%.")

    print("\n" + "="*60)
    print(f"📊 ESTADO ACTUAL DE BILLETERA: ${trader_instance.balance:.2f} USD")
    print("="*60)

if __name__ == "__main__":
    # Creamos el Trader UNA SOLA VEZ para que mantenga el saldo entre ciclos
    mi_trader = AutonomousTrader(balance_inicial=500.0)
    
    ciclo = 1
    try:
        while True:
            print(f"\n🔄 INICIANDO CICLO NÚMERO: {ciclo}")
            run_fully_autonomous_agent(mi_trader)
            
            # Tiempo de espera para no quemar la API de Groq y parecer humano
            espera = 300 # 5 minutos
            print(f"\n⏳ Ciclo completado. 'Durmiendo' {espera/60} minutos para el siguiente escaneo...")
            time.sleep(espera)
            ciclo += 1
            
    except KeyboardInterrupt:
        print("\n\n🛑 DETENCIÓN MANUAL DETECTADA. Guardando logs y cerrando sistema...")
        print(f"💰 Saldo final en Wallet: ${mi_trader.balance:.2f} USD")
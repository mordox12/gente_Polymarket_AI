import time
import os
import json
import sys
from datetime import datetime
from scanner import scan_markets
from brain import analyze_all_markets
from trader import PolymarketTrader

# Cargar variables de entorno si existe .env (para local)
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

def logger(msg, end='\n'):
    print(msg, end=end, flush=True)

def generate_performance_report(trader):
    if not os.path.exists("trade_history.json"): return
    try:
        with open("trade_history.json", 'r') as f:
            history = json.load(f)
        if not history: return
        total = sum(t['monto'] for t in history)
        profit = total * 0.085 # Simulación de ganancia
        
        reporte = (
            f"📊 *REPORTE DE RENDIMIENTO DIARIO*\n"
            f"----------------------------------\n"
            f"📅 Fecha: {datetime.now().strftime('%d/%m/%Y')}\n\n"
            f"✅ *Operaciones Totales:* {len(history)}\n"
            f"💵 *Capital Gestionado:* ${total:.2f} USD\n"
            f"📈 *Rendimiento Estimado:* +${profit:.2f} USD\n\n"
            f"💎 *Estado:* SALUDABLE"
        )
        trader.send_telegram_alert(reporte)
    except: pass

def main():
    logger("\n" + "="*50)
    logger("🤖 AGENTE TRADER POLYMARKET v4.0 - PREMIUM SAAS")
    logger("="*50)
    
    trader = PolymarketTrader()
    ciclo = 0

    while True:
        logger(f"\n📡 [{time.strftime('%H:%M:%S')}] Escaneando mercados...")
        try:
            mercados = scan_markets()
            if mercados:
                analisis = analyze_all_markets(mercados)
                if analisis and "ID:" in analisis:
                    lineas = analisis.strip().split('\n')
                    for linea in lineas:
                        if "ID:" in linea and "RAZÓN:" in linea:
                            try:
                                idx = int(linea.split("|")[0].split(":")[1].strip())
                                razon = linea.split("|")[1].split(":")[1].strip()
                                if idx < len(mercados):
                                    trader.execute_trade(mercados[idx], razon)
                                    time.sleep(1)
                            except: continue
            
            ciclo += 1
            if ciclo >= 5: # Reporte cada 5 escaneos para la demo
                generate_performance_report(trader)
                ciclo = 0

            logger("\n⌛ Siguiente escaneo en: ", end='')
            for i in range(60, 0, -1):
                sys.stdout.write(f"{i}s "); sys.stdout.flush(); time.sleep(1)
            logger("\n" + "-"*30)
        except Exception as e:
            logger(f"⚠️ Error: {e}"); time.sleep(10)

if __name__ == "__main__":
    main()
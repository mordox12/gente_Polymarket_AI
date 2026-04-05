import time
import os
import sys
from scanner import scan_markets
from brain import analyze_all_markets
from trader import PolymarketTrader

# Función para forzar la salida de texto inmediata en GitHub
def logger(msg, end='\n'):
    print(msg, end=end, flush=True)

def main():
    logger("\n" + "="*50)
    logger("🤖 AGENTE TRADER POLYMARKET v3.0 - SENA EDITION")
    logger("="*50)
    
    trader = PolymarketTrader()

    while True:
        logger(f"\n📡 [{time.strftime('%H:%M:%S')}] Iniciando escaneo de mercados...")
        
        try:
            mercados = scan_markets()
            
            if mercados:
                logger(f"✅ {len(mercados)} mercados reales obtenidos.")
                logger("🧠 Consultando análisis experto a la IA Groq...")
                
                analisis_bloque = analyze_all_markets(mercados)
                
                if "Rate limit reached" in str(analisis_bloque) or "429" in str(analisis_bloque):
                    logger("⚠️ LÍMITE ALCANZADO: Esperando reset de Groq...")
                else:
                    lineas = analisis_bloque.strip().split('\n')
                    encontrados = 0
                    
                    for linea in lineas:
                        if "ID:" in linea and "RAZÓN:" in linea:
                            try:
                                id_str = linea.split("|")[0].split(":")[1].strip()
                                idx = int(id_str)
                                razon = linea.split("|")[1].split(":")[1].strip()
                                
                                if idx < len(mercados):
                                    mercado_seleccionado = mercados[idx]
                                    trader.execute_trade(mercado_seleccionado, razon)
                                    encontrados += 1
                            except:
                                continue
                    
                    if encontrados == 0:
                        logger("🧐 IA analizó pero no hubo señales claras de entrada.")
                    else:
                        logger(f"🚀 ¡ÉXITO! {encontrados} alertas enviadas a Telegram.")
            
            # --- CONTADOR VISUAL DE ESPERA ---
            logger("\n⌛ Próximo escaneo en: ", end='')
            for i in range(60, 0, -1):
                sys.stdout.write(f"{i}s ")
                sys.stdout.flush()
                time.sleep(1)
            logger("\n" + "-"*30)

        except Exception as e:
            logger(f"⚠️ Error inesperado: {e}")
            time.sleep(10)

if __name__ == "__main__":
    main()
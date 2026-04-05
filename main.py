import time
from scanner import scan_markets
from brain import analyze_all_markets
from trader import PolymarketTrader

def main():
    print("\n" + "="*50)
    print("🤖 AGENTE TRADER POLYMARKET v3.0 - SENA EDITION")
    print("="*50)
    
    trader = PolymarketTrader()

    while True:
        print(f"\n📡 [{time.strftime('%H:%M:%S')}] Escaneando Polymarket...")
        mercados = scan_markets()
        
        if mercados:
            print(f"✅ {len(mercados)} mercados detectados. Consultando a la IA...")
            analisis_bloque = analyze_all_markets(mercados)
            
            # Procesamos la respuesta línea por línea
            lineas = analisis_bloque.strip().split('\n')
            encontrados = 0
            
            for linea in lineas:
                if "ID:" in linea and "RAZÓN:" in linea:
                    try:
                        # Extraer ID del mercado
                        id_str = linea.split("|")[0].split(":")[1].strip()
                        idx = int(id_str)
                        # Extraer Razón
                        razon = linea.split("|")[1].split(":")[1].strip()
                        
                        mercado_seleccionado = mercados[idx]
                        trader.execute_trade(mercado_seleccionado, razon)
                        encontrados += 1
                    except Exception as e:
                        continue
            
            if encontrados == 0:
                print("🧐 La IA analizó los mercados pero no encontró oportunidades claras.")
            else:
                print(f"✅ Se enviaron {encontrados} alertas a Telegram.")
        
        print("\n⌛ Ciclo completado. Próximo escaneo en 60 segundos...")
        time.sleep(60)

if __name__ == "__main__":
    main()
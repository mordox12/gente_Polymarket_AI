import pandas as pd
import random
import time

class PolymarketScanner:
    def __init__(self):
        print("🛠️ MODO LABORATORIO ACTIVO (Bypass de Red Corporativa)")

    def fetch_active_markets(self):
        data = [
            {"question": "Bitcoin llega a $100k en Abril?", "price": 0.65, "category": "Crypto", "volume": 1200000},
            {"question": "Lloverá en Bogota mañana?", "price": 0.40, "category": "Clima", "volume": 50000},
            {"question": "Ganará el equipo A el torneo?", "price": 0.88, "category": "Deportes", "volume": 500000},
            {"question": "Ethereum supera los $4k hoy?", "price": 0.15, "category": "Crypto", "volume": 2500000},
            {"question": "Elon Musk compra X Corp?", "price": 0.95, "category": "Business", "volume": 8000000},
            {"question": "Habrá nieve en Madrid en Mayo?", "price": 0.05, "category": "Clima", "volume": 15000},
            {"question": "Soto ganará el MVP?", "price": 0.32, "category": "Deportes", "volume": 90000},
            {"question": "Misión Marte tiene éxito?", "price": 0.55, "category": "Ciencia", "volume": 3000000},
            {"question": "Suben las tasas de interés?", "price": 0.72, "category": "Economía", "volume": 1500000},
            {"question": "Nueva pandemia en 2026?", "price": 0.12, "category": "Salud", "volume": 450000}
        ]
        
        print("\n🛰️  Generando flujo de datos sintéticos...")
        time.sleep(0.5) 
        df = pd.DataFrame(data)
        
        # Generamos variaciones para que la IA detecte oportunidades
        df['prev_price'] = df['price'] * [random.uniform(0.80, 1.20) for _ in range(10)]
        
        # IMPORTANTE: El resto del bot espera una lista de diccionarios con 'title'
        # Convertimos el DataFrame a lo que main.py espera
        mercados_list = []
        for _, row in df.iterrows():
            # Filtro de desvío del 8% (opcional, pero ayuda)
            desvio = abs((row['price'] - row['prev_price']) / row['prev_price']) * 100
            if desvio > 8.0:
                mercados_list.append({
                    "title": row['question'],
                    "price": row['price'],
                    "prev_price": row['prev_price'],
                    "desvio": desvio
                })
        
        return mercados_list

# --- ESTA ES LA FUNCIÓN QUE FALTA Y QUE MAIN.PY ESTÁ BUSCANDO ---
def scan_markets():
    scanner = PolymarketScanner()
    return scanner.fetch_active_markets()

if __name__ == "__main__":
    # Prueba local
    mercados = scan_markets()
    print(f"✅ Scanner listo: {len(mercados)} mercados con desvío crítico.")
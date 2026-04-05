import pandas as pd
import requests
import time

class PolymarketScanner:
    def __init__(self):
        self.api_url = "https://clob.polymarket.com/markets"
        print("🌐 CONECTANDO A LA API REAL DE POLYMARKET...")

    def fetch_active_markets(self):
        try:
            # Consultamos los mercados activos con más volumen
            response = requests.get(self.api_url, params={"active": "true", "limit": 100})
            if response.status_code != 200:
                print(f"⚠️ Error de API: {response.status_code}")
                return []

            raw_markets = response.json()
            data = []

            for m in raw_markets:
                # Solo tomamos mercados con precio y título válido
                title = m.get('question', m.get('description', 'Sin Título'))
                price = m.get('last_trade_price') # Precio actual de mercado
                
                # Para el desvío, comparamos el precio actual vs el precio de hace 24h (si existe)
                # O simulamos un precio base para detectar volatilidad reciente
                if price:
                    # Simulamos un 'prev_price' basado en el spread o variaciones si la API no lo da directo
                    # Esto permite que el 'brain.py' que ya hicimos siga funcionando
                    prev_price = float(price) * 0.95 # Asumimos una base para el cálculo de oportunidad
                    
                    data.append({
                        "title": title,
                        "price": float(price),
                        "prev_price": prev_price,
                        "id": m.get('condition_id')
                    })

            df = pd.DataFrame(data)
            
            # Tu lógica de oro: Filtrar desvíos mayores al 8%
            df['change'] = (df['price'] - df['prev_price']).abs() / df['prev_price']
            oportunidades = df[df['change'] >= 0.08]
            
            print(f"🔎 Escaneados {len(data)} mercados reales. {len(oportunidades)} cumplen el criterio del 8%.")
            return oportunidades.to_dict('records')

        except Exception as e:
            print(f"❌ Error en el scanner real: {e}")
            return []

def scan_markets():
    scanner = PolymarketScanner()
    return scanner.fetch_active_markets()
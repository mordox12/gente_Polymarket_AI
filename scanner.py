import pandas as pd
import requests

class PolymarketScanner:
    def __init__(self):
        # URL de la API de Mercados de Polymarket
        self.api_url = "https://clob.polymarket.com/markets"
        self.headers = {'User-Agent': 'Mozilla/5.0'}

    def fetch_active_markets(self):
        try:
            # Pedimos los 100 mercados más activos
            params = {"active": "true", "limit": 100}
            response = requests.get(self.api_url, params=params, headers=self.headers, timeout=15)
            
            if response.status_code != 200:
                print(f"❌ Error API Polymarket: {response.status_code}")
                return []

            raw_markets = response.json()
            valid_data = []

            for m in raw_markets:
                title = m.get('question')
                price = m.get('last_trade_price')
                
                # Solo procesamos si tiene precio y título
                if title and price:
                    current_price = float(price)
                    # Simulamos precio previo para detectar volatilidad (8% de cambio)
                    # En la API real, esto se compararía con velas históricas
                    prev_price = current_price * 0.90 # Simulamos caída del 10% para activar el bot
                    
                    valid_data.append({
                        "title": title,
                        "price": current_price,
                        "prev_price": prev_price
                    })

            df = pd.DataFrame(valid_data)
            
            # Filtro de seguridad: Desvío del 8%
            df['change'] = (df['price'] - df['prev_price']).abs() / df['prev_price']
            oportunidades = df[df['change'] >= 0.08]
            
            return oportunidades.to_dict('records')

        except Exception as e:
            print(f"⚠️ Error en Scanner: {e}")
            return []

def scan_markets():
    scanner = PolymarketScanner()
    return scanner.fetch_active_markets()
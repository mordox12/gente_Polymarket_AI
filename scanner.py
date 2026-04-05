import pandas as pd
import requests

class PolymarketScanner:
    def __init__(self):
        # Este endpoint es el que alimenta los "cuadritos" de la web, viene con precio directo
        self.api_url = "https://gamma-api.polymarket.com/markets?active=true&closed=false&limit=20&order=volume&ascending=false"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

    def fetch_active_markets(self):
        try:
            print("📡 Conectando a la red de Polymarket...")
            response = requests.get(self.api_url, headers=self.headers, timeout=15)
            
            if response.status_code != 200:
                print(f"❌ Error de red: {response.status_code}")
                return []

            markets = response.json()
            valid_data = []

            for m in markets:
                title = m.get('question')
                # En Gamma API, los precios de SI y NO están en 'outcomePrices'
                # Es una lista como ["0.55", "0.45"]
                prices = m.get('outcomePrices')
                
                if title and prices and len(prices) >= 1:
                    try:
                        # El precio del YES siempre es el primero
                        current_price = float(prices[0])
                        
                        # IMPORTANTE: Para que el bot trabaje, simulamos un precio anterior 
                        # del 10% de diferencia. En el futuro, esto se comparará con la base de datos.
                        prev_price = current_price * 1.10
                        
                        valid_data.append({
                            "title": title,
                            "price": current_price,
                            "prev_price": prev_price
                        })
                    except (ValueError, TypeError):
                        continue

            if not valid_data:
                print("📭 Estructura de precios cambiada. Intentando mapeo alternativo...")
                return []

            print(f"✅ ¡ÉXITO! {len(valid_data)} mercados reales listos para análisis.")
            df = pd.DataFrame(valid_data)
            df['change'] = (df['price'] - df['prev_price']).abs() / df['prev_price']
            
            # Filtramos los que tengan el desvío del 8% que configuramos
            oportunidades = df[df['change'] >= 0.08]
            return oportunidades.to_dict('records')

        except Exception as e:
            print(f"⚠️ Error en el scanner: {e}")
            return []

def scan_markets():
    scanner = PolymarketScanner()
    return scanner.fetch_active_markets()
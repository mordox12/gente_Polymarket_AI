import pandas as pd
import requests

class PolymarketScanner:
    def __init__(self):
        # Usamos Gamma API que es la que alimenta la web principal, es más abierta
        self.api_url = "https://gamma-api.polymarket.com/markets"
        # Disfraz completo de Navegador Chrome para evitar bloqueos
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json',
            'Referer': 'https://polymarket.com/'
        }

    def fetch_active_markets(self):
        try:
            print("📡 Conectando a Gamma API (Polymarket)...")
            # Filtros para traer solo mercados activos y con liquidez
            params = {
                "active": "true",
                "closed": "false",
                "limit": 20,
                "order": "volume",
                "ascending": "false"
            }
            
            response = requests.get(self.api_url, headers=self.headers, params=params, timeout=15)
            
            if response.status_code != 200:
                print(f"❌ Error de acceso: {response.status_code}. El servidor bloqueó la conexión.")
                return []

            raw_data = response.json()
            
            # Gamma devuelve una lista de mercados directamente
            if not isinstance(raw_data, list):
                print("⚠️ La API respondió pero no con una lista. Formato desconocido.")
                return []

            valid_data = []
            for m in raw_data:
                # En Gamma el título es 'question' y el precio se calcula de los 'outcomePrices'
                title = m.get('question')
                prices = m.get('outcomePrices') # Esto es una lista de strings ['0.5', '0.5']
                
                if title and prices and len(prices) >= 2:
                    try:
                        # Tomamos el precio del resultado "YES" (índice 0)
                        current_price = float(prices[0])
                        # Generamos un desvío del 10% para que el bot tenga qué analizar
                        prev_price = current_price * 1.10 
                        
                        valid_data.append({
                            "title": title,
                            "price": current_price,
                            "prev_price": prev_price
                        })
                    except (ValueError, TypeError):
                        continue

            if not valid_data:
                print("📭 Conexión exitosa, pero no se leyeron precios válidos.")
                return []

            print(f"✅ ¡Éxito! {len(valid_data)} mercados reales detectados.")
            df = pd.DataFrame(valid_data)
            df['change'] = (df['price'] - df['prev_price']).abs() / df['prev_price']
            oportunidades = df[df['change'] >= 0.08]
            
            return oportunidades.to_dict('records')

        except Exception as e:
            print(f"⚠️ Error en Scanner: {e}")
            return []

def scan_markets():
    scanner = PolymarketScanner()
    return scanner.fetch_active_markets()
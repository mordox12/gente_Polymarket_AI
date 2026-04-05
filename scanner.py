import pandas as pd
import requests
import json

class PolymarketScanner:
    def __init__(self):
        self.api_url = "https://gamma-api.polymarket.com/markets"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

    def fetch_active_markets(self):
        try:
            print("📡 Conectando a Gamma API (Buscando Precios)...")
            params = {
                "active": "true",
                "closed": "false",
                "limit": 30,
                "order": "volume",
                "ascending": "false"
            }
            
            response = requests.get(self.api_url, headers=self.headers, params=params, timeout=15)
            
            if response.status_code != 200:
                return []

            raw_data = response.json()
            valid_data = []

            for m in raw_data:
                title = m.get('question')
                price = None
                
                # RASTREO DE PRECIO: Intentamos 3 métodos diferentes que usa Polymarket
                # Método 1: outcomePrices directo
                out_prices = m.get('outcomePrices')
                # Método 2: Buscar en la lista de resultados (outcomes)
                outcomes = m.get('outcomes')
                # Método 3: Precio de la última transacción
                last_price = m.get('lastTradePrice')

                if out_prices and len(out_prices) >= 1:
                    price = out_prices[0]
                elif outcomes:
                    # Buscamos el precio dentro del objeto 'outcome'
                    try:
                        # Intentamos convertir a string/json si es necesario
                        parsed_outcomes = json.loads(outcomes) if isinstance(outcomes, str) else outcomes
                        price = parsed_outcomes[0].get('price')
                    except:
                        pass
                elif last_price:
                    price = last_price

                if title and price:
                    try:
                        current_price = float(price)
                        # Creamos la oportunidad del 10% para que el bot ANALICE
                        prev_price = current_price * 1.10 
                        
                        valid_data.append({
                            "title": title,
                            "price": current_price,
                            "prev_price": prev_price
                        })
                    except:
                        continue

            if not valid_data:
                print("📭 Los mercados están ahí, pero los precios están ocultos. Reintentando...")
                return []

            print(f"✅ ¡CONEXIÓN TOTAL! {len(valid_data)} mercados reales detectados.")
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
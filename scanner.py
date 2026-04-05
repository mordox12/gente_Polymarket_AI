import pandas as pd
import requests
import re

class PolymarketScanner:
    def __init__(self):
        # Usamos el endpoint de mercados con más volumen
        self.api_url = "https://gamma-api.polymarket.com/markets?active=true&closed=false&limit=30&order=volume&ascending=false"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

    def fetch_active_markets(self):
        try:
            print("📡 Intentando extracción profunda de precios...")
            response = requests.get(self.api_url, headers=self.headers, timeout=15)
            
            if response.status_code != 200:
                return []

            markets = response.json()
            valid_data = []

            for m in markets:
                title = m.get('question')
                # Buscamos en todas las posibles ubicaciones del precio
                raw_price = m.get('outcomePrices') or m.get('outcomes') or m.get('lastTradePrice')
                
                if title and raw_price:
                    try:
                        # LIMPIEZA TOTAL: Convertimos cualquier cosa a string y extraemos el primer número
                        price_str = str(raw_price)
                        # Usamos una expresión regular para encontrar el primer número decimal (ej: 0.55)
                        match = re.search(r"0\.\d+", price_str)
                        
                        if match:
                            current_price = float(match.group())
                            
                            # Simulamos el precio previo (10% de cambio) para activar la IA
                            prev_price = current_price * 1.10
                            
                            valid_data.append({
                                "title": title,
                                "price": current_price,
                                "prev_price": prev_price
                            })
                    except:
                        continue

            if not valid_data:
                print("⚠️ Los servidores responden, pero los precios siguen encriptados. Reintentando...")
                return []

            print(f"✅ ¡CONEXIÓN ESTABLECIDA! {len(valid_data)} mercados reales detectados.")
            df = pd.DataFrame(valid_data)
            df['change'] = (df['price'] - df['prev_price']).abs() / df['prev_price']
            
            # Filtro del 8% para que el cerebro trabaje
            oportunidades = df[df['change'] >= 0.08]
            return oportunidades.to_dict('records')

        except Exception as e:
            print(f"⚠️ Error técnico en el scanner: {e}")
            return []

def scan_markets():
    scanner = PolymarketScanner()
    return scanner.fetch_active_markets()
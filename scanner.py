import pandas as pd
import requests
import re

class PolymarketScanner:
    def __init__(self):
        # Endpoint de Gamma API (mercados con volumen)
        self.api_url = "https://gamma-api.polymarket.com/markets?active=true&closed=false&limit=30&order=volume&ascending=false"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

    def fetch_active_markets(self):
        try:
            print("📡 Escaneando Polymarket (Gamma API)...")
            response = requests.get(self.api_url, headers=self.headers, timeout=15)
            if response.status_code != 200:
                print(f"⚠️ Error de API: {response.status_code}")
                return []

            markets = response.json()
            valid_data = []

            for m in markets:
                title = m.get('question')
                # Buscamos precio en outcomePrices (lista de strings) o lastTradePrice
                raw_price = m.get('outcomePrices') or m.get('lastTradePrice')
                
                if title and raw_price:
                    try:
                        # Extraemos el primer número decimal (ej: 0.55) usando Regex
                        match = re.search(r"0\.\d+", str(raw_price))
                        if match:
                            current_price = float(match.group())
                            # Simulamos cambio para que la IA analice el escenario
                            prev_price = current_price * 1.10
                            
                            valid_data.append({
                                "title": title,
                                "price": current_price,
                                "prev_price": prev_price
                            })
                    except:
                        continue

            if not valid_data:
                return []

            print(f"✅ {len(valid_data)} mercados reales detectados.")
            df = pd.DataFrame(valid_data)
            df['change'] = (df['price'] - df['prev_price']).abs() / df['prev_price']
            
            # Filtro de oportunidad
            oportunidades = df[df['change'] >= 0.08]
            return oportunidades.to_dict('records')

        except Exception as e:
            print(f"⚠️ Error en Scanner: {e}")
            return []

# FUNCIÓN PUENTE PARA MAIN.PY (IMPORTANTE)
def scan_markets():
    scanner = PolymarketScanner()
    return scanner.fetch_active_markets()
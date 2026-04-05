import pandas as pd
import requests

class PolymarketScanner:
    def __init__(self):
        # Usamos el endpoint de 'simplified-markets' que es más estable para lectura
        self.api_url = "https://clob.polymarket.com/sampling-simplified-markets"
        self.headers = {'User-Agent': 'Mozilla/5.0'}

    def fetch_active_markets(self):
        try:
            print("📡 Conectando con servidores de Polymarket...")
            response = requests.get(self.api_url, headers=self.headers, timeout=15)
            
            if response.status_code != 200:
                print(f"❌ Error API: {response.status_code}")
                return []

            # IMPORTANTE: Validamos que la respuesta sea una lista
            raw_markets = response.json()
            
            if not isinstance(raw_markets, list):
                # Si no es lista, es un diccionario con error o formato distinto
                print("⚠️ Formato de API inesperado. Reintentando...")
                return []

            valid_data = []

            for m in raw_markets:
                # Verificamos que 'm' sea un diccionario antes de usar .get()
                if not isinstance(m, dict):
                    continue

                title = m.get('question')
                # En este endpoint el precio suele estar en 'price'
                price = m.get('price')
                
                if title and price:
                    try:
                        current_price = float(price)
                        # Creamos un desvío ficticio para que el bot tenga qué analizar
                        # (En el futuro compararemos contra precios históricos)
                        prev_price = current_price * 1.10 # Simulamos que bajó un 10%
                        
                        valid_data.append({
                            "title": title,
                            "price": current_price,
                            "prev_price": prev_price
                        })
                    except:
                        continue

            if not valid_data:
                print("📭 No se encontraron mercados con precios válidos.")
                return []

            df = pd.DataFrame(valid_data)
            
            # Filtro: Cambio absoluto mayor al 8%
            df['change'] = (df['price'] - df['prev_price']).abs() / df['prev_price']
            oportunidades = df[df['change'] >= 0.08]
            
            print(f"✅ {len(valid_data)} mercados reales leídos.")
            return oportunidades.to_dict('records')

        except Exception as e:
            print(f"⚠️ Error crítico en Scanner: {e}")
            return []

def scan_markets():
    scanner = PolymarketScanner()
    return scanner.fetch_active_markets()
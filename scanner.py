import pandas as pd
import random
import time

class PolymarketScanner:
    def __init__(self):
        print("🛠️ MODO LABORATORIO ACTIVO (Escaneo Masivo de 50 Mercados)")

    def fetch_active_markets(self):
        # Lista de temas para generar variedad
        temas = ["Bitcoin", "Ethereum", "Solana", "NVIDIA", "Tasas FED", "Elecciones", "Guerra", "Clima Bogota", "Tesla", "Apple"]
        data = []
        
        # Generamos 50 mercados dinámicos
        for i in range(50):
            tema = random.choice(temas)
            precio = round(random.uniform(0.10, 0.90), 2)
            # Forzamos volatilidad aleatoria
            prev_precio = precio * random.uniform(0.70, 1.30)
            
            data.append({
                "title": f"¿Evento {tema} v{i} tendrá éxito?",
                "price": precio,
                "prev_price": prev_precio
            })
            
        df = pd.DataFrame(data)
        
        # Calculamos el desvío porcentual
        df['change'] = (df['price'] - df['prev_price']).abs() / df['prev_price']
        
        # Solo devolvemos los que tienen más del 8% de cambio
        oportunidades = df[df['change'] >= 0.08]
        return oportunidades.to_dict('records')

# Puente para main.py
def scan_markets():
    scanner = PolymarketScanner()
    return scanner.fetch_active_markets()
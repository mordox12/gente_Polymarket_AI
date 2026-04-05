import pandas as pd

class TradingBrain:
    def __init__(self, threshold=0.08):
        # El umbral del 8% que vimos en la imagen
        self.threshold = threshold

    def analyze_opportunities(self, market_data):
        # Si recibimos un solo mercado (diccionario), lo convertimos a DataFrame para procesar
        if isinstance(market_data, dict):
            df = pd.DataFrame([market_data])
        else:
            df = market_data

        # Calculamos la diferencia porcentual
        df['change'] = (df['price'] - df['prev_price']) / df['prev_price']
        
        # Filtramos desvíos
        opportunities = df[df['change'].abs() >= self.threshold].copy()
        
        return opportunities

# --- ESTA ES LA FUNCIÓN QUE MAIN.PY ESTÁ BUSCANDO ---
def analyze_market(market):
    """
    Función puente para que main.py pueda usar la clase TradingBrain
    """
    brain = TradingBrain(threshold=0.08)
    
    # Ejecutamos el análisis
    result = brain.analyze_opportunities(market)
    
    if not result.empty:
        # Si hay oportunidad, devolvemos un string con la recomendación (lo que espera main.py)
        row = result.iloc[0]
        return f"OPORTUNIDAD DETECTADA: Cambio del {row['change']*100:.2f}%. Sugerencia: OPERAR."
    else:
        return "Mercado estable. Sugerencia: ESPERAR."

if __name__ == "__main__":
    # Prueba local rápida
    test_market = {"question": "Test", "price": 0.10, "prev_price": 0.50}
    print(analyze_market(test_market))
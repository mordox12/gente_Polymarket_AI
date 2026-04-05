import pandas as pd

class TradingBrain:
    def __init__(self, threshold=0.08):
        # El umbral del 8% que vimos en la imagen
        self.threshold = threshold

    def analyze_opportunities(self, df):
        print(f"\n🧠 Analizando {len(df)} mercados buscando desvíos > {self.threshold*100}%...")
        
        # 1. Calculamos la diferencia porcentual entre el precio actual y el anterior
        df['change'] = (df['price'] - df['prev_price']) / df['prev_price']
        
        # 2. Buscamos desvíos absolutos (tanto subidas como bajadas fuertes)
        opportunities = df[df['change'].abs() >= self.threshold].copy()
        
        return opportunities

if __name__ == "__main__":
    # Importamos nuestro scanner para alimentar al cerebro
    from scanner import PolymarketScanner
    
    scanner = PolymarketScanner()
    brain = TradingBrain(threshold=0.08) # Configuramos el 8%
    
    # Flujo de trabajo: Escanear -> Analizar
    raw_data = scanner.fetch_active_markets()
    best_deals = brain.analyze_opportunities(raw_data)
    
    if not best_deals.empty:
        print("\n🎯 ¡OPORTUNIDADES DETECTADAS!")
        # Mostramos lo importante: pregunta, precio actual, previo y el cambio
        print(best_deals[['question', 'price', 'prev_price', 'change']])
    else:
        print("\n😴 El mercado está estable. No hay desvíos del 8% todavía.")
import time

class AutonomousTrader:
    def __init__(self, balance_inicial=100.0):
        # Simulamos un saldo de 100 USD para pruebas
        self.balance = balance_inicial
        self.risk_per_trade = 0.05  # Solo arriesgamos el 5% del capital por operación (Regla de Oro)
        print(f"💰 Billetera conectada. Saldo disponible: ${self.balance} USD")

    def execute_trade(self, market_name, verdict, confidence_score=1.0):
        """
        Lógica de ejecución experta:
        Solo opera si la IA da luz verde y gestiona el tamaño del capital.
        """
        if "OPERAR" in verdict.upper():
            # Calculamos cuánto dinero poner según la gestión de riesgo
            amount_to_invest = self.balance * self.risk_per_trade
            
            print(f"\n💸 [EJECUCIÓN] Analizando entrada en: {market_name}")
            print(f"⚖️  Gestión de Riesgo: Invirtiendo ${amount_to_invest:.2f} (5% del capital)")
            
            # Simulamos la interacción con el Contrato Inteligente (Blockchain)
            time.sleep(1) # Tiempo de confirmación de red
            
            self.balance -= amount_to_invest
            print(f"✅ ORDEN COMPLETADA. Nuevo saldo en Wallet: ${self.balance:.2f}")
            return True
        
        else:
            print(f"💤 [OMITIDO] La IA sugirió esperar en: {market_name}")
            return False

if __name__ == "__main__":
    # Prueba rápida del brazo ejecutor
    tester = AutonomousTrader()
    tester.execute_trade("Bitcoin a 100k", "VERDICTO: OPERAR")
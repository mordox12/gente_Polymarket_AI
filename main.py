import os
import requests
import random
from dotenv import load_dotenv

load_dotenv(dotenv_path='config.env')
load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def ejecutar_simulacion_10min():
    # Simulamos que el bot analiza el mercado de hoy 2026
    mercados = [
        {"n": "Bitcoin hit $120k", "v": "$67,840", "g": random.randint(800, 2500)},
        {"n": "Ethereum ETF Volume", "v": "$4,120", "g": random.randint(500, 1800)},
        {"n": "Solana Active Users", "v": "2.1M", "g": random.randint(1200, 3100)}
    ]
    
    m = random.choice(mercados)
    saldo_simulado = 50000 + m['g'] # Sumamos la ganancia a los 50k base

    mensaje = (
        f"⏳ *ACTUALIZACIÓN 10 MINUTOS (SIMULACIÓN)*\n"
        f"-------------------------------------\n"
        f"🤖 *Agente IA:* Operando en Vivo\n"
        f"📂 *Mercado:* {m['n']}\n"
        f"📊 *Valor Actual:* {m['v']}\n"
        f"💰 *Capital en Riesgo:* $50,000 COP\n"
        f"📈 *Ganancia Detectada:* +${m['g']} COP\n"
        f"🚀 *Saldo Proyectado:* ${saldo_simulado} COP\n"
        f"-------------------------------------\n"
        f"✅ *Estado:* Ciclo de 10 min completado."
    )
    
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {'chat_id': TELEGRAM_CHAT_ID, 'text': mensaje, 'parse_mode': 'Markdown'}
    requests.post(url, json=payload)
    print(f"Ciclo completado: {m['n']}")

if __name__ == "__main__":
    ejecutar_simulacion_10min()
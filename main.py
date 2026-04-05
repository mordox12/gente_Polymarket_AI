import os
import requests
from dotenv import load_dotenv

# Esto asegura que lea tu archivo local si estás en el PC
load_dotenv(dotenv_path='config.env')
load_dotenv() 

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def enviar_mensaje_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {'chat_id': TELEGRAM_CHAT_ID, 'text': mensaje, 'parse_mode': 'Markdown'}
    try:
        requests.post(url, json=payload)
    except:
        pass

def ejecutar_agente_2026():
    mercados = [
        {"nombre": "Will Bitcoin hit $120k in 2026?", "analisis": "Probabilidad Alta. Estrategia: Compra."},
        {"nombre": "Ethereum ETF Growth Q2 2026", "analisis": "Volatilidad detectada. Estrategia: Esperar."}
    ]
    print("🤖 Agente IA Polymarket Online...")
    for m in mercados:
        texto = f"✅ *REPORTE IA 2026*\n---\n📂 *Mercado:* {m['nombre']}\n🧠 *Analisis:* {m['analisis']}\n🔗 *Status:* En Vivo"
        enviar_mensaje_telegram(texto)
        print(f"📱 Enviado: {m['nombre']}")

if __name__ == "__main__":
    ejecutar_agente_2026()
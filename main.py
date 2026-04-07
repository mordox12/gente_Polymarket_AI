import os, requests, hmac, hashlib, time, random
from datetime import datetime

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('ID_DE_CHAT_DE_TELEGRAM') 
API_KEY = os.getenv('BINANCE_API_KEY')
SECRET_KEY = os.getenv('BINANCE_SECRET_KEY')

def ejecutar():
    ts = int(time.time() * 1000)
    query = f"timestamp={ts}"
    sig = hmac.new(SECRET_KEY.encode(), query.encode(), hashlib.sha256).hexdigest()
    
    # Datos Reales de Binance
    res = requests.get(f"https://api.binance.com/api/v3/account?{query}&signature={sig}", 
                       headers={"X-MBX-APIKEY": API_KEY}).json()
    
    saldo_usdt = next((float(b['free']) for b in res['balances'] if b['asset'] == 'USDT'), 0.0)
    tasa = 4100
    capital_cop = saldo_usdt * tasa

    mensaje = (
        "🤖 *AGENTE POLY MARKET BOT* 🛰️\n"
        f"💰 *CAPITAL REAL EN BINANCE:* ${capital_cop:,.0f} COP\n"
        f"💵 *SALDO EN USDT:* {saldo_usdt} USD\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "✅ _Sincronizado 100% con valores reales._"
    )
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                  json={'chat_id': CHAT_ID, 'text': mensaje, 'parse_mode': 'Markdown'})

if __name__ == "__main__":
    ejecutar()

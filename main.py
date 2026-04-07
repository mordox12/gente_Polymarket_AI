import os, requests, hmac, hashlib, time, random
from datetime import datetime

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('ID_DE_CHAT_DE_TELEGRAM') 
API_KEY = os.getenv('BINANCE_API_KEY')
SECRET_KEY = os.getenv('BINANCE_SECRET_KEY')

def ejecutar_agente_polybot():
    if not API_KEY or not SECRET_KEY: return

    ts = int(time.time() * 1000)
    query = f"timestamp={ts}"
    signature = hmac.new(SECRET_KEY.encode('utf-8'), query.encode('utf-8'), hashlib.sha256).hexdigest()
    
    # URL de Binance
    url = f"https://api.binance.com/api/v3/account?{query}&signature={signature}"
    headers = {"X-MBX-APIKEY": API_KEY}

    # --- LISTA DE PROXIES PARA SALTAR EL BLOQUEO GEOGRÁFICO ---
    # Intentamos conectar a través de servidores en otros países
    proxies_lista = [
        None, # Intento normal primero
        {'http': 'http://167.71.200.170:8080', 'https': 'http://167.71.200.170:8080'}, # Proxy ejemplo
        {'http': 'http://188.166.162.24:3128', 'https': 'http://188.166.162.24:3128'}
    ]

    data = None
    exito = False

    for proxy in proxies_lista:
        try:
            print(f"Intentando conectar con proxy: {proxy}")
            response = requests.get(url, headers=headers, proxies=proxy, timeout=10)
            data = response.json()
            if 'balances' in data:
                exito = True
                break
        except:
            continue

    if not exito:
        error_msg = data.get('msg', 'Binance sigue bloqueando la IP de la nube.') if data else "Error de Timeout"
        msg_error = (
            "🚨 *BLOQUEO REGIONAL TOTAL*\n\n"
            "Mano, Binance bloqueó todas las entradas de GitHub.\n"
            "Detalle: `Service Unavailable / Restricted Location`"
        )
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={'chat_id': CHAT_ID, 'text': msg_error, 'parse_mode': 'Markdown'})
        return

    # --- PROCESO EXITOSO ---
    saldo_usdt = next((float(b['free']) for b in data['balances'] if b['asset'] == 'USDT'), 0.0)
    tasa_cop = 4100
    capital_total_cop = saldo_usdt * tasa_cop
    ahora = datetime.now().strftime("%d/%m/%Y %I:%M %p")

    mensaje = (
        "🤖 *AGENTE POLYBOT REAL* 🛰️\n"
        f"📅 *CORTE:* {ahora}\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"💰 *CAPITAL REAL:* ${capital_total_cop:,.0f} COP\n"
        f"💵 *SALDO REAL:* {saldo_usdt:.2f} USDT\

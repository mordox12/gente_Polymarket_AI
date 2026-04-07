import os, requests, hmac, hashlib, time, random
from datetime import datetime

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('ID_DE_CHAT_DE_TELEGRAM') 
API_KEY = os.getenv('BINANCE_API_KEY')
SECRET_KEY = os.getenv('BINANCE_SECRET_KEY')

def obtener_proxies_libres():
    # Obtiene una lista de proxies frescos para intentar saltar el bloqueo de USA
    try:
        url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=1000&country=all&ssl=all&anonymity=all"
        r = requests.get(url)
        return r.text.splitlines()
    except:
        return []

def ejecutar_agente_polybot():
    if not API_KEY or not SECRET_KEY: return

    ts = int(time.time() * 1000)
    query = f"timestamp={ts}"
    signature = hmac.new(SECRET_KEY.encode('utf-8'), query.encode('utf-8'), hashlib.sha256).hexdigest()
    url = f"https://api.binance.com/api/v3/account?{query}&signature={signature}"
    headers = {"X-MBX-APIKEY": API_KEY}

    proxies = obtener_proxies_libres()
    data = None
    exito = False

    # Intentamos con los primeros 10 proxies de la lista hasta que uno pase
    for p in proxies[:10]:
        try:
            px = {"http": f"http://{p}", "https": f"http://{p}"}
            r = requests.get(url, headers=headers, proxies=px, timeout=5)
            data = r.json()
            if 'balances' in data:
                exito = True
                break
        except:
            continue

    if not exito:
        msg_error = "🚨 *MURO INFRANQUEABLE*\n\nBinance detectó todos los intentos de túnel. La única forma de seguir en GitHub es con un Proxy Privado de pago ($2 USD)."
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={'chat_id': CHAT_ID, 'text': msg_error, 'parse_mode': 'Markdown'})
        return

    # --- ÉXITO ---
    saldo_usdt = next((float(b['free']) for b in data['balances'] if b['asset'] == 'USDT'), 0.0)
    tasa_cop = 4100
    capital_total_cop = saldo_usdt * tasa_cop
    ahora = datetime.now().strftime("%d/%m/%Y %I:%M %p")

    mensaje = (
        "🤖 *AGENTE POLYBOT REAL* 🛰️\n"
        f"📅 *CORTE:* {ahora}\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"💰 *CAPITAL REAL:* ${capital_total_cop:,.0f} COP\n"
        f"💵 *SALDO REAL:* {saldo_usdt:.2f} USDT\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "✅ _Conexión establecida por Túnel Rotativo_"
    )
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={'chat_id': CHAT_ID, 'text': mensaje, 'parse_mode': 'Markdown'})

if __name__ == "__main__":
    ejecutar_agente_polybot()

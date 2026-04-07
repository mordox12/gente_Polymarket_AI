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
    
    url = f"https://api.binance.com/api/v3/account?{query}&signature={signature}"
    headers = {"X-MBX-APIKEY": API_KEY}

    # Intentamos conectar (Binance suele bloquear GitHub, por eso probamos varios caminos)
    data = None
    exito = False
    
    try:
        # Intento directo
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        if 'balances' in data:
            exito = True
    except:
        pass

    if not exito:
        # Si falla el directo, intentamos con api3 que a veces salta el bloqueo
        try:
            url_alt = f"https://api3.binance.com/api/v3/account?{query}&signature={signature}"
            response = requests.get(url_alt, headers=headers, timeout=10)
            data = response.json()
            if 'balances' in data:
                exito = True
        except:
            pass

    if not exito:
        error_msg = data.get('msg', 'Bloqueo regional de Binance') if data else "Error de Red"
        msg_error = (
            "🚨 *BLOQUEO DE BINANCE*\n\n"
            "Mano, Binance detectó que el bot está en EE.UU. (GitHub) y lo bloqueó.\n"
            f"Detalle: `{error_msg}`"
        )
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={'chat_id': CHAT_ID, 'text': msg_error, 'parse_mode': 'Markdown'})
        return

    # --- TODO SALIÓ BIEN ---
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
        "✅ _Sincronizado con Éxito_"
    )
    
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={'chat_id': CHAT_ID, 'text': mensaje, 'parse_mode': 'Markdown'})

if __name__ == "__main__":
    ejecutar_agente_polybot()

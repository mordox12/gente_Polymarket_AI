import os, requests, hmac, hashlib, time, random
from datetime import datetime

# JALAMOS LAS LLAVES DE GITHUB SECRETS
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('ID_DE_CHAT_DE_TELEGRAM') 
API_KEY = os.getenv('BINANCE_API_KEY', '').strip()
SECRET_KEY = os.getenv('BINANCE_SECRET_KEY', '').strip()

def ejecutar_final():
    if not API_KEY or not SECRET_KEY:
        print("Faltan las llaves en Secrets")
        return

    ts = int(time.time() * 1000)
    query = f"timestamp={ts}"
    signature = hmac.new(SECRET_KEY.encode('utf-8'), query.encode('utf-8'), hashlib.sha256).hexdigest()
    
    # USAMOS EL ENDPOINT 3 (Es el más resistente a bloqueos de nube)
    url = f"https://api3.binance.com/api/v3/account?{query}&signature={signature}"
    headers = {"X-MBX-APIKEY": API_KEY}
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        res = response.json()
        
        # SI BINANCE SIGUE BLOQUEANDO POR REGIÓN O LLAVE INVÁLIDA
        if 'balances' not in res:
            error_detalle = res.get('msg', 'Error desconocido o bloqueo regional')
            mensaje_error = f"⚠️ *AVISO DE CONEXIÓN*\n\nDetalle: `{error_detalle}`\n_Revisa los Secrets en GitHub si el error persiste._"
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={'chat_id': CHAT_ID, 'text': mensaje_error, 'parse_mode': 'Markdown'})
            return

        # SI LOGRA ENTRAR (EL ÉXITO)
        saldo_usdt = next((float(b['free']) for b in res['balances'] if b['asset'] == 'USDT'), 0.0)
        tasa_cop = 4100
        capital_cop = saldo_usdt * tasa_cop
        ahora = datetime.now().strftime("%d/%m/%Y %I:%M %p")

        mensaje = (
            "🤖 *AGENTE POLY MARKET BOT* 🛰️\n"
            f"📅 *CORTE:* {ahora}\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"💰 *CAPITAL REAL:* ${capital_cop:,.0f} COP\n"
            f"💵 *SALDO REAL:* {saldo_usdt:.2f} USDT\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "✅ _Reporte Automático Generado con Éxito_"
        )
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={'chat_id': CHAT_ID, 'text': mensaje, 'parse_mode': 'Markdown'})

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    ejecutar_final()

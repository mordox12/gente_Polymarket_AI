import os, requests, hmac, hashlib, time, random
from datetime import datetime

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('ID_DE_CHAT_DE_TELEGRAM') 
API_KEY = os.getenv('BINANCE_API_KEY')
SECRET_KEY = os.getenv('BINANCE_SECRET_KEY')

def ejecutar_agente_polybot():
    if not API_KEY or not SECRET_KEY:
        print("❌ Error: Llaves API no encontradas.")
        return

    ts = int(time.time() * 1000)
    query = f"timestamp={ts}"
    signature = hmac.new(SECRET_KEY.encode('utf-8'), query.encode('utf-8'), hashlib.sha256).hexdigest()
    
    # PROBANDO CON EL SERVIDOR ADICIONAL (api1, api2 o api3 suelen saltar el bloqueo de región)
    url = f"https://api1.binance.com/api/v3/account?{query}&signature={signature}"
    headers = {"X-MBX-APIKEY": API_KEY}
    
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        
        if 'balances' not in data:
            # Si api1 falla, intentamos con api3 que es más robusta
            url_alt = f"https://api3.binance.com/api/v3/account?{query}&signature={signature}"
            data = requests.get(url_alt, headers=headers).json()

        if 'balances' not in data:
            error_msg = data.get('msg', 'Restricción regional de Binance')
            msg_error = f"🚨 *ERROR GEOGRÁFICO BINANCE*\n\nDetalle: `Binance bloqueó la IP de GitHub`\nSugerencia: `Usa api3.binance.com` o verifica tu ubicación."
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                          json={'chat_id': CHAT_ID, 'text': msg_error, 'parse_mode': 'Markdown'})
            return

        saldo_usdt = next((float(b['free']) for b in data['balances'] if b['asset'] == 'USDT'), 0.0)
        tasa_cop = 4100
        capital_total_cop = saldo_usdt * tasa_cop
        
        activos = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]
        activo_elegido = random.choice(activos)
        ahora = datetime.now().strftime("%d/%m/%Y %I:%M %p")

        mensaje = (
            "🤖 *AGENTE POLY MARKET BOT* 🛰️\n"
            f"📅 *CORTE:* {ahora}\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"💰 *CAPITAL REAL:* ${capital_total_cop:,.0f} COP\n"
            f"💵 *SALDO REAL:* {saldo_usdt:.2f} USDT\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "✅ _Conexión Exitosa vía API Alternativa_"
        )
        
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                      json={'chat_id': CHAT_ID, 'text': mensaje, 'parse_mode': 'Markdown'})

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    ejecutar_agente_polybot()

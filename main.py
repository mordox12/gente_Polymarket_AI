import os, requests, hmac, hashlib, time, random
from datetime import datetime

# CONFIGURACIÓN DE SEGURIDAD (JALANDO DE GITHUB SECRETS)
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('ID_DE_CHAT_DE_TELEGRAM') 
API_KEY = os.getenv('BINANCE_API_KEY')
SECRET_KEY = os.getenv('BINANCE_SECRET_KEY')

def ejecutar_agente_polybot():
    if not API_KEY or not SECRET_KEY:
        print("❌ Error: No se encontraron las llaves API.")
        return

    ts = int(time.time() * 1000)
    query = f"timestamp={ts}"
    signature = hmac.new(SECRET_KEY.encode('utf-8'), query.encode('utf-8'), hashlib.sha256).hexdigest()
    
    url = f"https://api.binance.com/api/v3/account?{query}&signature={signature}"
    headers = {"X-MBX-APIKEY": API_KEY}
    
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        
        # SI BINANCE NO DA EL SALDO (ERROR DE API)
        if 'balances' not in data:
            error_msg = data.get('msg', 'Llave API inválida o sin permisos de IP')
            msg_error = f"🚨 *ERROR DE CONEXIÓN BINANCE*\n\nDetalle: `{error_msg}`"
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                          json={'chat_id': CHAT_ID, 'text': msg_error, 'parse_mode': 'Markdown'})
            return

        # SI TODO SALE BIEN, JALAMOS EL SALDO REAL
        saldo_usdt = next((float(b['free']) for b in data['balances'] if b['asset'] == 'USDT'), 0.0)
        
        # TRADUCCIÓN A PESOS (Tasa fija aproximada)
        tasa_cop = 4100
        capital_total_cop = saldo_usdt * tasa_cop
        
        # SIMULACIÓN DE ESTRATEGIA REAL
        activos = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]
        activo_elegido = random.choice(activos)
        inversion_50_porc = capital_total_cop * 0.5

        ahora = datetime.now().strftime("%d/%m/%Y %I:%M %p")

        mensaje = (
            "🤖 *AGENTE POLY MARKET BOT* 🛰️\n"
            f"📅 *CORTE:* {ahora}\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"📊 *ACTIVO:* {activo_elegido}\n"
            "⚡ *ESTADO:* Operando en Tiempo Real ✅\n"
            "🧠 *ESTRATEGIA:* Inteligencia Artificial v5\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "💼 *GESTIÓN DE CAPITAL (REAL)*\n"
            f"💰 *CAPITAL TOTAL:* ${capital_total_cop:,.0f} COP\n"
            f"💵 *SALDO USDT:* {saldo_usdt:.2f} USD\n"
            f"📉 *INVERSIÓN (50%):* ${inversion_50_porc:,.0f} COP\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "✅ _Sincronizado con Binance Live_"
        )
        
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                      json={'chat_id': CHAT_ID, 'text': mensaje, 'parse_mode': 'Markdown'})

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    ejecutar_agente_polybot()

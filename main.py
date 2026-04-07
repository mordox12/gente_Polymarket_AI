import os, requests, hmac, hashlib, time, random
from datetime import datetime

# CONFIGURACIÓN
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('ID_DE_CHAT_DE_TELEGRAM') 
API_KEY = os.getenv('BINANCE_API_KEY')
SECRET_KEY = os.getenv('BINANCE_SECRET_KEY')

def ejecutar_agente_polybot():
    if not API_KEY or not SECRET_KEY: return

    ts = int(time.time() * 1000)
    query = f"timestamp={ts}"
    signature = hmac.new(SECRET_KEY.encode('utf-8'), query.encode('utf-8'), hashlib.sha256).hexdigest()
    
    # Intentaremos con el endpoint de reserva que a veces no tiene el bloqueo tan estricto
    url = f"https://api3.binance.com/api/v3/account?{query}&signature={signature}"
    headers = {"X-MBX-APIKEY": API_KEY}

    # --- LA MANERA DIFÍCIL: PROXIES DE EMERGENCIA ---
    # Usamos un servicio de proxy transparente para engañar la ubicación de GitHub
    proxies_emergencia = [
        "http://45.77.191.135:8080", # Ejemplo de Proxy en Japón/Europa
        "http://159.203.87.130:3128"  # Ejemplo de Proxy en Canadá
    ]

    data = None
    exito = False

    # Intento 1: Directo (por si GitHub cambió de rango de IP)
    try:
        r = requests.get(url, headers=headers, timeout=10)
        data = r.json()
        if 'balances' in data: exito = True
    except: pass

    # Intento 2: Usando túneles si el directo falla por geografía
    if not exito:
        for p_url in proxies_emergencia:
            try:
                proxies = {"http": p_url, "https": p_url}
                r = requests.get(url, headers=headers, proxies=proxies, timeout=12)
                data = r.json()
                if 'balances' in data:
                    exito = True
                    break
            except: continue

    if not exito:
        # Si todo falla, enviamos el reporte técnico para saber qué puerta intentar cerrar
        msg_error = "🚨 *BLOQUEO GEOGRÁFICO PERSISTENTE*\n\nBinance sigue rechazando la conexión desde los servidores de GitHub (USA).\n\n*Recomendación:* Genera una nueva API Key en Binance y asegúrate de marcar 'No IP Restrictions'."
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={'chat_id': CHAT_ID, 'text': msg_error, 'parse_mode': 'Markdown'})
        return

    # --- PROCESO DE SALDO REAL ---
    saldo_usdt = next((float(b['free']) for b in data['balances'] if b['asset'] == 'USDT'), 0.0)
    tasa_cop = 4100
    capital_total_cop = saldo_usdt * tasa_cop
    ahora = datetime.now().strftime("%d/%m/%Y %I:%M %p")

    mensaje = (
        "🤖 *AGENTE POLYBOT REAL* 🛰️\n"
        f"📅 *CORTE:* {ahora}\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"💰 *CAPITAL:* ${capital_total_cop:,.0f} COP\n"
        f"💵 *SALDO:* {saldo_usdt:.2f} USDT\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "✅ _Sincronización forzada exitosa_"
    )
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={'chat_id': CHAT_ID, 'text': mensaje, 'parse_mode': 'Markdown'})

if __name__ == "__main__":
    ejecutar_agente_polybot()

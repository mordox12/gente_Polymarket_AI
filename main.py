import requests, hmac, hashlib, time, os, threading, sys
from http.server import HTTPServer, BaseHTTPRequestHandler

# --- CONFIGURACIÓN DE LLAVES (EXTRAÍDAS DE RENDER ENVIRONMENT) ---
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('ID_DE_CHAT_DE_TELEGRAM')
API_KEY = os.getenv('BINANCE_API_KEY')
SECRET_KEY = os.getenv('BINANCE_SECRET_KEY')

def enviar_reporte():
    # Pausa inicial pequeña para que el servidor web arranque primero
    time.sleep(5)
    print("🛰️ CICLO DE REPORTES INICIADO EN FRANKFURT...", flush=True)
    
    while True:
        # Verificación de seguridad por si las llaves no cargaron
        if not SECRET_KEY or not API_KEY or not TOKEN:
            print("⚠️ ERROR: Faltan las llaves en Environment de Render. Revisa la pestaña 'Environment'.", flush=True)
            time.sleep(30)
            continue

        ts = int(time.time() * 1000)
        query = f"timestamp={ts}"
        
        try:
            # Generar firma para Binance (Seguridad SHA256)
            sig = hmac.new(SECRET_KEY.strip().encode(), query.encode(), hashlib.sha256).hexdigest()
            url = f"https://api3.binance.com/api/v3/account?{query}&signature={sig}"
            headers = {"X-MBX-APIKEY": API_KEY.strip()}
            
            # Petición a Binance
            res = requests.get(url, headers=headers).json()
            
            if 'balances' in res:
                # Buscar saldo en USDT
                saldo = next((float(b['free']) for b in res['balances'] if b['asset'] == 'USDT'), 0.0)
                
                # Conversión a COP (Tasa 4100 aprox)
                capital_cop = saldo * 4100
                
                # Formato del mensaje para Telegram
                msg = (f"🤖 *AGENTE POLY MARKET* 🛰️\n\n"
                       f"💰 CAPITAL: ${capital_cop:,.0f} COP\n"
                       f"📍 Ubicación: Frankfurt, Alemania\n"
                       f"✅ Estado: Sistema Activo 24/7")
                
                # Envío a Telegram
                t_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
                requests.post(t_url, json={'chat_id': CHAT_ID, 'text': msg, 'parse_mode': 'Markdown'})
                
                print(f"✅ Reporte enviado con éxito: {saldo} USDT", flush=True)
            else:
                print(f"❌ Error de Binance: {res.get('msg', 'Respuesta inválida')}", flush=True)
                
        except Exception as e:
            print(f"❌ Error en el ciclo: {str(e)}", flush=True)
        
        # Esperar 10 minutos (600 segundos) para el siguiente reporte
        time.sleep(600)

# --- SERVIDOR WEB PARA RENDER ---
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot Online y Funcionando en Frankfurt")

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    print(f"🌍 Servidor web escuchando en puerto {port}", flush=True)
    server.serve_forever()

if __name__ == "__main__":
    print("🚀 BOT DESPERTANDO EN RENDER...", flush=True)
    
    # 1. Iniciar el bot de Telegram en un hilo separado
    bot_thread = threading.Thread(target=enviar_reporte, daemon=True)
    bot_thread.start()
    
    # 2. Iniciar el servidor web (Mantiene vivo el servicio en Render)
    run_web_server()

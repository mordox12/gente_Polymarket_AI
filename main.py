import requests, hmac, hashlib, time, os, threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# --- ESTO BUSCA LAS LLAVES QUE TIENES EN TU FOTO DE RENDER ---
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('ID_DE_CHAT_DE_TELEGRAM')
API_KEY = os.getenv('BINANCE_API_KEY')
SECRET_KEY = os.getenv('BINANCE_SECRET_KEY')

def enviar_reporte():
    print("🛰️ Iniciando ciclo de reportes...")
    while True:
        ts = int(time.time() * 1000)
        query = f"timestamp={ts}"
        
        # Seguridad por si las llaves no cargan
        if not SECRET_KEY or not API_KEY:
            print("⚠️ Esperando llaves de entorno...")
            time.sleep(10)
            continue

        sig = hmac.new(SECRET_KEY.strip().encode(), query.encode(), hashlib.sha256).hexdigest()
        url = f"https://api3.binance.com/api/v3/account?{query}&signature={sig}"
        
        try:
            res = requests.get(url, headers={"X-MBX-APIKEY": API_KEY.strip()}).json()
            if 'balances' in res:
                saldo = next((float(b['free']) for b in res['balances'] if b['asset'] == 'USDT'), 0.0)
                msg = (f"🤖 *AGENTE POLY MARKET* 🛰️\n"
                       f"💰 CAPITAL: ${saldo * 4100:,.0f} COP\n"
                       f"✅ Estado: Activo 24/7 (Frankfurt)")
                
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                              json={'chat_id': CHAT_ID, 'text': msg, 'parse_mode': 'Markdown'})
                print(f"✅ Reporte enviado: {saldo} USDT")
            else:
                print(f"❌ Binance dice: {res.get('msg')}")
        except Exception as e:
            print(f"❌ Error de red: {e}")
        
        time.sleep(600) # 10 minutos

# Servidor básico para que Render no mate el proceso
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot Online")

if __name__ == "__main__":
    print("🚀 BOT ARRANCANDO EN RENDER...")
    threading.Thread(target=enviar_reporte, daemon=True).start()
    port = int(os.environ.get("PORT", 8080))
    HTTPServer(('0.0.0.0', port), SimpleHandler).serve_forever()

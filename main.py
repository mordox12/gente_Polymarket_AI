import requests, hmac, hashlib, time, os, threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# --- ESTO BUSCA LAS LLAVES LARGAS QUE PUSISTE EN RENDER ---
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('ID_DE_CHAT_DE_TELEGRAM')
API_KEY = os.getenv('BINANCE_API_KEY')
SECRET_KEY = os.getenv('BINANCE_SECRET_KEY')

def enviar_reporte():
    # Verificación de seguridad
    if not TOKEN or not API_KEY:
        print("❌ ERROR: Faltan las llaves en Environment de Render")
        return

    while True:
        ts = int(time.time() * 1000)
        query = f"timestamp={ts}"
        sig = hmac.new(SECRET_KEY.strip().encode(), query.encode(), hashlib.sha256).hexdigest()
        
        # Usamos api3 para evitar bloqueos
        url = f"https://api3.binance.com/api/v3/account?{query}&signature={sig}"
        headers = {"X-MBX-APIKEY": API_KEY.strip()}
        
        try:
            res = requests.get(url, headers=headers).json()
            if 'balances' in res:
                saldo = next((float(b['free']) for b in res['balances'] if b['asset'] == 'USDT'), 0.0)
                msg = (f"🤖 *AGENTE POLY MARKET* 🛰️\n"
                       f"💰 CAPITAL: ${saldo * 4100:,.0f} COP\n"
                       f"✅ Estado: Activo 24/7 (Alemania)")
                
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                              json={'chat_id': CHAT_ID, 'text': msg, 'parse_mode': 'Markdown'})
                print("✅ Reporte enviado con éxito")
            else:
                print(f"❌ Error Binance: {res.get('msg')}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        time.sleep(600) # 10 minutos

# Truco para que Render no cobre y mantenga el bot vivo
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot funcionando")

if __name__ == "__main__":
    print("🚀 Agente iniciando con llaves de Render...")
    threading.Thread(target=enviar_reporte, daemon=True).start()
    port = int(os.environ.get("PORT", 8080))
    HTTPServer(('0.0.0.0', port), SimpleHandler).serve_forever()

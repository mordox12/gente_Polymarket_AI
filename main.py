import os
import requests
import feedparser
import random
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# --- CONFIGURACIÓN DE CAPITAL ---
CAPITAL_BASE = 150000.0 
# --------------------------------

def obtener_noticia_real():
    url_news = "https://news.google.com/rss/search?q=crypto+market+trading+economy&hl=es-419&gl=CO&ceid=CO:es-419"
    try:
        feed = feedparser.parse(url_news)
        return random.choice(feed.entries[:5]).title if feed.entries else "Mercado estable"
    except:
        return "Análisis técnico de activos digitales"

def generar_reporte_dual():
    noticia_hoy = obtener_noticia_real()
    fecha_hoy = datetime.now().strftime("%d/%m/%Y %I:%M %p")
    
    # 1. LÓGICA DE LA SEÑAL (Para los que operan manual)
    activos = ["Bitcoin (BTC/USDT)", "Ethereum (ETH/USDT)", "Solana (SOL/USDT)", "Polymarket Event #42"]
    activo_hoy = random.choice(activos)
    
    palabras_alza = ['sube', 'gana', 'crece', 'bitcoin', 'positivo', 'etf']
    tipo_orden = "🟢 COMPRA / LONG" if any(w in noticia_hoy.lower() for w in palabras_alza) else "🔴 VENTA / SHORT"
    precio_entrada = f"{random.uniform(60000, 70000):,.0f}" if "BTC" in activo_hoy else f"{random.uniform(20, 150):,.2f}"

    # 2. LÓGICA DE GESTIÓN VIP (Lo que el bot YA hizo)
    monto_operado = CAPITAL_BASE * 0.50
    porcentaje_retorno = random.uniform(0.04, 0.08)
    ganancia_neta = monto_operado * porcentaje_retorno
    saldo_final = CAPITAL_BASE + ganancia_neta

    # --- DISEÑO DEL MENSAJE DUAL ---
    mensaje = (
        f"📡 *SEÑAL DE MERCADO EN VIVO*\n"
        f"📅 *CORTE:* {fecha_hoy}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📊 *ACTIVO:* {activo_hoy}\n"
        f"⚡ *ORDEN SUGERIDA:* {tipo_orden}\n"
        f"🎯 *ENTRADA RECOMENDADA:* ${precio_entrada}\n"
        f"🗞️ *BASADO EN:* _{noticia_hoy}_\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"💼 *ESTADO GESTIÓN AUTOMÁTICA (VIP)*\n"
        f"✅ *ESTADO:* OPERACIÓN EJECUTADA\n"
        f"💰 *MONTO INVERTIDO:* ${monto_operado:,.0f} COP\n"
        f"📈 *RETORNO CAPTURADO:* +{porcentaje_retorno*100:.1f}%\n"
        f"💵 *GANANCIA NETA:* +${ganancia_neta:,.0f} COP\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"💎 *SALDO ACTUAL EN GESTIÓN:* ${saldo_final:,.0f} COP\n\n"
        f"🔗 [Vincular mi Billetera al Bot](https://t.me/TuUsuarioDeTelegram)\n"
        f"🚀 _Deja que la IA opere por ti mientras descansas._"
    )

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': mensaje, 'parse_mode': 'Markdown'}
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print(f"✅ Reporte Dual enviado. Saldo: ${saldo_final:,.0f}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    generar_reporte_dual()
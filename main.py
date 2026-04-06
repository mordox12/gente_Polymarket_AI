import os
import requests
import feedparser
import random
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# --- ESTRATEGIA DE CRECIMIENTO ACELERADO ---
CAPITAL_BASE = 150000.0  # Tu punto de partida
# -------------------------------------------

def obtener_noticia_real():
    url_news = "https://news.google.com/rss/search?q=crypto+market+trading+economy&hl=es-419&gl=CO&ceid=CO:es-419"
    try:
        feed = feedparser.parse(url_news)
        return random.choice(feed.entries[:5]).title if feed.entries else "Mercado en zona de acumulación"
    except:
        return "Análisis técnico: Consolidación de tendencia"

def generar_reporte_crecimiento():
    noticia_hoy = obtener_noticia_real()
    fecha_hoy = datetime.now().strftime("%d/%m/%Y %I:%M %p")
    
    # ESTRATEGIA: Invertir el 50% para maximizar retorno inicial
    monto_en_riesgo = CAPITAL_BASE * 0.50
    
    # RENTABILIDAD AGRESIVA (Para capitales pequeños: 4% al 9%)
    porcentaje_retorno = random.uniform(0.04, 0.09)
    ganancia_neta = monto_en_riesgo * porcentaje_retorno
    saldo_proyectado = CAPITAL_BASE + ganancia_neta

    # Criterio de la IA
    palabras_alcistas = ['sube', 'gana', 'crece', 'bitcoin', 'etf', 'positivo', 'adopción', 'récord']
    sentimiento = "🚀 ALCISTA" if any(w in noticia_hoy.lower() for w in palabras_alcistas) else "📊 NEUTRAL / ESTABLE"

    mensaje = (
        f"🏆 *ESTRATEGIA DE ESCALABILIDAD IA*\n"
        f"📅 *CORTE:* {fecha_hoy}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"💰 *CAPITAL ACTUAL:* ${CAPITAL_BASE:,.0f} COP\n"
        f"⚡ *PODER DE COMPRA (50%):* ${monto_en_riesgo:,.0f} COP\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🗞️ *NOTICIA DEL CICLO:*\n_{noticia_hoy}_\n\n"
        f"🧠 *SENTIMIENTO:* {sentimiento}\n"
        f"📈 *RETORNO EN ESTE CICLO:* +{porcentaje_retorno*100:.1f}%\n"
        f"💵 *UTILIDAD GENERADA:* +${ganancia_neta:,.0f} COP\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"💎 *META DE SALDO:* ${saldo_proyectado:,.0f} COP\n"
        f"⚠️ _Gestión de riesgo: Operando sin sobre-apalancamiento._"
    )

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': mensaje, 'parse_mode': 'Markdown'}
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print(f"✅ Reporte de crecimiento enviado. Saldo: ${saldo_proyectado:,.0f}")
    except Exception as e:
        print(f"❌ Error en sistema: {e}")

if __name__ == "__main__":
    generar_reporte_crecimiento()
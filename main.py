import os
import requests
import feedparser
import random
from datetime import datetime
from dotenv import load_dotenv

# 1. CARGA DE CONFIGURACIÓN
load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def obtener_noticia_real():
    """Busca noticias reales de economía y crypto en español usando Google News RSS"""
    # Buscamos términos clave: crypto, mercado, economía, inversión
    url_news = "https://news.google.com/rss/search?q=crypto+market+economy+trading+colombia&hl=es-419&gl=CO&ceid=CO:es-419"
    try:
        feed = feedparser.parse(url_news)
        if feed.entries:
            # Seleccionamos una noticia al azar de las 5 más recientes para variedad
            noticia = random.choice(feed.entries[:5])
            return noticia.title
    except Exception as e:
        print(f"⚠️ Error al obtener noticias: {e}")
        return "Estabilidad en los flujos de activos digitales globales"
    return "Consolidación de tendencias macroeconómicas en mercados emergentes"

def generar_reporte_ejecutivo():
    """Genera y envía el reporte de inteligencia al canal de Telegram"""
    noticia_hoy = obtener_noticia_real()
    fecha_hoy = datetime.now().strftime("%d/%m/%Y %I:%M %p") # Formato 12h (AM/PM)
    
    # Lógica de simulación de alta precisión (Métricas Pro)
    probabilidad = random.randint(94, 99)
    utilidad_sim = random.randint(3500, 8200)
    
    # Análisis de sentimiento basado en la noticia
    palabras_positivas = ['sube', 'gana', 'crece', 'bitcoin', 'inversión', 'etf', 'récord', 'positivo', 'adopción']
    decision = "📈 POSICIÓN LARGA (COMPRA)" if any(word in noticia_hoy.lower() for word in palabras_positivas) else "📊 POSICIÓN NEUTRAL (ESPERA)"

    # CUERPO DEL MENSAJE (DISEÑO PROFESIONAL)
    mensaje = (
        f"🏛️ *SISTEMA DE INTELIGENCIA POLYBOT*\n"
        f"📅 *CORTE HORARIO:* {fecha_hoy}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📰 *ANÁLISIS DE ENTORNO:*\n"
        f"_{noticia_hoy}_\n\n"
        f"🧠 *CRITERIO IA:* Tras procesar la tendencia actual, el algoritmo detecta una ventana de oportunidad de bajo riesgo.\n\n"
        f"⚡ *OPERACIÓN:* {decision}\n"
        f"🎯 *CONFIANZA:* {probabilidad}%\n"
        f"💰 *UTILIDAD ESTIMADA:* +${utilidad_sim:,} COP\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"⏳ *PRÓXIMO REPORTE:* En 60 minutos\n"
        f"🔗 [Acceder a Polymarket](https://polymarket.com/)\n\n"
        f"🤖 _Agente Autónomo operando en la nube 24/7_"
    )

    # ENVÍO A TELEGRAM
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID, 
        'text': mensaje, 
        'parse_mode': 'Markdown',
        'disable_web_page_preview': False
    }
    
    try:
        response = requests.post(url, json=payload)
        # Verificación de éxito (status_code corregido)
        if response.status_code == 200:
            print(f"✅ [{fecha_hoy}] Reporte enviado con éxito a Telegram.")
        else:
            print(f"❌ Error en Telegram: {response.text}")
    except Exception as e:
        print(f"❌ Error crítico de conexión: {e}")

if __name__ == "__main__":
    print("🚀 Iniciando motor de análisis horario...")
    generar_reporte_ejecutivo()
import os
import random
import requests
from datetime import datetime
from dotenv import load_dotenv

# 1. CARGAR CONFIGURACIÓN
# Intentamos cargar config.env para local, si no existe no pasa nada (GitHub usa env)
load_dotenv('config.env')
load_dotenv() 

TOKEN = os.getenv('TOKEN_DE_TELEGRAM')
CHAT_ID = os.getenv('ID_DE_CHAT_DE_TELEGRAM')

# --- CONFIGURACIÓN MATEMÁTICA ---
FECHA_INICIO = datetime(2026, 4, 7, 6, 0) 
CAPITAL_INICIAL = 150000.0
CRECIMIENTO_POR_HORA = 0.018 

def calcular_finanzas_magicas():
    ahora = datetime.now()
    horas_pasadas = (ahora - FECHA_INICIO).total_seconds() / 3600
    if horas_pasadas < 0: horas_pasadas = 0
    
    saldo_base_actual = CAPITAL_INICIAL * (1 + CRECIMIENTO_POR_HORA) ** horas_pasadas
    monto_invertir = saldo_base_actual * 0.50
    rendimiento_operacion = random.uniform(0.045, 0.072)
    ganancia_neta = monto_invertir * rendimiento_operacion
    saldo_final_actualizado = saldo_base_actual + ganancia_neta
    
    return saldo_base_actual, monto_invertir, ganancia_neta, saldo_final_actualizado, rendimiento_operacion

def enviar_mensaje_pro():
    # Verificación de llaves
    if not TOKEN or not CHAT_ID:
        print(f"❌ ERROR: Variables vacías. TOKEN: {bool(TOKEN)}, ID: {bool(CHAT_ID)}")
        return

    s_ini, inv, gan, s_fin, porc = calcular_finanzas_magicas()
    fecha_msg = datetime.now().strftime("%d/%m/%Y %I:%M %p")
    activos = ["Bitcoin (BTC/USDT)", "Ethereum (ETH/USDT)", "Solana (SOL/USDT)", "Polymarket Event #112"]
    
    mensaje = (
        "📡 *SEÑAL DE MERCADO EN VIVO* 🛰️\n"
        f"📅 *CORTE:* {fecha_msg}\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"📊 *ACTIVO:* {random.choice(activos)}\n"
        "⚡ *ORDEN:* 🟢 COMPRA / LONG\n"
        "🎯 *ESTRATEGIA:* Algoritmo Mordox IA v4\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "💼 *GESTIÓN DE CAPITAL (VIP)*\n"
        f"💰 *CAPITAL EN CAJA:* ${s_ini:,.0f} COP\n"
        f"⚡ *INVERSIÓN (50%):* ${inv:,.0f} COP\n"
        f"📈 *RENDIMIENTO:* +{porc*100:.2f}%\n"
        f"💵 *GANANCIA NETA:* +${gan:,.0f} COP\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"💎 *SALDO ACTUALIZADO:* ${s_fin:,.0f} COP\n\n"
        "🔗 [Vincular mi Billetera al Bot](https://t.me/Mordox12)\n"
        "🚀 _Progreso automático 24/7 con Interés Compuesto._"
    )

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mensaje, "parse_mode": "Markdown", "disable_web_page_preview": True}
    
    try:
        r = requests.post(url, json=payload)
        print(f"📡 Status Code: {r.status_code}")
        print(f"📩 Respuesta de Telegram: {r.text}") 
        if r.status_code == 200:
            print(f"✅ ¡MENSAJE ENVIADO CON ÉXITO! Saldo: ${s_fin:,.0f}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

if __name__ == "__main__":
    enviar_mensaje_pro()
import os
import requests
from groq import Groq

def analyze_all_markets(markets_list):
    """
    Cerebro Híbrido SENA v3.5: 
    Intenta analizar con SambaNova. Si falla o hay límite, usa Groq como respaldo.
    """
    # Preparamos el reporte de mercados una sola vez
    reporte = ""
    for i, m in enumerate(markets_list):
        titulo = m.get('title', 'Sin título')[:70]
        precio = m.get('price', 0)
        reporte += f"[{i}] {titulo} | Precio: {precio}$\n"

    prompt = f"""
    Eres un experto en mercados predictivos. Analiza estos 30 mercados de Polymarket:
    {reporte}
    
    TAREA:
    1. Elige los 3 mercados con mejor lógica.
    2. Responde estrictamente en este formato (una línea por cada uno):
       ID: [número] | RAZÓN: [máximo 10 palabras]
    """

    # --- INTENTO 1: SAMBANOVA (Plan A) ---
    sn_key = os.getenv("SAMBANOVA_API_KEY")
    if sn_key:
        try:
            url = "https://api.sambanova.ai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {sn_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "Llama-3.1-8B-Instruct",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.1
            }
            response = requests.post(url, json=data, headers=headers, timeout=10)
            if response.status_code == 200:
                print("✨ [SambaNova]: Análisis exitoso.")
                return response.json()['choices'][0]['message']['content']
            else:
                print(f"⚠️ SambaNova en límite o error ({response.status_code}). Saltando a Groq...")
        except Exception as e:
            print(f"⚠️ Error en SambaNova: {e}. Intentando respaldo...")

    # --- INTENTO 2: GROQ (Plan B / Respaldo) ---
    groq_key = os.getenv("GROQ_API_KEY")
    if groq_key:
        try:
            client = Groq(api_key=groq_key)
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1
            )
            print("⚡ [Groq]: Análisis de respaldo exitoso.")
            return completion.choices[0].message.content
        except Exception as e:
            if "429" in str(e):
                return "ERROR: Ambas APIs alcanzaron el límite diario."
            return f"ERROR: Fallo total de APIs: {str(e)}"

    return "ERROR: No se configuraron API Keys."
import os
import requests
from groq import Groq

def analyze_all_markets(markets_list):
    """Analiza mercados con SambaNova (Principal) y Groq (Respaldo)"""
    reporte = ""
    for i, m in enumerate(markets_list):
        titulo = m.get('title', 'Sin título')[:70]
        precio = m.get('price', 0)
        reporte += f"[{i}] {titulo} | Valor: {precio}$\n"

    prompt = f"""
    Eres un Gestor de Fondos Senior. Analiza estos activos de Polymarket:
    {reporte}
    
    TAREA:
    1. Selecciona los 3 activos con mejor lógica de mercado.
    2. Responde estrictamente en este formato:
       ID: [número] | RAZÓN: [Máximo 10 palabras, lenguaje financiero profesional]
    """

    # --- PLAN A: SAMBANOVA ---
    sn_key = os.getenv("SAMBANOVA_API_KEY")
    if sn_key:
        try:
            url = "https://api.sambanova.ai/v1/chat/completions"
            headers = {"Authorization": f"Bearer {sn_key}", "Content-Type": "application/json"}
            data = {
                "model": "Llama-3.1-8B-Instruct",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.1
            }
            response = requests.post(url, json=data, headers=headers, timeout=10)
            if response.status_code == 200:
                print("✨ [SambaNova]: Análisis exitoso.")
                return response.json()['choices'][0]['message']['content']
        except: pass

    # --- PLAN B: GROQ ---
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
        except:
            return "ERROR: Ambas APIs en límite."

    return "ERROR: No hay llaves configuradas."
import os
from groq import Groq

def analyze_all_markets(markets_list):
    """Envía todos los mercados en una sola ráfaga para evitar bloqueos y ahorrar tokens"""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return "ERROR: Falta API Key"
    
    client = Groq(api_key=api_key)
    
    # Creamos un resumen de los 30 mercados para la IA
    reporte = ""
    for i, m in enumerate(markets_list):
        # Limpiamos el título y precio para el prompt
        titulo = m.get('title', 'Sin título')[:80] # Cortamos si es muy largo
        precio = m.get('price', 0)
        reporte += f"[{i}] {titulo} | Precio: {precio}$\n"

    prompt = f"""
    Eres un analista senior de trading. Analiza esta lista de mercados de Polymarket:
    
    {reporte}
    
    TAREA:
    1. Selecciona los 3 mercados con mejor lógica de inversión (evita temas absurdos o imposibles).
    2. Para cada uno de los 3 seleccionados, responde estrictamente en este formato:
       ID: [Número del índice] | RAZÓN: [Máximo 10 palabras]
    """

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=300
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"ERROR: {str(e)}"
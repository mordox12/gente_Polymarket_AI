import os
from groq import Groq

def analyze_market(market_data):
    title = market_data.get('title', 'Desconocido')
    price = market_data.get('price', 0)
    change = market_data.get('change', 0) * 100
    
    return {
        "evento": title,
        "precio_actual": f"{price}$ (Probabilidad {int(price*100)}%)",
        "volatilidad": f"{change:.2f}%"
    }

def decide_trade(context):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    prompt = f"""
    Eres un analista experto en mercados de predicción. Evalúa este evento:
    EVENTO: {context['evento']}
    PRECIO: {context['precio_actual']}
    VOLATILIDAD: {context['volatilidad']}
    
    REGLAS:
    1. Si el evento es absurdo, imposible o pura especulación sin base, di NO OPERAR.
    2. Si el precio es menor a 0.05 o mayor a 0.95, sé muy cauteloso (Riesgo/Beneficio malo).
    3. Responde estrictamente en este formato:
       DECISIÓN: [OPERAR o NO OPERAR]
       RAZÓN: [Máximo 10 palabras]
    """

    try:
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )
        res = completion.choices[0].message.content
        
        decision = "OPERAR" if "DECISIÓN: OPERAR" in res else "NO OPERAR"
        razon = res.split("RAZÓN:")[1].strip() if "RAZÓN:" in res else "Sin razón específica"
        return decision, razon
    except Exception as e:
        return "NO OPERAR", f"Error IA: {e}"
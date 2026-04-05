import os
from dotenv import load_dotenv
from groq import Groq

# 1. Cargamos las variables del .env
load_dotenv()

# 2. DEFINIMOS LA CLASE (Esto es lo que te daba el error)
class DecisionMaker:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        # Inicializamos Groq
        self.client = Groq(api_key=api_key)
        print("🤖 Oráculo de IA (Groq) CONECTADO.")

    def evaluate_with_ai(self, question, change):
        print(f"🧠 Consultando a la IA sobre: {question}...")
        
        prompt = f"""
        Actúa como un trader profesional de Polymarket. 
        El mercado '{question}' se movió un {change*100:.2f}%.
        Explica brevemente por qué esto es una oportunidad o un riesgo. 
        Termina con una recomendación clara de OPERAR o ESPERAR.
        Responde en español y sé muy directo.
        """

        try:
            # Probamos con el modelo más estable actualmente en Groq
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-specdec", 
            )
            return response.choices[0].message.content
        except Exception as e:
            # Plan de respaldo si el modelo anterior falla
            try:
                response = self.client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama-3.1-8b-instant",
                )
                return response.choices[0].message.content
            except Exception as e_inner:
                return f"❌ Error de conexión con la IA: {e_inner}"
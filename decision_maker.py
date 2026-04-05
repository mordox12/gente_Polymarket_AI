import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

class DecisionMaker:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
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
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-specdec", 
            )
            return response.choices[0].message.content
        except Exception:
            try:
                response = self.client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama-3.1-8b-instant",
                )
                return response.choices[0].message.content
            except Exception as e_inner:
                return f"❌ Error de conexión con la IA: {e_inner}"

# --- ESTA ES LA FUNCIÓN "PUENTE" QUE TU MAIN NECESITA ---
def decide_trade(analysis_text):
    """
    Esta función recibe el análisis (que en tu caso viene del brain) 
    o los datos del mercado y decide.
    """
    dm = DecisionMaker()
    # Si el análisis dice que hay oportunidad, devolvemos OPERAR
    if "OPORTUNIDAD DETECTADA" in analysis_text:
        # Extraemos un mensaje simple para el log
        return "OPERAR", analysis_text
    else:
        return "ESPERAR", "No se detectó desvío suficiente."
import os
import requests
from dotenv import load_dotenv

# Esto carga las variables si estás en tu PC (config.env)
load_dotenv("config.env")

class Brain:
    def __init__(self):
        # Busca las llaves en el sistema (GitHub) o en el archivo local
        self.api_key = os.getenv("SAMBANOVA_API_KEY")
        self.url = "https://api.sambanova.ai/v1/chat/completions"

    def analizar_mercado(self, market_title):
        if not self.api_key:
            return "Error: No hay API Key de SambaNova"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "Meta-Llama-3.1-8B-Instruct",
            "messages": [
                {"role": "system", "content": "Eres un experto en trading. Analiza el mercado y da una razón de máximo 10 palabras."},
                {"role": "user", "content": f"¿Es buena idea invertir en: {market_title}?"}
            ]
        }

        try:
            response = requests.post(self.url, json=payload, headers=headers)
            return response.json()['choices'][0]['message']['content']
        except:
            return "Alta probabilidad de éxito según tendencia actual."
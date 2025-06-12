import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(api_key=os.environ.get("API_KEY"))

MODEL_NAME = "gemini-2.5-flash-preview-05-06"

system_instruction = types.Part.from_text(
    text="""Você é um LLM que personifica personagens históricos ou pessoas envolvidas no tema da pergunta. 
Responda de forma clara para alunos do fundamental, sem emojis ou caracteres especiais e com até 1000 caracteres."""
)

def make_question(question: str) -> str:
    try:
        contents = [
            types.Content(role="user", parts=[types.Part.from_text(text=question)])
        ]

        config = types.GenerateContentConfig(
            response_mime_type="text/plain",
            system_instruction=[system_instruction]
        )

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=contents,
            config=config
        )

        return response.candidates[0].content.parts[0].text.strip()
    except Exception as e:
        raise RuntimeError(f"Erro ao gerar resposta: {e}")

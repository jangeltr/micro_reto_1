# main.py
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import json

app = FastAPI(title="Micro Reto 1: Ingesta de Datos", version="1.0.0")

# --- CONFIGURACIÓN LLM (LM Studio / OpenAI) ---
# En Docker, para acceder al host (tu Debian), usaremos una URL especial o la IP local.
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "http://host.docker.internal:1234/v1")
LLM_API_KEY = os.getenv("LLM_API_KEY", "lm-studio") # LM Studio no valida la key, OpenAI sí.

client = OpenAI(base_url=LLM_BASE_URL, api_key=LLM_API_KEY)

# --- MODELOS DE DATOS (Pydantic) ---
class RawInput(BaseModel):
    source: str  # "whatsapp" o "email"
    content: str # El mensaje sucio, ej: "Hola soy Juan del taller mecánico..."

class StructuredOutput(BaseModel):
    nombre_empresa: str
    giro_negocio: str
    datos_clave: str
    canal_origen: str

# --- FUNCIÓN DE EXTRACCIÓN CON LLM ---
def extract_info_with_llm(text: str) -> dict:
    prompt = f"""
    Eres un asistente de extracción de datos. Analiza el siguiente texto informal de un cliente y extrae:
    1. Nombre de la empresa (si no existe, invéntalo basado en el contexto o pon 'Desconocido').
    2. Giro o tipo de negocio.
    3. Resumen de datos relevantes sobre sostenibilidad o descripción del negocio.
    
    Texto: "{text}"
    
    Responde SOLO con un JSON válido con este formato:
    {{
        "nombre_empresa": "...",
        "giro_negocio": "...",
        "datos_clave": "..."
    }}
    """
    
    try:
        response = client.chat.completions.create(
            model="local-model", # Nombre genérico para LM Studio
            messages=[
                {"role": "system", "content": "Eres un extractor de datos JSON experto."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0
        )
        content = response.choices[0].message.content
        
        # Limpieza básica por si el LLM pone texto extra
        json_start = content.find('{')
        json_end = content.rfind('}') + 1
        json_str = content[json_start:json_end]
        
        return json.loads(json_str)
    except Exception as e:
        print(f"Error LLM: {e}")
        # Fallback manual por si falla el LLM
        return {
            "nombre_empresa": "Extracción Fallida",
            "giro_negocio": "General",
            "datos_clave": text
        }

# --- ENDPOINTS ---

@app.get("/")
def read_root():
    return {"status": "Micro Reto 1 Online", "llm_url": LLM_BASE_URL}

@app.post("/ingest", response_model=StructuredOutput)
async def ingest_data(entrada: RawInput):
    """
    Recibe datos 'sucios' de WhatsApp o Email, los procesa con LLM 
    y devuelve JSON estructurado.
    """
    print(f"Recibiendo datos de {entrada.source}...")
    
    extracted_data = extract_info_with_llm(entrada.content)
    
    # Construimos la respuesta final
    return StructuredOutput(
        nombre_empresa=extracted_data.get("nombre_empresa", "N/A"),
        giro_negocio=extracted_data.get("giro_negocio", "N/A"),
        datos_clave=extracted_data.get("datos_clave", ""),
        canal_origen=entrada.source
    )
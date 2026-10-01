import os
from google import genai
from procesador_pdf import cargar_todos_los_pdfs

# 1. Cargar el conocimiento al iniciar la app
print("Cargando base de conocimiento de PDFs...")
BASE_DE_CONOCIMIENTO = cargar_todos_los_pdfs("PDFs")
print(f"Se generaron {len(BASE_DE_CONOCIMIENTO)} fragmentos de conocimiento.")

# Inicializar cliente Gemini (Tomará la clave que app.py ya cargó)
client = genai.Client()

def recuperar_contexto_relevante(pregunta):
    """
    Busca en los chunks de PDF cuáles tienen más relación con la pregunta.
    """
    palabras_pregunta = pregunta.lower().split()
    chunks_puntuados = []
    
    for chunk in BASE_DE_CONOCIMIENTO:
        puntuacion = sum(1 for palabra in palabras_pregunta if palabra in chunk.lower())
        if puntuacion > 0:
            chunks_puntuados.append((puntuacion, chunk))
            
    # Ordenar de mayor a menor coincidencia
    chunks_puntuados.sort(reverse=True, key=lambda x: x[0])
    
    # Tomar solo los 3 fragmentos más relevantes para no saturar a la IA
    mejores_chunks = [chunk for puntuacion, chunk in chunks_puntuados[:3]]
    return "\n\n---\n\n".join(mejores_chunks)

def generar_respuesta(mensaje_usuario):
    """Función principal que será llamada desde app.py"""
    contexto = recuperar_contexto_relevante(mensaje_usuario)
    
    prompt = f"""
    Eres un Tutor de Cálculo de la universidad. Responde a la pregunta del estudiante utilizando EXCLUSIVAMENTE la información proporcionada en el contexto. 
    Si la respuesta no se encuentra en el contexto, indícalo amablemente.
    
    MUY IMPORTANTE: Formatea TODAS las ecuaciones, variables, fracciones (como raíces sobre expresiones) y operaciones matemáticas usando código LaTeX. 
    - Usa un solo símbolo de dólar ($) para matemáticas en línea.
    - Usa doble símbolo de dólar ($$) para ecuaciones en bloque o centradas.
    
    Contexto extraído de los PDFs:
    {contexto}
    
    Pregunta del estudiante:
    {mensaje_usuario}
    """
    
    response = client.models.generate_content(
        model='gemini-3.8-flash-8b',
        contents=prompt,
    )
    return response.text
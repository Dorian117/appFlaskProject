import os
from flask import Flask, render_template, request, jsonify
from google import genai
from dotenv import load_dotenv

# Cargar variables de entorno (para desarrollo local)
load_dotenv()

app = Flask(__name__)

# Inicializar el cliente de Gemini. 
# Automáticamente tomará la variable de entorno GEMINI_API_KEY
client = genai.Client()

def recuperar_contexto_rag(mensaje_usuario):
    """
    Aquí integras la lógica de tu archivo 'Avance1_TutorCalculo.py'.
    El objetivo es buscar en los documentos de los 'Talleres' la información
    más relevante basada en la consulta del usuario.
    """
    # Ejemplo de contexto simulado (reemplaza esto con tu lógica de búsqueda vectorial o lectura de archivos reales de los talleres)
    contexto_extraido = "Las derivadas representan la tasa de cambio instantánea de una función."
    return contexto_extraido

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    
    try:
        # 1. Recuperación (Retrieval)
        contexto = recuperar_contexto_rag(user_message)
        
        # 2. Aumento del Prompt (Augmented)
        prompt_rag = f"""
        Eres un Tutor de Cálculo experto. Responde a la pregunta del estudiante utilizando EXCLUSIVAMENTE la información proporcionada en el contexto. Si la respuesta no se encuentra en el contexto, indícalo amablemente.
        
        Contexto de los talleres:
        {contexto}
        
        Pregunta:
        {user_message}
        """
        
        # 3. Generación (Generation)
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt_rag,
        )
        
        bot_response = response.text
        
    except Exception as e:
        bot_response = f"Error interno en el servidor de IA: {str(e)}"
        
    return jsonify({"response": bot_response})

if __name__ == '__main__':
    # El puerto 5000 es para local; Render asignará su propio puerto en producción
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
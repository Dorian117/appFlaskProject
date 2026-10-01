import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# 1. CARGAR LAS VARIABLES DE ENTORNO PRIMERO
load_dotenv()

# 2. IMPORTAR LA LÓGICA DESPUÉS (para que ya encuentre la API Key)
from Avance1_TutorCalculo import generar_respuesta

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    
    try:
        # Llamamos a la función que conecta todo (PDFs + Contexto + Gemini)
        bot_response = generar_respuesta(user_message)
    except Exception as e:
        bot_response = f"Hubo un error al procesar tu solicitud: {str(e)}"
        
    return jsonify({"response": bot_response})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
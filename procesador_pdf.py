import os
import PyPDF2

def extraer_texto_pdf(ruta_archivo):
    texto_completo = ""
    try:
        with open(ruta_archivo, 'rb') as archivo:
            lector = PyPDF2.PdfReader(archivo)
            for pagina in lector.pages:
                texto_extraido = pagina.extract_text()
                if texto_extraido:
                    texto_completo += texto_extraido + " "
    except Exception as e:
        print(f"Error al leer el PDF {ruta_archivo}: {e}")
    return texto_completo

def fragmentar_con_solapamiento(texto, tamano_chunk=250, solapamiento=50):
    palabras = texto.split()
    chunks = []
    i = 0
    while i < len(palabras):
        chunk_actual = palabras[i : i + tamano_chunk]
        chunks.append(" ".join(chunk_actual))
        i += (tamano_chunk - solapamiento)
    return chunks

# --- NUEVA FUNCIÓN PARA LEER LA CARPETA ---
def cargar_todos_los_pdfs(ruta_carpeta="PDFs"):
    """Lee todos los PDFs de la carpeta y devuelve una lista con todos los chunks."""
    conocimiento_total = []
    
    if not os.path.exists(ruta_carpeta):
        print(f"Advertencia: No se encontró la carpeta '{ruta_carpeta}'")
        return conocimiento_total
        
    for archivo in os.listdir(ruta_carpeta):
        if archivo.endswith(".pdf"):
            ruta_completa = os.path.join(ruta_carpeta, archivo)
            print(f"Procesando: {archivo}...")
            texto = extraer_texto_pdf(ruta_completa)
            # Usamos 300 palabras y 50 de solapamiento
            chunks = fragmentar_con_solapamiento(texto, 300, 50)
            conocimiento_total.extend(chunks)
            
    return conocimiento_total
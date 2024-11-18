import os
import time
from pyngrok import ngrok

# Definir el puerto donde Streamlit se ejecutará
port = 8501

print("Iniciando Streamlit...")
# Iniciar Streamlit como un proceso del sistema (de forma no bloqueante)
streamlit_process = os.popen(f"streamlit run app.py")

# Esperar unos segundos para asegurar que Streamlit inicie correctamente
time.sleep(5)

print("Exponiendo el servidor con Ngrok...")
try:
    # Exponer el puerto 8501 al público utilizando Ngrok
    public_url = ngrok.connect(port)
    print(f"Tu aplicación está disponible en: {public_url}")

    # Mantener la conexión activa para que Ngrok no se detenga
    input("Presiona ENTER para finalizar el túnel y cerrar Streamlit...")
finally:
    # Detener el túnel de Ngrok y el proceso de Streamlit
    ngrok.kill()
    streamlit_process.close()
    print("Ngrok detenido. Streamlit cerrado.")

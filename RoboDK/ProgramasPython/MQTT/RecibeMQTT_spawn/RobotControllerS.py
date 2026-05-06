# Contenido de RobotController.py

def handle_message(mqtt_client, topic, mensaje, RDK):
    print(f"--> Nuevo mensaje en {topic}: {mensaje}")
    
    # 1. Convertimos el mensaje (texto) a un número (entero)
    # Usamos try/except por si acaso alguien envía una palabra en vez de un número
    try:
        tipo = int(mensaje)
    except ValueError:
        print(f"Error: El mensaje '{mensaje}' no es un número. Ignorando orden.")
        return # Salimos de la función para no provocar un fallo
        
    # 2. A partir de aquí, 'tipo' ya es una variable numérica normal.
    # ¡Aquí entra tu código del principio!

    RDK.setParam('TipoAzulejo', tipo)


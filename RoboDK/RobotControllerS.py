# Contenido de RobotController.py

def handle_message(mqtt_client, topic, mensaje, RDK):
    
    # 1. Convertimos el mensaje a un número
    try:
        tipo = int(mensaje)
    except ValueError:
        print(f"Error: El mensaje '{mensaje}' no es un número. Ignorando orden.")
        return 
        

    cola_raw = RDK.getParam('ColaAzulejos')
    
    if isinstance(cola_raw, (float, int)):
        cola_actual = str(int(cola_raw))
    elif cola_raw:
        cola_actual = str(cola_raw)
    else:
        cola_actual = ""


    if not cola_actual:
        RDK.setParam('ColaAzulejos', str(tipo))
        
    else:
        nueva_cola = cola_actual + "," + str(tipo)
        RDK.setParam('ColaAzulejos', nueva_cola)

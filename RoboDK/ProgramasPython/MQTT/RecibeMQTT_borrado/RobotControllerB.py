# Contenido de RobotController.py

def handle_message(mqtt_client, topic, mensaje, RDK):
    print(f"--> Nuevo mensaje en {topic}: {mensaje}")
    
    try:
        tipo = int(mensaje)
    except ValueError:
        print(f"Error: El mensaje '{mensaje}' no es un número. Ignorando orden.")
        return 
        
    # ¡Líneas de robolink eliminadas! Usamos el RDK que viene por los parámetros.

    prog1 = RDK.Item('Palet1OFF')
    prog2 = RDK.Item('Palet2OFF')

    frame1 = RDK.Item('Frame Pallet 1')
    frame2 = RDK.Item('Frame Pallet 2')

    lista_palet1 = frame1.Childs()
    lista_palet2 = frame2.Childs()
    
    match tipo:
        case 1:
            # 1. Comprobamos que el programa existe para evitar fallos
            if not prog1.Valid():
                print("Error: No se encontró el programa 'Palet1OFF'")
                return
                
            for item in lista_palet1:
                # Buena práctica: Validar antes de leer el nombre (como vimos antes)
                if item.Valid() and item.Name().startswith('cajaC'):
                    item.Delete()
                    
            RDK.setParam('x3', 0)
            RDK.setParam('y3', 0)
            RDK.setParam('z3', 0)
            RDK.setParam('LuzPalet1', 0)
            
            # 2. Ejecutamos e imprimimos el resultado
            resultado = prog1.RunProgram()
            if resultado == 1:
                print("Éxito: Programa Palet1OFF iniciado.")
            else:
                print("Fallo: RoboDK rechazó iniciar el programa. (¿El robot está ocupado?)")

        case 2:
            if not prog2.Valid():
                print("Error: No se encontró el programa 'Palet2OFF'")
                return
                
            for item in lista_palet2:
                if item.Valid() and item.Name().startswith('cajaC'):
                    item.Delete()
                    
            RDK.setParam('x4', 0)
            RDK.setParam('y4', 0)
            RDK.setParam('z4', 0)
            RDK.setParam('LuzPalet2', 0)
            
            prog2.RunProgram()

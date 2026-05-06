# Ejemplo de un nuevo programa: enviar_alerta.py
import paho.mqtt.client as mqtt

# 1. Configuración
broker = "broker.emqx.io"
port = 1883
# user = "giirob"
# passwd = "UPV2024"
topic_destino = "sim/working/palet2"

# 2. Conexión rápida
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
#mqttc.username_pw_set(username=user, password=passwd)
mqttc.connect(broker, port, 60)

# 3. ¡Disparar el mensaje!
mensaje = "off"
mqttc.publish(topic_destino, mensaje)

# 4. Desconectar (Es buena práctica si el script termina aquí)
mqttc.disconnect()

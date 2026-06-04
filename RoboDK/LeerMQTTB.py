from robodk import robolink    # RoboDK API
from robodk import robomath    # Robot toolbox
RDK = robolink.Robolink()

import paho.mqtt.client as mqtt
import RobotControllerB as rc
    

broker="broker.emqx.io"
port=1883
#user="giirob"
#passwd="UPV2024"
base_topic="sim/working/button/empty"
#station_name="/demo"
#station_commands_topic=base_topic+station_name+"/commands"
#station_status_topic=base_topic+station_name+"/status"


def on_message(mqttc, obj, msg):
    payload = msg.payload.decode('utf-8')
    topic = msg.topic
    qos = msg.qos
    rc.handle_message(mqttc, topic, payload, RDK)

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_message = on_message

#mqttc.username_pw_set(username=user, password=passwd)
mqttc.connect(broker, port, 60)
mqttc.subscribe(base_topic, 0)

mqttc.publish(base_topic, "ready")

mqttc.loop_forever()


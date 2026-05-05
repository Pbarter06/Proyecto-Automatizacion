
void suscribirseATopics() {
  
  // Suscripciones a los topics MQTT ...
  // Se suscribe a los topics para recibir comandos de encendido/apagado de LEDs de estado de palets
  mqtt_subscribe(PALET1_STATUS_TOPIC);
  mqtt_subscribe(PALET2_STATUS_TOPIC);
  mqtt_subscribe(WORKING_TOPIC);

}

void alRecibirMensajePorTopic(char* topic, String incomingMessage) {

  // Control de LEDs de estado de palets
  if (strcmp(topic, PALET1_STATUS_TOPIC) == 0) {
    if (incomingMessage == "on") {
      info("LED PALET 1: "); infoln("ON");
      digitalWrite(LED_PALET1_LLENO, HIGH);
    } 
    else if (incomingMessage == "off") {
      info("LED PALET 1: "); infoln("OFF");
      digitalWrite(LED_PALET1_LLENO, LOW);
    }
  }
  else if (strcmp(topic, PALET2_STATUS_TOPIC) == 0) {
    if (incomingMessage == "on") {
      info("LED PALET 2: "); infoln("ON");
      digitalWrite(LED_PALET2_LLENO, HIGH);
    } 
    else if (incomingMessage == "off") {
      info("LED PALET 2: "); infoln("OFF");
      digitalWrite(LED_PALET2_LLENO, LOW);
    }
  }
  else if (strcmp(topic, WORKING_TOPIC) == 0) {
    info("Mensaje en WORKING_TOPIC: "); infoln(incomingMessage);
  }
  else {
    warn("Topic no reconocido: "); warnln(topic);
  }

}








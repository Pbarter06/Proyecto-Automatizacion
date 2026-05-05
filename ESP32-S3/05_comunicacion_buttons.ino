long now = 0, lastMsg = 0;
long sensorsUpdateInterval = 5000; // tiempo de actualización de los sensores


void enviarMensajePorTopic(const char* topic, String outgoingMessage) {

  mqtt_publish(topic, outgoingMessage.c_str());

}

struct BotonMQTT {
  uint8_t pin;
  const char* topic;
  const char* payload;
  bool lastReading;
  bool stableState;
  unsigned long lastDebounceTime;
};

void gestionarBoton(BotonMQTT& boton) {
  const unsigned long debounceDelay = 50;
  bool reading = digitalRead(boton.pin);

  if (reading != boton.lastReading) {
    boton.lastDebounceTime = millis();
    boton.lastReading = reading;
  }

  if ((millis() - boton.lastDebounceTime) > debounceDelay && reading != boton.stableState) {
    boton.stableState = reading;

    if (boton.stableState == LOW) {
      info("Boton pulsado, publicando: "); infoln(boton.payload);
      enviarMensajePorTopic(boton.topic, String(boton.payload));
    }
  }
}

void on_loop() {

  static BotonMQTT botones[] = {
    {AZULEJO_BUENO, BUTTON_SPAWN_TOPIC, "BUENO", HIGH, HIGH, 0},
    {AZULEJO_MALO, BUTTON_SPAWN_TOPIC, "ROTO", HIGH, HIGH, 0},
    {AZULEJO_DEFECTUOSO, BUTTON_SPAWN_TOPIC, "DEFECTUOSO", HIGH, HIGH, 0},
    {BUTTON_VACIAR_PALET1, BUTTON_EMPTY_TOPIC, "PALET1", HIGH, HIGH, 0},
    {BUTTON_VACIAR_PALET2, BUTTON_EMPTY_TOPIC, "PALET2", HIGH, HIGH, 0}
  };

  now = millis();
  if (now - lastMsg > sensorsUpdateInterval ) {
    lastMsg = now;
    
    //
    // Read and process sensors
    //
/*
    char tempString[8];
    dtostrf(temperature, 1, 2, tempString);
    Serial.print("Temperature: ");
    Serial.println(tempString);
    enviarMensajePorTopic("esp32/temperature", tempString);
*/

  }

  for (size_t i = 0; i < sizeof(botones) / sizeof(botones[0]); i++) {
    gestionarBoton(botones[i]);
  }

}


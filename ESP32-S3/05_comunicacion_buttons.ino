#include "buttons.h"

long now = 0, lastMsg = 0;
long sensorsUpdateInterval = 5000; // tiempo de actualización de los sensores

struct BotonMQTT;
void gestionarBoton(BotonMQTT& boton);


void enviarMensajePorTopic(const char* topic, String outgoingMessage) {

  mqtt_publish(topic, outgoingMessage.c_str());

}


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
    {AZULEJO_BUENO, BUTTON_SPAWN_TOPIC, "1", HIGH, HIGH, 0}, 
    {AZULEJO_MALO, BUTTON_SPAWN_TOPIC, "2", HIGH, HIGH, 0},
    {AZULEJO_DEFECTUOSO, BUTTON_SPAWN_TOPIC, "3", HIGH, HIGH, 0},
    {BUTTON_VACIAR_PALET1, BUTTON_EMPTY_TOPIC, "1", HIGH, HIGH, 0},
    {BUTTON_VACIAR_PALET2, BUTTON_EMPTY_TOPIC, "2", HIGH, HIGH, 0}
  };

  now = millis();
  if (now - lastMsg > sensorsUpdateInterval ) {
    lastMsg = now;

  }

  for (size_t i = 0; i < sizeof(botones) / sizeof(botones[0]); i++) {
    gestionarBoton(botones[i]);
  }

}


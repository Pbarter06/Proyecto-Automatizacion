#define MQTT_CONNECTION_RETRIES 3

PubSubClient mqttClient(espWifiClient);

#define MQTT_DEDUPE_SIZE 32
static uint32_t mqtt_dedupe_buffer[MQTT_DEDUPE_SIZE];
static int mqtt_dedupe_idx = 0;

// Deduplicador MQTT (mínimo, buffer circular de hashes recientes)
static uint32_t djb2_hash(const char* str) {
  uint32_t hash = 5381;
  int c;
  while ((c = *str++)) {
    hash = ((hash << 5) + hash) + (uint8_t)c; /* hash * 33 + c */
  }
  return hash;
}

// Devuelve true si el hash se vio recientemente; si no, lo almacena y devuelve false
static bool mqtt_seen_recent(uint32_t h) {
  for (int i = 0; i < MQTT_DEDUPE_SIZE; ++i) {
    if (mqtt_dedupe_buffer[i] == h) return true;
  }
  // almacenar en el índice actual
  mqtt_dedupe_buffer[mqtt_dedupe_idx++] = h;
  if (mqtt_dedupe_idx >= MQTT_DEDUPE_SIZE) mqtt_dedupe_idx = 0;
  return false;
}

// CONFIGURACIÓN MQTT
const char* mqttServerIP = MQTT_SERVER_IP;
unsigned int mqttServerPort = MQTT_SERVER_PORT;
String mqttClientID;

void mqtt_loop() {

  if (!mqttClient.connected()) {
    mqtt_reconnect(MQTT_CONNECTION_RETRIES);
    suscribirseATopics();
  }
  mqttClient.loop();

}
void mqtt_connect(String clientID) {

    // Configuramos cliente MQTT
    mqttClientID = String(clientID);
    mqttClient.setServer(mqttServerIP, mqttServerPort);

    // Configuramos 'mqttCallback' como la función que se invocará al 
    //  recibir datos por las suscripciones realizadas
    mqttClient.setCallback(mqttCallback);

    // Conectamos
    mqtt_reconnect(MQTT_CONNECTION_RETRIES);

}

void mqtt_reconnect(int retries) {

  if ( !WiFi.isConnected() )
    return;

  if ( !mqttClient.connected() )
    warnln("Disconnected from the MQTT broker");

  // Bucle hasta que nos reconectemos, o se alcance el número de reintentos...
  int r=0;
  while (!mqttClient.connected() && r<retries) {
    r++;

    trace("Attempting an MQTT connection to: 'mqtt://");
    trace(mqttServerIP);
    trace(":");
    trace(mqttServerPort);
    trace("' with client-id: '");
    trace(mqttClientID);
    traceln("' ... ");


    // Intentar conectar
    // boolean connect (clientID, [username, password], [willTopic, willQoS, willRetain, willMessage], [cleanSession])

    if ( mqttClient.connect(mqttClientID.c_str()) ) {
      debugln("-=- Connected to MQTT Broker");
      // Damos tiempo a que la conexión se establezca por completo
      delay(1000);
    } else {
      debug("-X- failed, rc=");
      debugln(mqttClient.state());
      debugln("-R-   re-trying in 5 seconds");
      // Esperar 5 segundos antes de reintentar
      delay(5000);
    }
  }
}

void mqttCallback(char* topic, byte* message, unsigned int length) {
  // Función que se invocará automáticamente al recibir datos por algún topic
  //  sobre el que nos hayamos suscrito

  // Cargamos los datos recibidos en una variable
  String incomingMessage;
  for (int i = 0; i < length; i++) {
    incomingMessage += (char)message[i];
  }

  // Deduplícación: calcular hash de topic + payload e ignorar duplicados recientes
  String combo = String(topic);
  combo += '|';
  combo += incomingMessage;
  uint32_t h = djb2_hash(combo.c_str());
  if ( mqtt_seen_recent(h) ) {
    trace("-- Ignorando mensaje MQTT duplicado (reciente)");
    return;
  }

  traceln("<<~~ RECEIVING an MQTT message:");
  traceln(topic);
  traceln(incomingMessage);

  alRecibirMensajePorTopic(topic, incomingMessage);
}

void mqtt_publish(const char* topic, String outgoingMessage) {
  if ( !mqttClient.connected() ) {
    errorln("Cannot send message through the topic ... the MQTT Client is disconnected!!")
    return;
  }

  traceln("~~>> PUBLISHING an MQTT message:");
  traceln(topic);
  traceln(outgoingMessage);
  mqttClient.publish(topic, outgoingMessage.c_str());
}


void mqtt_subscribe(const char* topic) {
  if ( !mqttClient.connected() ) {
    errorln("Cannot subscribe to topic ... the MQTT Client is disconnected!!")
    return;
  }


  trace("Subscribed to topic: ");
  traceln(topic);
  mqttClient.subscribe(topic);
}

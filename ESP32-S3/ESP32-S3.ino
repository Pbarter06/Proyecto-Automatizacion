/****************************************************************************
 * 
 * @details    : Implementación con ESP32-S3 de un sistema de control mediante comunicación con MQTT
 * @author     : Paula Barona, Finn Perea, Ainhoa López, Claudia Moreno
 * 
 **************************************************************************
 */
#include "00_Config.h"
#include <WiFi.h>
#ifdef SSL_ROOT_CA
  #include <WiFiClientSecure.h>
#endif
#include <PubSubClient.h>
#include <ArduinoJson.h>

// ID de Dispositivo : se proporcionan varias alternativas, a modo de ejemplo
String deviceID = "esp32-" + WiFi.macAddress(); 

  // Versión usando el ID asignado en la asignatura GIIROB-PR2
//String deviceID = String("device-") + String(WiFi.macAddress());            
  // Versión usando la dirección MAC del dispositivo
//String deviceID = String("device-esp32s3-") + String(DEVICE_ESP_ID);        
  // Versión usando el ID de ESP del dispositivo

void setup() {
  // Este setup configura conceptos 'core', inicializa la wifi y la conexión con 
  //  el bróker MQTT, y ejecuta algunos métodos que hay que completar. 
  // En concreto los alumnos deberán implementar los métodos:
  //  - suscribirseATopics()  -> topics MQTT a suscribir para recibir mensajes 
  //                            (g_comunicaciones.ino)
  //  - on_setup()            -> añadir la configuración de pines, inicialización
  //                            de variables, etc. (s_setup.ino)
  //  - on_loop()             -> tareas a realizar dentro del 'loop' (w_loop.ino)

#ifdef LOGGER_ENABLED
  // Inicializamos comunicaciones serial
  Serial.begin(BAUDS);
  delay(1000);
  Serial.println();
#endif

Serial.println(deviceID);

  // Nos conectamos a la wifi
  wifi_connect();

  // Nos conectamos al broker MQTT, indicando un 'client-id'
  mqtt_connect(deviceID);

  suscribirseATopics();

  on_setup();

}

void loop() {

  wifi_loop();
  mqtt_loop();
  on_loop();
}



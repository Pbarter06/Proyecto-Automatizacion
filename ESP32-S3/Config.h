// COMM BAUDS
#define BAUDS 115200 

#define LOGGER_ENABLED            // Comentar para deshabilitar el logger por consola serie

#define LOG_LEVEL TRACE           // nivells en c_logger: TRACE, DEBUG, INFO, WARN, ERROR, FATAL, NONE

// DEVICE
//#define DEVICE_ESP_ID             "54CE0361421"   // ESP32 ID
#define DEVICE_GIIROB_PR2_ID      "00" //"giirobpr2_00"

// WIFI
#define NET_SSID                  "UPV-PSK"
#define NET_PASSWD                "giirob-pr2-2023"

// MQTT
#define MQTT_SERVER_IP            "mqtt.dsic.upv.es"
#define MQTT_SERVER_PORT          1883 // Conexion ABIERTA para pruebas (sin SSL). Para SSL usar 8883 + SSL_ROOT_CA.
#define MQTT_USERNAME             "giirob" // Por definir 
#define MQTT_PASSWORD             "UPV2024" // Por definir


//TOPICS MQTT
#define BUTTON_SPAWN_TOPIC               "sim/working/button/spawn"   //Botones de spawneo de azulejos
#define BUTTON_EMPTY_TOPIC               "sim/working/button/empty"  //Botones de vaciado de palets
#define WORKING_TOPIC                    "sim/working"    // Topic para publicar el estado de funcionamiento del dispositivo 
#define PALET1_STATUS_TOPIC              "sim/working/palet1/status" // Topic para publicar el estado del palet 1 (lleno/vacío)
#define PALET2_STATUS_TOPIC              "sim/working/palet2/status" // Topic para publicar el estado del palet 2 (lleno/vacío)          "

// LEDS (OUTPUTS)
#define LED_FUNCIONAMIENTO      2 // GPIO0, LED integrado en la placa (ON: LOW, OFF: HIGH)
#define LED_PALET1_LLENO        18 // GPIO18, LED externo (ON: HIGH, OFF: LOW)
#define LED_PALET2_LLENO        19 // GPIO19, LED externo (ON: HIGH, OFF: LOW)

// _________________ FALTA POR DEFINIR EL RESTO DE LEDS ______________________


// BOTONES (INPUTS)
#define BUTTON_VACIAR_PALET1        38 // GPIO38, Botón externo (PULSADO: LOW, NO PULSADO: HIGH)
#define BUTTON_VACIAR_PALET2        39 // GPIO39, Botón externo (PULSADO: LOW, NO PULSADO: HIGH)

#define AZULEJO_BUENO              40 // GPIO40, Botón externo que spawnea mediante el envío de MQTT un azulejo (PULSADO: LOW, NO PULSADO: HIGH)
#define AZULEJO_MALO               41 // GPIO41, Botón externo que spawnea mediante el envío de MQTT un azulejo (PULSADO: LOW, NO PULSADO: HIGH)
#define AZULEJO_DEFECTUOSO         42 // GPIO42, Botón externo que spawnea mediante el envío de MQTT un azulejo (PULSADO: LOW, NO PULSADO: HIGH)


// ____________________ FALTA POR REVISAR TODOS LOS PINES _______________________





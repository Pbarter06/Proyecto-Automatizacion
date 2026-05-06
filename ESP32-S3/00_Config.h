// COMM BAUDS
#define BAUDS 115200 

#define LOGGER_ENABLED            // Comentar para deshabilitar el logger por consola serie

#define LOG_LEVEL TRACE           // nivells en c_logger: TRACE, DEBUG, INFO, WARN, ERROR, FATAL, NONE

// DEVICE
//#define DEVICE_ESP_ID             "54CE0361421"   // ESP32 ID
#define DEVICE_GIIROB_PR2_ID      "00" //"giirobpr2_00"

// WIFI
#define NET_SSID                  "Azulejos"
#define NET_PASSWD                "paula123"

// MQTT
#define MQTT_SERVER_IP            "broker.emqx.io"
#define MQTT_SERVER_PORT          1883 // Conexion ABIERTA para pruebas (sin SSL). Para SSL usar 8883 + SSL_ROOT_CA.

/*
#define MQTT_USERNAME             "azulejos"
#define MQTT_PASSWORD             "azulejos123" // Por definir
*/

//TOPICS MQTT
#define BUTTON_SPAWN_TOPIC               "sim/working/button/spawn"   //Botones de spawneo de azulejos
#define BUTTON_EMPTY_TOPIC               "sim/working/button/empty"  //Botones de vaciado de palets
#define WORKING_TOPIC                    "sim/working"    // Topic para publicar el estado de funcionamiento del dispositivo 
#define PALET1_STATUS_TOPIC              "sim/working/palet1" // Topic para publicar el estado del palet 1 (lleno/vacío)
#define PALET2_STATUS_TOPIC              "sim/working/palet2" // Topic para publicar el estado del palet 2 (lleno/vacío)

// LEDS (OUTPUTS)
#define LED_FUNCIONAMIENTO      2 // GPIO, LED integrado en la placa (ON: LOW, OFF: HIGH)
#define LED_PALET1_LLENO        17 // GPIO, LED externo (ON: HIGH, OFF: LOW)
#define LED_PALET2_LLENO        18 // GPIO, LED externo (ON: HIGH, OFF: LOW)



// BOTONES (INPUTS)
#define BUTTON_VACIAR_PALET1        9 // GPIO, Botón externo (PULSADO: LOW, NO PULSADO: HIGH)
#define BUTTON_VACIAR_PALET2        10 // GPIO, Botón externo (PULSADO: LOW, NO PULSADO: HIGH)

#define AZULEJO_BUENO              11 // GPIO, Botón externo que spawnea mediante el envío de MQTT un azulejo (PULSADO: LOW, NO PULSADO: HIGH)
#define AZULEJO_MALO               12 // GPIO, Botón externo que spawnea mediante el envío de MQTT un azulejo (PULSADO: LOW, NO PULSADO: HIGH)
#define AZULEJO_DEFECTUOSO         13 // GPIO, Botón externo que spawnea mediante el envío de MQTT un azulejo (PULSADO: LOW, NO PULSADO: HIGH)








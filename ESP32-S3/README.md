# CÓDIGOS ESP32-S3
En esta carpeta se va a proceder a explicar la configuración en Arduino que se ha llevado a cabo para el funcionamiento del sistema embebido, ESP32-S3. Para una amyor organización, se va a dividir la explicación por ficheros.

## Config.h
Este fichero tiene como objetivo definir constantes, parámetros necesarios para conectarse a la red, credenciales y topics para la comunicación a través del broker MQTT.

## comunicaciones.ino
Este fichero contiene las funciones que getsionan:
- Suscripciones a topics.
- Recepción de mensajes.
- Envío de mensajes.
  
  ### Función 1:
    ```cpp
    void suscribirseATopics(){
    mqtt_subscribe(HELLO_TOPIC);
    }
    ```
    Esta función se llama al iniciar la conexión MQTT. A continuación se suscribe la ESP32-S3 al topic `HELLO_TOPIC` . Además, permite a parte de enviar mensajes, recibirlos a través de ese canal.

  ### Función 2:
    ```cpp
    void alRecibirMensajePorTopic(char* topic, String incomingMessage){
    ```
    Esta función tiene el rol de controlador que gestiona la recepción de datos. Asimosmo, para que pueda llevar a cabo esta tarea recibe el nombre del topic por el que va a recibir un mensaje y, por último, recibe un mensaje en formato `string`.

  ```cpp
  JsonDocument doc;
  DeserializationError err = deserializeJson(doc, incomingMessage);
  ```
  Lo siguiente a realizar es la creación de un docuemnto JSON, para posteriormente convertir el string recibido en un objeto de formato JSON.
  A continuación, en el código se hace una gestión de errores por si el objeto JSON ha tenido algún problema en su ceración. En ese caso, se muestra un warning por pantalla y se saldrá de la función.
  En el caso de que se haya creado correctamente, lo siguiente a ejecutar es la lectura de campos JSON:
  ```cpp
  String msg = doc["message"];
  info("(JSON) Rebut message: "); infoln(msg);
  int lum = doc["luminosidad"];
  info(" (JSON) Rebut luminosidad: "); infoln(lum);
  const char* temp = doc["temperatura"];
  info("(JSON) Rebut temperatura: "); infoln(temp);
  ```
  A través de estas líneas de código se busca extraer valores del objeto JSON recibido. Luego, estos valores son impresos por pantalla.

  ```cpp
  if(strcmp(topic, HELLO_TOPIC) == 0) {
  ```
    Por último, si se recibe el mensaje se procede a la gestión del topic `HELLO_TOPIC`. De manera que lo primero a llevar a cabo es la comprobación de si el mensaje pertenece al topic esperado. Si es así, entonces dependiendo del mensaje recibido (`on`/ `off`) se mostrará por pantalla el estado del led interno.

  ### Función 3:
  ```cpp
  void enviarMensajePorTopic(const char* topic, String outgoingMessage){
    mqtt_publish(topic, outgoingMessage.c_str());
  }
  ```
  Esta última función del fichero es la encargada de publicar un mensaje a través de un canal MQTT. Su funcionamiento es el inverso a la primera función que se ha analizado; convierte el `String` a `const char*` para la librería MQTT.
  
## funciones.ino

## logger.ino

## loop.ino

## main.ino

## mqtt_lib.ino

## setup.ino

## wifi_lib.ino
Este fichero tiene como propósito gestionar todo lo relacionado con la conexión WIFi de la ESP32-S3. Específicamente este fichero implementa un módulo de comunicaciones WiFi que lleva a cabo lo siguiente:
1. Inicializa la interfaz WiFi de la ESP32-S3.
2. Intenta conectarse a la red configurada en `Config.h`.
3. Reconecta automáticamente si se pierde la conexión en algún punto del proceso.
4. Gestiona el cliente TCP/IP que usará el broker de comunicación MQTT.
5. permite usar TLS/SSL si el proyecto lo requiere.

```cpp
#ifdef SSL_ROOT_CA
  WiFiClientSecure espWifiClient;
#else
  WiFiClient espWifiClient;
#endif
```
Si el proyecto usa **TLS/SSl** se crea un cliente seguro (`WiFiClientSecure`). En el caso contrario, se usa un cliente normal en el proyecto (`WiFIClient`).  Este cliente será usado por MQTT.

```cpp
const char* wifiSSID = NET_SSID;
const char* wifiPasswd = NET_PASSWD;
```
Lo que se busca con estas líneas de código es tomar el SSID y la contraseña que previamente se han definido en `Config.h`.

  ### wifi_loop()
  ```cpp
  void wifi_loop(){
    if(!WiFi.isConnected())
      wifi_recomect(WIFI_CONNECTION_TIMEOUT_SECONDS);
  }
  ```
  Esta función se ejecuta en cada iteración del loop principal. Su principal objetivo es detectar si la ESP32-S3 ha perdido la conexión y si es el caso, intentar reconetar automáticamente.

  ### wifi_connect()
  ```cpp
  WiFi.mode(WIFI_STA);
  trace("MAC Address:. ");
  traceln(WiFi.macAddress());
  ```
  Configura la ESP32-S3 como estación WiFi.
  A continuación, imprime la MAC del dispositivo. Esto se lleva a cabo porque resulta útil al sistema para la depuración del código.

  ```cpp
  #ifdef SSL_ROOT_CA
    espWiFiClient.sestCACert(SSL_ROOT_CA);
  #endif
  ```
  Esta parte del código es la encargada de la configuarción de certificados en el caso de que se apliquen. Pemrite validar certificados si se usa TLS.

  ```cpp
  wifi_reconnect(WIFI_CONNECTION_TIMEOUT_SECONDS);
  ```
  En este instante se llama a la función que realmente intenta conectarse.

  ### wifi_reconnect()
  ```cpp
  WiFi.begin(wifiSSID, wifiPasswd);
  ```
  Inicia la conexión con la red.

  ```cpp
  while (WiFi.status() != WL_CONNECTED && r<retries){
    delay(1000);
    trace(".");
  }
  ```
  Esta sección de código espera hasta conectarse o agortar los intentos; luego, imprime puntos para indicar progreso.
  Si conecta correctamente se muestra la IP asignada. 

  ```cpp
    errorln("-X- Cannot connect to the WiFi newtwork");
  ```
  Sin embargo, si falla en el proceso de conectarse se imprime el error como muestra la línea de código.

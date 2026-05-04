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
Este fichero agrupa funciones auxiliares. Su propósito principal es getsionar el estado del LED interno de la ESP32-S3m actuando como un pequeño módulo de control de actuadores.

```cpp
uint8_t ledStatus = 0;
```
Lo primer a realizar es declarar una variable global (entero sin signo de 8 bits) que almacene el estado actual del LED interno, de manera que :
- `0` : apagado
- `1` : encendido

### setInternalLed(uint8_t status)
  Esta función busca controlar el LED interno de la ESP32-S3. Recibe como parámetro el estado deseado y actualiza el hardware.

  ```cpp
  if(ledStatus == status)
    return;
  ```
  Si el LED ya está en el estaod slicitado, la función termina inmediatamente. Esta condición evita llamadas innecesarias a `digitalWrite()`.

  ```cpp
  ledStatus = status;
  ```
  Actualiza la variable global para reflejar y guardar el nuevo estado del LED.

  ```cpp
  if(status){
    infoln("Led: on");
    digitalWrite(LED_BUILTIN, HIGH);
  } else{
    infoln("Led: off");
    digitalWrite(LED_BUILTIN, LOW);
  }
  ```
  Este bloque de código es realmente el control físico del LED. Funciona de la siguiente manera:
  - `status` != 0 -> enciende el LED
  - `status` == 0 -> apaga el LED
  - `digitalWrite()` es la función estándar de Arduino para escribir en un pin digital.
  - `LED_BUILTIN` está definido en `Config.h` y corresponde al pin físico del LED interno.
  - Se utiliza `infoln()` para registrar el cambio en el sistema de logging, lo que dacilita la depuraciónd e código.

## logger.ino
Este fichero implementa un módulo de registro que permite mostrar mensajes por la terminar con distintas informaciones. Este sistema es fundamentañ àra depurar el comportamiento del firmware. 

En primer lugar, se han definido los niveles de log. Estos valores numéricos representan la prioridad de cada nivel:
- `TRACE(6)`: nivel más detallado.
- `DEBUG(5)`: información útil.
- `INFO(4)`: mensajes informativos generales.
- `WARN(3)`: advertencias
- `ERROR(2)`: errores recuperables.
- `FATAL(1)`: errores críticos.
- `NONE(0)`: descativa completamente el logging.

El nivel activo se define en `Config.h`:
```cpp
#define LOG_LEVEL TRACE
```
Esto significa que se mostrarán todos los mensajes, desde TRACE hasta FATAL.

```cpp
#ifdef LOG_LEVEL
```
Este bloque solo se commpila si existe una constante denominada `LOG_LEVEL`. Si no está definida, todo el logging se desactiva automáticamente.

```cpp
bool _log_newline = true;
```
En el caso de esta variable, es la encargada de controlar si se debe imprimir la etiquera del nivel (`[INFO]`, `[ERROR]`, etc) antes del mensaje.
- `_log_newline == true ` : se imprime la etiqueta.
- `_log_newline == flase` : el mensaje anterior no terminó en salto de línea, por lo que no se repite la etiqueta.

  ```cpp
  #define info(message)  if (LOG_LEVEL >= INFO) { if (_log_newline) Serial.print("[INFO] "); Serial.print(message);  _log_newline = false; }
  #define info(message)  if (LOG_LEVEL >= INFO) { if (_log_newline) Serial.print("[INFO] "); Serial.printls(message);  _log_newline = true; }
  ```
  El bloque de código que surge a continuación sigue esta estructura, esto permite comprobar si el nivel de log actual permite mostrar ese mesaje, si corresponde, en ese caso imprime la etiqueta `[INFO]`. Luego, imprime el emnsaje y actualiza en último lugar la variable `_log_newline` según si se usó `print()` o `println()`.
Sin embargo, si el logging se encuentra desactivado, el compilador elimina completamente el código de loggin y todas las macros se convierten en líneas vacías.

## loop.ino

## main.ino

## mqtt_lib.ino

## setup.ino
La finalidad de este fichero es inicializar los recursos de la ESP32-S3 y enviar un mensaje inicial al broker MQTT para confirmar que el dispositivo está operativo.

  ### on_setup()
  Esta función solamente se ejecutará una vez tras la incialización del sistema.
  
  ```cpp
  pinMode(LED_BUILTIN, OUTPUT);
  ```
  Lo primero a llevar a cabo es la confugración del pin asociado al LED. Se configura como salida digital (`OUTPUT`). La función del LED es un indicador visual que informa del estado del dispositivo.

  ```cpp
  setInternalLed(0);
  ```
  Lo segundo a realizar es la inicialización del LED interno. A través de esta línea de código, se llama a la función definida en el fichero `funciones.ino`. En este caso, `0` significa apagar el LED. Esto garantiza que el dispositivo arranca en un estado conocido y facilita el trabajo que se lleva a cabo a continuación.

  ```cpp
  JsonDOcument doc;
  doc["message] = hello_msg;
  doc["luminosidad"] = 450;
  doc["temperatura"] = 21.5;
  ```
  Después de la creación de un mensaje de texto que se enviará al broker MQTT donde identifica al dispositivo se crea un objeto JSON, gracias a la librería correspondiente. Este objeto permitirá estructurar los datos de manera estándar.  Luego, se asignan los campos al objeto.
  - `message` : texto de saludo
  - `luminosidad`: valor numérico
  - `temperatura`: valor con decimales

  ```cpp
  String hello_mgg_json;
  serializeJson(doc, hello_msg_json);
  enviarMensajePorTopic(HELLO_TOPIC, hello_msg_json);
  ```
Por último, el objeto JSON se convierte en un`String`y está listo para enviarse por MQTT. En el caso de `serializeJson()` permite transformar la estructura interna en un texto. Finalmente, se envía el mensaje al broker MQTT. Se publica el JSON en el topic definido en `Config.h`.

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

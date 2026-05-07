# CÓDIGOS ESP32-S3
En esta carpeta se va a proceder a explicar la configuración en Arduino que se ha llevado a cabo para el funcionamiento del sistema embebido, ESP32-S3. Para una mayor organización, se va a dividir la explicación por ficheros.

## 00_Config.h
Este fichero tiene como objetivo definir constantes, parámetros necesarios para conectarse a la red, topics MQTT y pines de entrada y salida. Se agrupan todos estos parámetros en el mismo fichero con el fin de que, si se requiere modificar alguno de ellos, no sea necesario tocar el resto del código.

```cpp
#define BAUDS 115200
```
En primer lugar, se define la velocidad de comunicación del puerto serie. En este caso, la velocidad elegida es la estándar para la depuración rápida.

```cpp
#define LOGGER_ENABLED
```
En segundo lugar, si esta línea de código está activa se habilita el sistema logging implementado en el fichero `01_logger.ino`. En el caso de que no esté habilitado, el logging se deshabilita de igual manera.

```cpp
#define LOG_LEVEL TRACE
```
A continuación, se define el nivel de severidad mínimo que se mostrará. En este caso, al tratarse de `TRACE` se trata de un nivel más detalado lo que permite ver absolutamente todos los mensajes.

```cpp
#define DEVICE_GIIROB_PR2_ID "00"
```
En cuanto al identificador del dispositivo, se mantiene como un identificador lógico del proyecto PR2. Se usa como referencia para distinguir varias ESP32-S3 en la misma red MQTT.

```cpp
#define NET_SSID "Azulejos"
#define NET_PASSWD "paula123"
```
Gracias a este bloque de código se puede configurar la red WiFi. Se definen las credenciales de la red WiFi a la que se conectará la ESP32-S3.
- `NET_SSID`: nombre de la red.
- `NET_PASSWD`: contraseña para acceder a la red.
Estas credenciales son utilizadas por el fichero `02_wifi_lib.ino`.

```cpp
#define MQTT_SERVER_IP "broker.emqx.io"
#define MQTT_SERVER_PORT 1883
```
En este caso, no se configura la red WiFi, sino que se trata de la configuración del broker MQTT. En la versión actual se usa `broker.emqx.io` en el puerto 1883, sin autenticación por defecto.

```cpp
#define BUTTON_SPAWN_TOPIC "sim/working/button/spawn"
#define BUTTON_EMPTY_TOPIC "sim/working/button/empty"
#define WORKING_TOPIC "sim/working"
#define PALET1_STATUS_TOPIC "sim/working/palet1"
#define PALET2_STATUS_TOPIC "sim/working/palet2"
```
Estos son los topics usados por el sistema actual:
- `BUTTON_SPAWN_TOPIC`: publicación de azulejos generados por los botones de spawn.
- `BUTTON_EMPTY_TOPIC`: publicación para vaciar palets.
- `WORKING_TOPIC`: control del LED de funcionamiento.
- `PALET1_STATUS_TOPIC` y `PALET2_STATUS_TOPIC`: control visual del estado de cada palet.

```cpp
#define LED_FUNCIONAMIENTO 2
#define LED_PALET1_LLENO 17
#define LED_PALET2_LLENO 18
```
Por último, se definen los pines físicos de los LEDs internos y externos de la ESP32-S3. El de funcionamiento se utiliza en `04_funciones.ino` y `07_setup.ino`, y los de palets en `06_comunicacion_leds.ino`.

## 05_comunicacion_buttons.ino
Este fichero contiene las funciones que gestionan:
- Lectura de botones físicos.
- Publicación de mensajes MQTT asociados a cada pulsación.
  
  ### void enviarMensajePorTopic(const char* topic, String outgoingMessage):
  ```cpp
  void enviarMensajePorTopic(const char* topic, String outgoingMessage){
    mqtt_publish(topic, outgoingMessage.c_str());
  }
  ```
  Esta función es la encargada de publicar un mensaje a través de un canal MQTT. Convierte el `String` a `const char*` para la librería MQTT.

  El bloque principal del fichero implementa un debounce de 50 ms y publica distintos payloads según el botón pulsado:
  - `AZULEJO_BUENO` publica `"1"` en `BUTTON_SPAWN_TOPIC`.
  - `AZULEJO_MALO` publica `"2"` en `BUTTON_SPAWN_TOPIC`.
  - `AZULEJO_DEFECTUOSO` publica `"3"` en `BUTTON_SPAWN_TOPIC`.
  - `BUTTON_VACIAR_PALET1` publica `"1"` en `BUTTON_EMPTY_TOPIC`.
  - `BUTTON_VACIAR_PALET2` publica `"2"` en `BUTTON_EMPTY_TOPIC`.
  
## 04_funciones.ino
Este fichero agrupa funciones auxiliares. Su propósito principal es gestionar el estado del LED interno de la ESP32-S3, actuando como un pequeño módulo de control de actuadores.

```cpp
uint8_t ledStatus = 0;
```
Lo primero a realizar es declarar una variable global (entero sin signo de 8 bits) que almacene el estado actual del LED interno, de manera que:
- `0`: apagado
- `1`: encendido

  ### setInternalLed(uint8_t status)
    Esta función busca controlar el LED interno de la ESP32-S3. Recibe como parámetro el estado deseado y actualiza el hardware.
  
    ```cpp
    if(ledStatus == status)
      return;
    ```
    Si el LED ya está en el estado solicitado, la función termina inmediatamente. Esta condición evita llamadas innecesarias a `digitalWrite()`.
  
    ```cpp
    ledStatus = status;
    ```
    Actualiza la variable global para reflejar y guardar el nuevo estado del LED.
  
    ```cpp
    if(status){
      digitalWrite(LED_FUNCIONAMIENTO, LOW);
    } else{
      digitalWrite(LED_FUNCIONAMIENTO, HIGH);
    }
    ```
    Este bloque de código es realmente el control físico del LED. Funciona de la siguiente manera:
    - `status` != 0 -> enciende el LED
    - `status` == 0 -> apaga el LED
    - `digitalWrite()` es la función estándar de Arduino para escribir en un pin digital.
    - `LED_FUNCIONAMIENTO` está definido en `00_Config.h` y corresponde al pin físico del LED interno.
    - El LED de funcionamiento es activo en LOW.

  ## 01_logger.ino
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
Este bloque solo se compila si existe una constante denominada `LOG_LEVEL`. Si no está definida, todo el logging se desactiva automáticamente.

```cpp
bool _log_newline = true;
```
En el caso de esta variable, es la encargada de controlar si se debe imprimir la etiqueta del nivel (`[INFO]`, `[ERROR]`, etc.) antes del mensaje.
- `_log_newline == true ` : se imprime la etiqueta.
- `_log_newline == flase` : el mensaje anterior no terminó en salto de línea, por lo que no se repite la etiqueta.

```cpp
#define info(message)    if ( LOG_LEVEL >= INFO  ) { if (_log_newline) Serial.print("[ INFO] "); Serial.print(message);   _log_newline = false;}
#define infoln(message)  if ( LOG_LEVEL >= INFO  ) { if (_log_newline) Serial.print("[ INFO] "); Serial.println(message); _log_newline = true;}
```
El bloque de código que surge a continuación sigue esta estructura, esto permite comprobar si el nivel de log actual permite mostrar ese mensaje, y en ese caso imprime la etiqueta correspondiente. Luego, imprime el mensaje y actualiza en último lugar la variable `_log_newline` según si se usó `print()` o `println()`.
Sin embargo, si el logging se encuentra desactivado, el compilador elimina completamente el código de loggin y todas las macros se convierten en líneas vacías.

## 05_comunicacion_buttons.ino
Este fichero contiene únicamente la función `on_loop()`, la cual representa la parte del programa que se ejecuta de manera repetitiva durante todo el proceso de ejecución.

```cpp
long now = 0, lastMsg = 0;
long sensorsUpdateInterval = 5000;
```
  ### now
  Esta variable es la encargada de guardar el tiempo actual en milisegundos desde que la ESP32-S3 se encendió. Esto se obtiene a través de `millis()`.
  
  ### lastMsg
  Esta variable guarda el instante en el que se ejecutó por última vez la tarea periódica.
  Se inicializa a 0.
  
  ### sensorsUpdateInterval
  En el caso de esta variable se trata de una variable que representa el intervalo de actualización en milisegundos. Al estar igualado a 5000 milisegundos, equivalente a 5 segundos, indica que la tarea periódica se ejecutará cada 5 segundos.

  En la versión actual, además de mantener esta temporización, la función realiza tareas periódicas del sistema como lectura de botones y actualización de estado. Los botones definidos en `buttons.h` se procesan en `05_comunicacion_buttons.ino`.
  
## ESP32-S3.ino
Este fichero se trata del fichero que contiene la estructura principal del programa. Su función es inicializar el sistema, configurar las comunicaciones WiFi y MQTT.

```cpp
String deviceID = "esp32-" + WiFi.macAddress();
```
Primeramente, se define un identificador único del dispositivo a partir de la MAC. Se usa para registrarse en el broker MQTT.

  ### setup()
  Esta función se ejecuta una sola vez al arrancar la ESP32-S3.
  ```cpp
  #ifdef LOGGER_ENABLED
    Serial.begin(BAUDS);
    delay(1000);
    Serial.println();
  #endif
  ```
  Lo siguiente a definir un identificador es la inicialización del logger. Inicia el puerto serie a 115200 baudios y permite imprimir mensajes de depuración. No obstante, solo se activa si `LOGGER_ENABLED` está definido en el fichero `00_Config.h`.
  
  ```cpp
  wifi_connect();
  ```
  EL siguiente paso para un buen funcionamiento es la conexión WiFi. En este caso, se llama a la función definida en `wifi_lib.ino` donde se configura la interfaz y se intenta conectar.
  
  ```cpp
  mqtt_connect(deviceID);
  ```
  De igual manera, se conecta al broker MQTT. En el caso de MQTT se configura el cliente y se establece la conexión con éste. Además, para concluir se registra el callback para aquellos nuevos mensajes que entren.
  
  ```cpp
  suscribirseATopics();
  ```
  Esta línea de código implica la llamada a la función definida previamente en el fichero `05_comunicacion_buttons.ino`. Es en esta función donde se añaden todos los topics que la ESP32-S3 debe escuchar o utilizar para enviar mensajes.

  ```cpp
  on_setup();
  ```
  Lo último a realizar en esta función es la configuración adicional del dispositivo mediante la función `on_setup()` definida en `07_setup.ino`. En ese fichero se realiza la configuración de pines y el estado inicial de LEDs y botones.
  
### void loop()
  Esta función se ejecuta continuamente mientras la ESP32-S3 está encendida.
  ```cpp
  wifi_loop();
  mqtt_loop();
  on_loop();
  ```
Como se puede observar, dentro de la función loop() se realiza el mantenimiento de la conexión WiFi, MQTT y las tareas periódicas que se llevan a cabo en la función `on_loop()`.

## 03_mqtt_lib.ino
La función de este fichero es establecer la conexión con el broker MQTT, mantener la conexión activa, reconectar si se pierde la WiFi, publicar mensajes y suscribirse a topics para procesar los mensajes entrantes mediante un callback. Además, implementa un mecanismo de **deduplicación de mensajes MQTT** que evita el procesamiento de mensajes duplicados recibidos en una ventana corta de tiempo.

### Deduplicador de Mensajes MQTT
Para mejorar la robustez del sistema, se ha incorporado un filtro de deduplicación que:
- Calcula un hash no criptográfico (función `djb2`) sobre la concatenación del topic y el payload.
- Mantiene un buffer circular de los últimos N hashes (`MQTT_DEDUPE_SIZE = 32`).
- Descarta mensajes cuyo hash ya se encuentre registrado en el buffer.
- Reduce reprocesos y falsos disparos causados por retransmisiones del broker o reconexiones de red.

Esta solución consume memoria fija O(N) y tiempo de comprobación proporcional al tamaño del buffer, siendo especialmente adecuada para el perfil limitado del microcontrolador.

```cpp
#define MQTT_CONNECTION_RETRIES 3
PubSubClient mqttClient(espWifiClient);
```
Primeramente, se deben definir todos aquellos parámetros iniciales y clientes de MQTT. En este caso, se define el número máximo de intentos de reconexión antes de finalizar la conexión. Luego, se crea un cliente MQTT usando el cliente WiFi (`espWifiClient`) definido en el fichero `02_wifi_lib.ino`. Este objeto es el que realmente se comunica con el broker.

```cpp
const char* mqttServerIP = MQTT_SERVER_IP;
unsigned int mqttServerPort = MQTT_SERVER_PORT;
String mqttClientID;
```
Continuando con los parámetros iniciales, en este apartado se cargan los parámetros definidos en `00_Config.h` (IP del broker, puerto y ID del cliente, que se asignará en `mqtt_connect()`).

### void mqtt_loop()
  ```cpp
  if(!mqttClient.connected()){
    mqtt_reconnect(MQTT_CONNECTION_RETRIES);
    suscribirseATopics();
  }
  mqttClient.loop();
  ```
  Esta función se ejecuta en cada iteración del loop principal. Principalmente esta función realiza 2 tareas:
    1. Comprueba si el cliente MQTT está conectado: si se detecta que el cliente MQTT no está conectado se llama a `mqtt_reconnect()` y vuelve a suscribirse a los topics.
    2. Llama a `mqttClient.loop()`: en esta fase se procesan mensajes entrantes y se mantiene activa la conexión. En el caso de esta función es imprescindible llamarla de manera continua.
    
### void mqtt_connect(String clientID)
  En un primer instante, esta función recibe como parámetro el ID del dispositivo desde `ESP32-S3.ino`. Se busca llevar a cabo la configuración del cliente y intentar mantener la conexión.

  ```cpp
  mqttClientID = String(clientID);
  mqttClient.setServer(mqttServerIP, mqttServerPort);
  mqttClient.setCallback(mqttCallback);
  ```
  En este bloque de código se realiza la configuración del cliente. Aquí se almacena el ID del cliente, se configura la IP y puerto del broker MQTT. Y también, se registra la función `mqttCallback()` como manejador de mensajes entrantes.

  ```cpp
  mqtt_reconnect(MQTT_CONNECTION_RETRIES);
  ```
  Cuando se ejecuta esta línea de código se llama a la función que realmente intenta conectar.

### void mqtt_reconnect(int retries)
  Esta función intenta garantizar la reconexión al broker hasta un máximo de `retries`.

  ```cpp
  if ( !WiFi.isConnected() )
    return;
  if ( !mqttClient.connected() )
    warnln("Disconnected from the MQTT broker");
  ```
  El primer paso a seguir en esta función es comprobar que haya conexión a WiFi. Si no hay conexión no se intenta conectar con el broker MQTT. En el caso de que ocurra esta situación, se enviará un mensaje de aviso informando de que el dispositivo se encuentra en estado de desconexión.

  ```cpp
  if ( mqttClient.connect(mqttClientID.c_str()) ) {
  ```
  Una vez llegado a esta sección de código, se realiza un intento de conexión. En la versión actual se conecta sin usuario y contraseña por defecto.
  Cuando se realiza una conexión exitosa se espera 1 segundo para estabilizarla. No obstante, si falla se muestra el código de error y se realiza una espera de 5 segundos antes de reintentar la conexión.

### void mqttCallBack(char* topic, byte* message, unsigned int length)
  Esta función se ejecuta automáticamente cuando llega un mensaje MQTT.

  ```cpp
  String incomingMessage;
  for (int i = 0; i < length; i++) {
    incomingMessage += (char)message[i];
  }
  ```
  El primer paso que lleva a cabo esta función es la conversión del mensaje a `String`. MQTT entrega los datos como un array de bytes que se convierten a texto.
  
  ```cpp
  alRecibirMensajePorTopic(topic, incomingMessage);
  ```
  Más tarde, se llama a la función definida en `06_comunicacion_leds.ino` que interpreta el topic y controla los LEDs.

### void mqtt_publish(const char* topic, String outgoingMessage)
  Esta función tiene como objetivo principal la publicación de los mensajes.

  ```cpp
  if ( !mqttClient.connected() ) {
    errorln("Cannot send message ... MQTT Client is disconnected!!")
    return;
  }
  ```
  El primer paso a realizar es comprobar la conexión. Luego, se publica el mensaje a través de `mqttClient.publish(topic, outgoingMessage.c_str())`.

### void mqtt_subscribe(const char* topic)
  Esta función es la que permite la suscripción a los topics correspondientes. Al igual que en los casos anteriores, el primer paso que se realiza es la comprobación de la conexión.

  ```cpp
  trace("Subscribed to topic: ");
  traceln(topic);
  mqttClient.subscribe(topic);
  ```
  Por último, se realiza el logging y la suscripción a los topics.

## 07_setup.ino
La finalidad de este fichero es inicializar los recursos de la ESP32-S3 y dejar el sistema en un estado conocido al arrancar.

  ### on_setup()
  Esta función solamente se ejecutará una vez tras la incialización del sistema.
  
  ```cpp
  pinMode(LED_FUNCIONAMIENTO, OUTPUT);
  pinMode(LED_PALET1_LLENO, OUTPUT);
  pinMode(LED_PALET2_LLENO, OUTPUT);
  ```
  Lo primero a llevar a cabo es la configuración de los pines asociados a los LEDs. Se configuran como salida digital (`OUTPUT`).

  ```cpp
  pinMode(BUTTON_VACIAR_PALET1, INPUT_PULLUP);
  pinMode(BUTTON_VACIAR_PALET2, INPUT_PULLUP);
  pinMode(AZULEJO_BUENO, INPUT_PULLUP);
  pinMode(AZULEJO_MALO, INPUT_PULLUP);
  pinMode(AZULEJO_DEFECTUOSO, INPUT_PULLUP);
  ```
  Además, se configuran los botones como entradas con `INPUT_PULLUP`, de forma que la pulsación se detecta en nivel bajo.

  ```cpp
  digitalWrite(LED_PALET1_LLENO, LOW);
  digitalWrite(LED_PALET2_LLENO, LOW);
  setInternalLed(0);
  ```
  Por último, se dejan apagados los LEDs externos y se apaga el LED de funcionamiento para arrancar en un estado conocido.

## 06_comunicacion_leds.ino
Este fichero contiene la función `alRecibirMensajePorTopic()`, que se encarga de interpretar los mensajes MQTT recibidos en diferentes topics y controlar los LEDs correspondientes. Reacciona a mensajes de actualización de estado de palets y controla los indicadores visuales del sistema.

## 02_wifi_lib.ino
Este fichero tiene como propósito gestionar todo lo relacionado con la conexión WiFi de la ESP32-S3. Específicamente este fichero implementa un módulo de comunicaciones WiFi que lleva a cabo lo siguiente:
1. Inicializa la interfaz WiFi de la ESP32-S3.
2. Intenta conectarse a la red configurada en `00_Config.h`.
3. Reconecta automáticamente si se pierde la conexión en algún punto del proceso.
4. Gestiona el cliente TCP/IP que usará el broker de comunicación MQTT.
5. Permite usar TLS/SSL si el proyecto lo requiere.

```cpp
#ifdef SSL_ROOT_CA
  WiFiClientSecure espWifiClient;
#else
  WiFiClient espWifiClient;
#endif
```
Si el proyecto usa **TLS/SSL** se crea un cliente seguro (`WiFiClientSecure`). En el caso contrario, se usa un cliente normal (`WiFiClient`). Este cliente será usado por MQTT.

```cpp
const char* wifiSSID = NET_SSID;
const char* wifiPasswd = NET_PASSWD;
```
Lo que se busca con estas líneas de código es tomar el SSID y la contraseña que previamente se han definido en `Config.h`.

  ### wifi_loop()
  ```cpp
  void wifi_loop(){
    if(!WiFi.isConnected())
      wifi_reconnect(WIFI_CONNECTION_TIMEOUT_SECONDS);
  }
  ```
  Esta función se ejecuta en cada iteración del loop principal. Su principal objetivo es detectar si la ESP32-S3 ha perdido la conexión y si es el caso, intentar reconetar automáticamente.

  ### wifi_connect()
  ```cpp
  WiFi.mode(WIFI_STA);
  trace("MAC Address: ");
  traceln(WiFi.macAddress());
  ```
  Configura la ESP32-S3 como estación WiFi (cliente que se conecta a una red existente, no punto de acceso).
  A continuación, imprime la MAC del dispositivo. Esto se lleva a cabo porque resulta útil al sistema para la depuración del código y para asignar identificadores únicos en la red MQTT.

  ```cpp
  #ifdef SSL_ROOT_CA
    espWifiClient.setCACert(SSL_ROOT_CA);
  #endif
  ```
  Esta parte del código es la encargada de la configuración de certificados en el caso de que se apliquen. Permite validar certificados si se usa TLS.

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

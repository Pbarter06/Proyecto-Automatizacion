# CÓDIGOS ESP32-S3
En esta carpeta se va a proceder a explicar la configuración en Arduino que se ha llevado a cabo para el funcionamiento del sistema embebido, ESP32-S3. Para una amyor organización, se va a dividir la explicación por ficheros.

## Config.h
Este fichero tiene como objetivo definir constantes, parámetros necesarios para conectarse a la red, credenciales y topics para la comunicación a través del broker MQTT. Se agrupan todos estos parámetros en el mismo fichero con el fin de si se requiere la modificación de algunos de estos parámetros poder modificarlos sin alterar el resto del código.

```cpp
#define BAUDS 115200
```
En primer lugar, se define la velocidad de comunicación del puerto serie. En este caso, la velocidad elegida es la estándar para la depuración rápida.

```cpp
#define LOGGER_ENABLE
```
En segundo lugar, si esta línea de código está activa se habilita el sistema logging implementado en el fichero `logger.ino`. En el caso de que no esté habilidato, el loggin se deshabilita de igual manera.

```cpp
#define LOG_LEVEL TRACE
```
A continuación, se define el nivel de severidad mínimo que se mostrará. En este caso, al tratarse de `TRACE` se trata de un nivel más detalado lo que permite ver absolutamente todos los mensajes.

```cpp
#define DEVICE_GIIROB_PR2_ID "00"
```
En cuanto al identificador del dispositivo se ha asignado un identificado al dispositivo del proyecto PR2. Se utiliza para construiir el `deviceID` en `main.ino`. De igual manera, permite distinguir varias ESP32-S3 en la misma red MQTT.

```cpp
#define NET_SSID "UPV-PSK"
#define NET_PASWD "giirob-pr2-2023"
```
Gracias a este bloque de código se puede configurar la red WiFi. Se definen las credenciales de la red WiFi a la que se conectará la ESP32-S3.
- `NET_SSID`: nombre de la red.
- `NET_PASSWR`: contraseña para acceder a la red.
Estas credenciales son utilizadas por el fichero `wifi_lab.ino`.

```cpp
#define MQTT_SERVER_IP "mqtt.dsic.upv.es"
#define MQTT_SERVER_PORT 1883

#define MQTT_USERNAME "giirob"
#define MAQTT_PASSWORD "UPV2024"
```
En este caso, no se configura la red WiFi, sino que se trata de la configuración del broker MQTT. En este caso la dirección del broker MQTT es de la UPV, su puesto estándar sin TLS es 1883.
Y en cuanto a las credenciales, se requiere saber el usuario y la contraseña para la autenticación en el broker. Estas credenciales se utilizan en `mqtt_lib.ino`.

```cpp
#define HELLO_TOPIC "giirob/pr2/devices/hello"
```
Este es el topic que se ha declarado para pruebas inciales del proyecto. La ESP32-S3 envía un mensaje JSON a este topic en `setup.ino`. De igual manera, también se suscribe a él para recibir comandos simples (encender/apagar LED).

```cpp
#define LED_BUILTIN 2
```
Por último, se define el pin físico del LED interno de la ESP32-S3. El pin se utilizará en los ficheros `funciones.ino` y `setup.ino`.

## comunicaciones.ino
Este fichero contiene las funciones que getsionan:
- Suscripciones a topics.
- Recepción de mensajes.
- Envío de mensajes.
  
  ### void suscribirseATopics() 
    ```cpp
    mqtt_subscribe(HELLO_TOPIC);
    ```
    Esta función se llama al iniciar la conexión MQTT. A continuación se suscribe la ESP32-S3 al topic `HELLO_TOPIC` . Además, permite a parte de enviar mensajes, recibirlos a través de ese canal.

  ### void alRecibirMensajePorTopic()
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

  ### void enviarMensajePorTopic(const char* topic, STring outgoingMessage):
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
Este fichero contiene únicamente la función `on_loop()`, la cual representa la parte del programa que se ejecuta de manera repetitiva durante todo el proceso de ejecución.

```cpp
long now, lastMSg = 0;
long sensorUpdateInterval = 5000;
```
  ### now
   Esta variable es la encargada de guardar el tiempo actual en milisegundos desde que la ESP32-S3 se encendió. Esto se obtiene a través de `milis()`.
  
  ### lastMsg
  Esta variable guarda el instante en el que se ejecutó por última vez la tarea periódica. 
  Se inicializa a 0.
  
  ### sensorUpdateInterval
  En el caso de esta variable se trata de una variable que representa el intervalo de actualización en milisegundos. Al estar igualado a  5000 milisegundos, equivalente a 5 segundos, indica que la tarea periódica se ejecutará cada 5 segundos.
  
## main.ino
Este fichero se trata del fichero que contiene la estructura principal del programa. Su función es inicializar el sistema, configurar las comunicaciones WiFi y MQTT.

```cpp
String deviceID = String("giirobpr2-device-") + STring(DEVICE_GIIROB_PR2_ID);
```
Primeramente, se define un identificador único del dispositivo. Se usa para registrarse en el broker MQTT.

  ### setup()
  Esta función se ejecuta una sola vez al arrancar la ESP32-S3.
  ```cpp
  #ifdef LOGGER_ENABLED
    Serial.begin(NAUDS);
    delay(1000);
    Serial.println();
  #endif
  ```
  Lo siguiente a definir un identificador es la incialización de logger. INicia el puerto seria a 115200 baudios y permite imrimir mensajes de depuración. No obstante, solo se activa se `LOGGER_ENABLED` está definido en el ficher `Config.h`.
  
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
  Esta línea de código implica la llamada a la función definida peviamente en el fichero `comunicaciones.ino`. Es en esta función donde se añaden todos los topics que la ESP32-S3 debe escuchar o utilizar para enviar mensajes.

  ```cpp
  on_setup();
  ```
  Lo último a realizar en esta función es la configuración adicional del dispositivo mediante la función `on_setup()` definida en `setup.ino`. En ese fichero se realiza la configuración de pines, la inicialización del LED y el envío de mensajes JSON.
  
### void loop()
  Esta función se ejecuta continuamente mientras la ESP32-S3 está encendida.
  ```cpp
  wifi_loop();
  mqtt_loop();
  on_loop();
  ```
Como se puede observar, dentro de la función loop() se realiza el mantenimiento de la conexión WiFi, MQTT y las tareas periódicas que se llevan a cabo en la función `on_loop()`.

## mqtt_lib.ino
La función de este fichero es establecer la conexión con el broker MQTT, mantener la conexión activa, en caso de que la conexión WiFi se pierda reconectar, publicar mensajes, suscribirse a topics para procesar los mensajes entrantes mediante un callback.
```cpp
#define MQTT_CONECTION_RETRIES 3
PubSubClient(espWifiClient);
```
Primeramente, se deben definir todos aquellos parámetros iniciales y clientes de MQTT. En este caso, de define el número máximo de intentos de reconexión antes de finalizar la conexión. Luego, se crea un cliente MQTT usando el cliente WiFi (`espWifiClient`) definido en el fichero `wifi_lib.ino`. Este objeto es el que realmente se comunica con el broker.

```cpp
const char* mqttServerIP = MQTT_SERVER_IP;
unsigned int mqttServerPort = MQTT_SERVER:PORT;
String mqttClientID;
```
Continuando con los parámetros iniciales, en este apartado se carga los parámetros definidos en `Config.h` (IP del broker, puerto y ID del cliente el cual se asignará en `mqtt_connect()`).

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
    2. Llama a `mqttClient.loop()`: en esta fase se procesa mensajes entrantes y mantiene activa la conexión. En el caso de esta función es imprescindible llamarla de manera continua.
    
### void mqtt_connect(String clientID)
  En un primer instante, esta función recibe como parámetro el ID del dispositivo desde `main.ino`. Se busca llevar a cabo la configuración del cliente y intentar mantener la conexión.

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
  El primer paso a seguir en esta función es comprobar que haya conexión a WiFI. Si no hay conexión no se intenta conectar con el broker MQTT. En el caso de que ocurra esta situación, se enviará un mensaje de aviso informando que se el dispositivo se encuentra en estado de desconexión. Posterior a imprimir por pantalla el aviso, se encuentra un bucle que se repite hasta que se consiga reconectar con la red WiFi o, en caso de no obtener éxtito, cerrar el programa porque se han agotado los intentos de reconexión.

    ```cpp
    #ifdef MQTT_USERNAME
      if ( mqttClient.connect(mqttClientID.c_str(), MQTT_USERNAME, MQTT_PASSWORD) ) {
    #else
      if ( mqttClient.connect(mqttClientID.c_str()) ) {
    #endif
    ```
  Una vez llegado a esta sección de código, se realiza un intento de conexión. Si existe un usuario con contraseña el sistema los utiliza. En el caso contrario se busca conectar sin la autenticación.
  Cuando se realiza una conexión exitosa se espera 1 segundo para estabilizar esta. No obstante, si falla se muestra el código error gracias a la gestión de errores que se implementa y se realiza una espera de 5 segundos antes de reintentar la conexión.

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
  Más tarde, se llama a la función definida en `comunicaciones.ino` que parse el objeto JSON, interpreta comandos y principalmente, controla el LED.

### void mqtt_publish(const char* topic, String outgoingMessage)
  Esta función tiene como objetivo principal la publicación de los mensajes.

  ```cpp
  if ( !mqttClient.connected() ) {
    errorln("Cannot send message ... MQTT Client is disconnected!!")
    return;
  }
  ```
  El primer paso a realizar es comprobar la conexión. Luego, se trata con el loggin y su posterior publicación a través de `mqttClient.publish(topic, outgoingMessage.c_str())` que envía el mensaje al broker.

### void mqtt_suscribe(const char* topic)
  Esta función es la que permite la suscripción a los topics correspondientes. Al igual que en los casos anteriores, el primer paso que se realiza es la comprobación de la conexión.

  ```cpp
  trace("Subscribed to topic: ");
  traceln(topic);
  mqttClient.subscribe(topic);
  ```
  Por último, se realiza el loggin y la suscripción a los topics.

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

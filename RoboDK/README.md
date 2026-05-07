# CÓDIGOS ROBODK
En esta carpeta se va a proceder a explicar la lógica implementada en los códigos que se ha llevado a cabo para el funcionamiento de la simulación de la celda de trabajo en RoboDK.

## Cintas
Dentro de la carpeta de cintas se encuentran los códigos de las diferentes cintas que se implementan en la celda de la fábrica. Todas las cintas tienen la misma estructura:
- `avanceCinta.py`
- `resetCinta.py`
Como la estructura aplicada en el programa `resetCinta.py` es equivalente en todos los códigos de las diferentes cintas, a continuación se explicará más detalladamente la estructura seguida de manera general. Sin embargo, los programas de avances de las cintas se agruparán de la diferente manera; por una parte se explicará el fichero Python de las cintas 1 y 2, luego el de las cintas 3 y 4 y, por último, el programa de avance de las cintas de los azulejos. Este último se explicará a parte, puesto que su funcionamiento es diferente al resto.

 ### resetCinta.py
  La estructura general utilizada para los programas de reset de las cintas es el siguiente:
  ```py
  from robodk import robolink
  from robodk import robomath
  RDK = robolink.Robolink()

  cinta = RDK.Item('CajasX')
  if cinta.Valid():
    cinta.setJoints([0])
  ```
  Para un buen funcionamiento en la simulación es necesraio la importación de la API principal de RoboDK; además de importar las utilidades requeridas para el procedimiento a seguir. Posteriormente, se conecta el script con la instancia abierta de RoboDK y obtiene el objeto de la cinta correspondiente.
  Luego, es obligatorio para el funcionamiento que se compruee que el objeto existe en la estación de trabajo, si exite, entonces resetea la posición de la cita a 0, su posición inicial.

  ### avanceCinta.py // Cinta 1 y 2
  Ambos programas de las cintas son idénticos excepto por los nombres asignados. 
  Para la inicialización se importan las librerías necesarias, se conecta al RoboDk como en el caso del programa `resetCinta.py`.
  ```py
  caja = RDK.Item('cajaA1')
  fotocelula = RDK.Item('Fotocelula1')
  frame = RDK.Item('CintaCaja1')
  cinta = RDK.Item('Cajas1')
  INCREMENTO_MN = 406
  ```
  Luego, se obtienen los objetos de la estación como se puede observar. Además, se define cuánto avanza la cinta en cada paso. Lo siguiente que se realiza en el código es dentro de un bucle infinito.
  ```py
  lista_caja = frame.Childs()
  detectado = False
  ```
  Por un lado se busca obtener las cajas actuales. `frame.Childs()` devuelve todos los objetos hijos del frame (las cajas). Y `detectado` indica si la fotcélula ha detectado una caja.

  ```py
  while not detectado:
    cinta.MoveJ(cinta.Joints()+INCREMENTO_MM)
    for caja in lista_caja:
        if caja.Name():
            if fotocelula.Collision(caja):
                detectado = True
                RDK.setParam('SenyalSensor1', 1)
                break
  ```
  Este bloque de código realiza el avance hasta detectar una caja. La cinta avanza en incrementos declarados al principio del programa, se revisa cada caja y si la fotocélula detecta colisión es que hay caja. Entonces, se activa el parámetro `SenyalSensorX`.

  ```py
  while detectado:
    done = RDK.getParam('Done1')
    if done == 1:
        detectado = False
    time.sleep(0.1)
  ```
  Lo siguiente a realizar es la espera a que el robot termine. La unidad robótica Ur5e pone `DoneX = 1` cuando termina de recoger la caja. Hasta no recibir ese dato, la cinta no avanza.

  ```py
  cinta.MoveJ(cinta.Joints()+INCREMENTO_MM)
  RDK.setParam('SenyalSensor1', 0)
  lista_caja = frame.Childs()
  
  for item in lista_caja:
      if item.Name().startswith('Azulejo'):
          item.Delete()
  
  RDK.setParam('Done1', 0)
  cinta.setJoints([0])
  ```
  Por último, este bloque de código es el fundamento del avance, borrado y reseteo tanto de las cajas como de las cintas. COn respecto a la cinta, ésta avanza para dejar espacio, luego se apaga el sensor y se borran los azulejos que ya han sido procesados. En ese instante, se resetea el parámetro Done y por tanto, se resetea la cinta.

  ### avanceCinta.py // Cinta 3 y 4
  Estas cintas son iguales excepto el funcionamiento especial de algunos parámetros. En estos programas solo se avanza cuando DoneX = 1, se detecta caja y en el caso de que la caja pase, se genera una nueva caja con `spawnear_caja()`.
  ```py
  template = RDK.Item('cajaBase')
  template.Copy()
  nueva_caja = RDK.Paste(frame)
  nueva_caja.setName("cajaC")
  nueva_caja.setVisible(True)
  nueva_caja.setPose(robomath.eye(4))
  ```
  Esta función permite copiar un objeto plantilla. En este caso, lo pega dentro del frame, lo renombra y lo hace visible. Luego lo coloca rn a posición inicial, de manera que simula la aparición de otra caja.

  ### avanceCinta.py // Cinta Azulejo
  Esta cinta genera azulejos, detecta la fotocélula y borra azulejos según su tipo. Como el proyecto automatizado lleva a cabo el control de calidad de azulejo, es de obligatorio cumplimiento la clasificación del azulejo según sus condiciones. Para una mejor distinción se han establecido 3 estados diferentes; bueno (1) si no presenta nigún defecto en su diseño, defectuoso (2) si cuenta con alguna modificación en su diseño o forma y roto (3). Asimismo, esta cinta avanza a una velocidad diferente en relación con el tipo de azulejo que se trate, es por ello por lo que se usa dos incrementos diferentes.

  ```py
  INCREMENTO_MM = 1680 
  INCREMENTO_B = 350
  tipo = RDK.getParam('TipoAzulejo')
  ```
  - `INCREMENTO_MN = 1680 ` se trata del incremento normal.
  - `INCREMENTO_B = 350 ` se trata de un incremento extra para aquellos azulejos defectuosos

  Para la detección de azulejos se implementa de la misma manera que en los casos anteriormente comentado.

  ```py
  if tipo == 3:
    cinta.MoveJ(cinta.Joints() + INCREMENTO_B)
    for item in lista_azulejos:
        if item.Valid() and item.Name().startswith('Azulejo'):
            item.Delete()
            lista_azulejos.remove(item)
            break
    detectado = False
  ```
  Cuando por la cinta avaza un azulejo cuyo estado es roto, éste tiene una implementación especial. Cuando sucede esta eventualidad, la cinta avanza un poco más y luego, una vez el azulejo llega a la zona de la papelera -situada al final de la cinta- se borra el azulejo y se limpia la pista de la cinta. Una vez se haya cumplido estos pasos de manera correcta, se reinicia el ciclo y se vuelve a generar de nuevo un azulejo mediante la instrucción `azulejo = spawnear_azulejo()`.
  
## MQTT
Para conseguir una comunicación exitosa se requiere de 3 fases principales de la comunicación a través del broker MQTT:
1. Enviar MQTT
2. Recibir MQTT de borrado
3. Recibir MQTT de spawneo

 ### Enviar MQTT
 Principalmente hay 3 scripts que son los encargados de publicar en MQTT:
 - Scripts que publican en `sim/working`
 - Scripts que publican en `sim/working/palet1`
 - Scripts que publidan en `sim/working/palet2`

La estructura general que se siguen en los scripts de ON/OFF es la siguiente:
```py
import paho.mqtt.client as mqtt

broker = "broker.emqx.io"
port = 1883
topic_destino = "..."

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.connect(broker, port, 60)

mensaje = "on"  # o "off"
mqttc.publish(topic_destino, mensaje)

mqttc.disconnect()
```
Al igual que en todos los casos anteriores, lo primero que se realiza es la importación de la librería correspondiente. En este caso se trara de la librería oficial de Python para MQTT. Esta librería permite crear clientes, conectarse a un broker y publicar mensajes. Pero para ello, se debe realizar una configuración adecuada. 
Con respecto a la configuración se debe tener en cuenta los siguientes parámetros:
- `broker.emqx.io` : se trata de un broker público.
- `port = 1883` : puesto estándar MQTT sin cifrado.
  
Una vez se ha realizado bien la configuración, se definen los topics anteriormente menncionados. Estos topics determinan a qué canal MQTT se envía el mensaje. No obstante, para enviar el mensaje previamente s edebe crear el cliente MQTT de la siguiente maner:
```py
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

```
Gracias a esta línea de código se crea el cliente y el parámetro `VERSION2` se trata de la API moderna de _CallBacks_.
Lo siguiente a tener en cuenta es la conexión del broker. Para ello, dentro de la función `mqtt.connect()` se introducen los parámetros de broker, port y 60. Este último parámetro es el **keep-alive**, en otras palabras, el tiempo másximo sin actividad.
Por último, para publicar el mensaje deseado se puede realizar de dos maneras diferentes:
- Manera 1:
  ```py
  mensaje = "on"
  mqttc.publish(topic_destino, mensaje)
  ```
  
- Manera 2:
  ```py
  mensaje = "off"
  mqttc.publish(topic_destino, mensaje)
  ```
  Publica el mensaje en el topic deseado.

  Para finalizar, se debe realizar el cierre con la conexión de manera correcta para evitar posibles conflictos.
  
 ### Recibir MQTT // Borrado
 En esta fase de comunicación MQTT cuenta con dos scripts a comentar

  #### LeerMQTTB.py
  Este script es el receptor MQTT que escucha mensajes y los pasa al controlador.
  Al inicio, como de costumbre se importa la API de RoboDK y las librerías requeridas para el proceso que se va a llevar a cabo. No obstante, además se importa el módulo `RobotControllerB.py` que contiene la lógica de respuesta. Luego, se configura el broker de igual manera que en los scripts anteriores, pero conla modificación de que se trata del topic donde este script escucha mensajes.
  ```py
  def on_message(mqttc, obj, msg):
    payload = msg.payload.decode('utf-8')
    topic = msg.topic
    qos = msg.qos
    rc.handle_message(mqttc, topic, payload, RDK)
  ```
  Este bloque de código representa el _Callback_ y cómo funciona internamente el proceso cuando se recibe un mensaje. El `payload` es el contenido del mensaje recibido a través del topic correspondiente. Mientras que el parámetro `qos` representa la calidad del servicio. Luego, se llama a `handle_menssage()` del controlador, pasándole el cliente MQTT, el topic, el mensaje y el objeto RDK para manipular RoboDK.
  Cabe aclarar que este script no toma decisiones ni envía mensajes, solamente se centra en recibir y delegar la información que le llega.

  Al mismo tiempo, se crea el cliente MQTT y se le asigna la función `on_message` como callback. Así mismo, se conecta al broker y se suscribe al topic `sim/working/button/empty`se la siguiente manera:
  ```py
  mqttc.connect(broker, port, 60)
  mqttc.subscribe(base_topic, 0)
  ```
  Para luego publicar el mensaje "_ready_" que informa al sistema de que el receptor está activo. Y por último, pero de vital importancia, se debe mantener el cliente escuchando infinitamente los mensajes que se reciban a través de un bucle infinito.
  
  #### RobotControllerB.py
  Este script es el cerebro que se encraga de interpretar el mensaje recibido y actúa en RoboDK.
  Su función principal es `def handle_message(mqtt_client, topic, mensaje, RDK)` que recibe el cliente MQTT, el topic por donde llegará el mensaje, el contenido del mismo y la conexión a RoboDK.
  Luego, se imprime el mensaje recibido a través de un `print` y se convierte el mensaje a número. En el caso de que el mensaje ya se tratase de un número no entraría en el bloque de código y no se modificaría nada.
  Una vez que el mensaje se encuentra en el tipo de dato correspondiente se procede a la interpretación del mismo.
  El mensaje puede variar entre `1` y `2` . Si se recibe un `1` significa que se debe vaciar el palet 1, en caso contrario, el palet a vaciar sería el 2.
  - tipo == 1 :
     ```py
     if not prog1.Valid():
     print("Error: No se encontró el programa 'Palet1OFF'")
     return
     ```
     Lo primero es la gestión de errores. Es por ello por lo que se verifica si el programa existe.
     ```py
     for item in lista_palet1:
     if item.Valid() and item.Name().startswith('cajaC'):
         item.Delete()
     RDK.setParam('x3', 0)
    RDK.setParam('y3', 0)
    RDK.setParam('z3', 0)
    RDK.setParam('LuzPalet1', 0)
     ```
     Lo segundo a realizar es el borrado de todas las cajas del palet 1, para luego resetear los parámetros. En otros términos, se resetea las coordenasad y luz del palet para por último, ejecutar el programa de RoboDk de la siguiente manera:
     ```py
     resultado = prog1.RunProgram()
     ```
  - tipo == 2:
    El procedimiento a seguir es equivalente al anterior pero en el espacio de trabajo del palet 2.
  
 ### Recibir MQTT / Spawneo
 En este script se encuentran similitudes con el script anterior, ya que ambos scripts llevan a cabo la imporatción de RoboDK y MQTT -al igual que todos los scripts generados- , realizan un Callback() a través de `on_message()`, se conectan al broker -obligatorio para su funcionamiento- y publican un mensaje "_ready_" para mostrar al sistema que todo está funcionando correctamente y puede ejecutar `loop_forever()`. Sin embargo, la gran diferencia entre ellos es que el scritp `RecibeMQTT_borrado` solo recibe mensajes MQTT a través del topic `sim/working/button/empty` y este segundo script, interpreta el mensaje y actúa en RoboDK a través del topic `sim/working/button/spawn`.
 Por otra parte, otro aspecto a destacar es que en este script el controlador implementeaod es distinto. Antes se importaba:
 ```py
  import RobotControllerB as rc
 ```
 Pero, para la realización del spawn se importa este controlador:
 ```py
  import RobotControllerS as rc
 ```
  Este cambio se ha llevado a cabo porque este controlador no borra cajas ni ejecuta programas, solamenet actualiza un parámetro global denominado `TipoAzulejo`. Este parámetro lo usa CintaAzulejos para decidir lo siguiente:
  - TipoAzulejo `1` : se trata de un azulejo en buen estado, por lo que avanza normal por la cinta.
  - TipoAzulejo `2`: se trata de un azulejo defectuoso, por lo que de igual manera avanza con normlidad a lo alrgo de la cinta.
  - TipoAzulejo `3`: se trata de un azulejo roto, por lo que avanza un espacio extra y se borra el azulejo.
  Este parámetro es la base de la comunicación entre MQTT y las cintas.

  En conclusión, el script leerMQTTS.py en su mayor porcentaje es equivalente al script leerMQTTB.py excepto por los topics con los que se trabaja y el controlador importado.
 
## Calidad de Vida
Este script se centra en el borrado de todos los azulejos que existan en las tres zonas diferentes de la estación de trabajo de RoboDK.
Una vez se han realizado las importaciones requeridas por el proceso, además de la conexión al RoboDK, se busca obtener los frames donde buscar azulejos.
```py
frame1 = RDK.Item('CintaCaja1')
frame2 = RDK.Item('CintaCaja2')
frame3 = RDK.Item('SMC ZXP7A01-ZP20U-X1 Vacuum Gripper')
```
El `frame1` contiene las cajas/azulejos de la Cinta 1. Mientras que el `frame2` contiene las cajas/azulejos de la Cinta 2. Y en cuanto al `frame3` , éste contiene los objetos agarrados por la ventosa de la unidad robótica correspondiente. El script busca el borrado de los azulejos en estos tres escenarios. Para ello, requiere de los objetos hilos de cada frame:
```py
lista_caja1 = frame1.Childs()
lista_caja2 = frame2.Childs()
lista_caja3 = frame3.Childs()
```
En este caso, `Childs()` devuelve todos los objetos dentro del frame, por lo que en el caso de la celda devolverá las cajas y los azulejos principalmente -también pueden aparecer otros elementos que se encuentren dentro del frame-. Esto permite recorrerlos uno a uno para decidir cuáles se deben eliminar.

### Borrado de azulejos de la Cinta 1
```py
for item in lista_caja1:
    if item.Name().startswith('Azulejo'):
        item.Delete()
```
En esta ocasión, se recorre todos los objetos dentro de `CintaCaja1` y si el nombre del objeto empieza por "_Azulejos_" en ese caso se borra de la estación. De esta manera, se consigue eliminar todos aquellos azulejos que se encuentren en la Cinta 1.

### Borrado de azulejos de la Cinta 2
```py
for item in lista_caja2:
    if item.Name().startswith('Azulejo'):
        item.Delete()
```
El proceso para el borrado de los azulejos de la Cinta 2 es equivalente al anterior.

### Borrado de azulejos de la Ventosa del Robot
```py
for item in lista_caja3:
    if item.Name().startswith('Azulejo'):
        item.Delete()
```
Por último, para el borrado de azulejos en el escenario de la herramienta del cobot se ha utilizado una implementación similar. Lo único a destacar es que se recorren todos los objetos -al igual que en los casos anteriores- que se encuentran en la ventosa. 

## Base de Datos
Este script permite conectarse a PostgreSQL e insertar un azulejo y una caja llena en sus tablas correspondientes.
Al igual que en los scripts anteriores, éste también requiere de la importación de la librería aunque en este caso la de PostgreSQL. Luego, para que se pueda conectar y interactuar con RoboDK se abre una conexión con PostgreSQl mediante `psycopg.connect()`. Esta función recibe como parámetros `dbname` como nombre de la base de datos, `user` como usuario de PostgreSQL con su respectiva contraseña. Y cuenta también con un `host` y `port` que hacen referencia al servidor (local) y el puerto etsándar de PostgreSQL respectivamente. Si la conexión funciona, imprime un mensaje de éxito. 
```sql
cur = conn.cursor()
```
El siguiente paso es crear un cursos. EL cursos es el objeto que permite ejecutar sentencias SQL. Todo lo que se inserte, se borre o se consulte se realiza a través de él.
Los últimos pasos a realizar son las instrucciones INSERT en la tabla Azulejo y en Caja_Llena

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

## Calidad de Vida

## Base de Datos

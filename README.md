# Automatizacion_Fabrica_Azulejos

**PR2-2-6**

## Integrantes del grupo
- Finn Alai Perea Oltmann
- Claudia Moreno Martínez
- Ainhoa López Gómez
- Paula Barona Terol

  ## 1. ¿En qué consiste la propuesta de automatización?
   Esta propuesta de automatización se centra en el control de calidad, empaquetado y paletizado de azulejos. El objetivo principal de la automatización es optimizar la línea de producción dividendo el flujo de trabajo en 2 procesos:
  - **Fase 1. Control de Calidad y Empaquetado** : Los azulejos se desplazan por una cinta mecánica donde un sistema de visión artificial se encargará de inspeccionar el estado del azulejo. Dependiendo del estado, la unidad robótica correspondiente se encargará de acercarse a la posición de pick y descargar el azulejo en la posición de place correspondiente.
  - Tipos de Azulejos:
    - Buen estado: No presenta ningún defecto en su diseño, por lo que se depositará en las cajas correspondientes a este estado para una venta de primera calidad.
    - Defectuoso: Presenta algún defecto en su diseño o dorma, por lo que se depositará en las cajas correspondientes a este estado para una venta de segunda calidad con un precio reducido al incial.
    - Roto: El robot no recoge el azulejo, éste se sigue desplazando por la cinta mecánica hasta caer en la basura.
  - **Fase 2. Paletizado de las cajas** : Una vez que las cajas de la fase anterior se llenan, una segunda cinta mecánica las traslada a la zona de paletizado. Allí, una segunda unidad robótica identifica el tipo de caja y la apila de forma ordenada en su palet correspondiente, dejándolo listo para su retirada y distribución.

  ## 2. Elementos que participan en la celda de automatización
  Para llevar a cabo la propuesta de automatización, la celda de trabajo integra diferentes componentes:
    - **Sistema de Visión Artificial** (`Cámara Motrix Iris GTR`): Actúa como sensor principal del control de calidad. Se sitúa sobre la primera cinta transportadora y es la encargada de analizar y determinar en qué estado se encuentra el azulejo. No obstante, debido a las circustancias del proyecto, no es posible la programación e implementación de este elemento para su demostración, por lo que será sustituído por un sistema embebido (ESP32-S3). De esta manera, el operario contará con 3 botones -uno por cada estado posible del azulejo- y una vez pulsado, esta información se enviará a través de un broker de comunicación (MQTT) a la aplicación Python, quien mandará ejecutar las tareas correspondientes a las unidades robóticas.
    - **Unidades Robóticas** : En cuanto a las unidades robóticas, esta propuesta busca implementar dos robots cooperativos.
      - Ur5e : Se sitúa al final de la cinta tranpsortadora por la que vienen los azulejos. Es el encargado de paletizar los azulejos (proceso 1) en sus cajas correspondientes dependiendo del tipo de venta al que posteriormente se van a exponer hasta llenarlas. En total, cada caja alberga en su interior un total de 10 azulejos.
      - UR30 : Se sitúa entre medias del final de las cintas transportadoras por las que vienen las cajas ya empaquetadas y listas para paletizarlas. Es el encargado de paletizar el producto ya empaquetado y depositarlo en el palet, para su posterior retirada.
    - **Sensor de Presencia** (`Sensor SICK WL4S laser Sensor`): Se sitúa al final de las cintas transportadores y se encarga de controlar la presencia o la no presencia de piezas (azulejos/cajas). Este sensor a diferencia del resto de sensores infrarrojos utiliza láser rojo altamente enfocado. Lo cual supone una gran ventaja, ya que genera un spot de luz muy pequeño y muy nítido, lo que permite una detección de bordes extremadamente precisa.
    - **Herramientas de agarre** : Cada unidad robótica cuenta con una garra, lo que les permite poder llevar a cabo sus funciones de paletizado de forma eficaz.
      - OnRobot VGP20 Vacuum Gripper : Herramienta de trabajo del UR30. Garra de vacío eléctrica que consta con capacidad de carga hasta de 20 Kg.
      - SMC ZXP7A01-ZP20U-X1 Vacuum Gripper : Herramienta de trabajo del Ur5e. Garra formada por 4 ventosas situadas a los laterales. Esta geometría permite agarrar los azulejos con mayor firmeza. Capacidad de carga 7 Kg.
    - **Cintas mecánicas** : Se ha optado por implementar 5 cintas mecánicas en total.
      - Longitud: 2000 mm
      - Anchura: 400 mm
    - **Cajas** : El tamaño de las cajas viene determinado directamente por la proporción del azulejo. En total, alberga 10 azulejos (2 columnas de 5 filas).
      - Ancho: 180 mm
      - Largo: 280 mm
      - Alto: 120 mm
  - **Azulejos** : Se ha optado por producir azulejos con tamaño estándar para la industria (180 mm x 140 mm), ya que se trata de uno de los tamaños más solicitados por los clientes.
  - **Palets** : Para el transporte de los azulejos se han implementado 2 palets (para azulejos en buen estado y para azulejos de segunda venta) de mismo tamaño (800 mm x 800 mm). Este tamaño permite a la empresa paletizar un total de 6 cajas (apilables a 3 alturas).

  ## 3. Arquitectura de Comunicaciones
  Un pilar fundamental de esta propuesta de automatización es la coordinación entre los diferentes elementos de la planta. Para un buen funcionamiento, el sistema cuenta con una comunicación bidireccional en tiempo real a través de la arquitectura basada en el protocolo MQTT. Por un lado, la ESP32-S3 publica (`publish`) datos hacia el servidor indicando eventos del proceso productivo (como la detección de un tipo de azulejo o la notificación de retirada de un palet). Por otro lado, la placa se suscribe (`suscribe`) a topics del sistema para recibir órdenes externas que le permiten encender indicadores LED.

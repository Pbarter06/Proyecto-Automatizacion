# CÓDIGOS BASE DE DATOS 
En esta carpeta se va a decsirbir la estructura, relaciones y contenido inicial de la base de datos utilizada en el proyecto automatizado.
La base de datos modela el flujo de factores externos con el paletizado, empaquetado y control de calidad de los azulejos. Asimismo, la base de datos se compone en dos ficheros:
- azulejos.sql : fichero enfocado a la creación del esquema y tablas de la base de datos.
- poblar_azulejos.sql : fichero que lleva a cabo la inserción de datos reales para la población de la misma.

  ## azulejos.sql
  Primeramente, cabe definir la estructura general del esquema de la siguiente manera:
  ```sql
  CREATE SCHEMA Azulejo;
  SET search_path TO Azulejo;
  ```
  Estas instrucciones de código permiten crear el esquema de azulejos y se establece como espacio de trabajo.
  A continuación, se describen todas las tablas con sus respectivos atributos, sus claves primarias, sus restricciones correspondientes y sus claves ajenas.
  ### Tabla Cliente
  ```sql
  CREATE TABLE Cliente(
    NIF VARCHAR(9) PRIMARY KEY,
    Teléfono VARCHAR(15) NOT NULL,
    Correo VARCHAR(150) NOT NULL,
    Dirección VARCHAR(100)
  );
  ```
  En esta tabla se almacena todos los datos de aquellos clientes que realizan pedidos a la fábrica. En el caso de esta entidad, se establece como identificador único a cada cliente, el NIF, ya que normalemente los clientes se van a tratar de empresas y no de individuos.

  ### Tabla Pedido
  ```sql
  CREATE TABLE Pedido(
    Código_compra VARCHAR(10) PRIMARY KEY,
    Precio REAL NOT NULL,
    Fecha_compra DATE NOT NULL,
    NIF_Cliente VARCHAR(9) NOT NULL,
    FOREING KEY (NIF_Cliente) REFERENCES Cliente(NIF)
      ON UPDATE CASCADE ON DELETE RESTRICT
    );
  ```
  Esta tabla específicamente representa los pedidos realizados por los clientes. Cada pedido pertenece a un cliente. Esta asociación se representa mediante la clave ajena en el atributo NIF_Cliente que hace referencia al NIF de la tabla de Cliente. Cabe destacar que `ON DELETE RESTRICT` evita borrar clientes con pedidos asociados.

  ### Tabla Caja_Llena
  ```sql
    CREATE TABLE Caja_Llena(
      ID_Lote VARCHAR(10) PRIMARY KEY,
      Tamano REAL NOT NULL,
      Tipo CHAR(12) NOT NULL,
      Código_compra VARCHAR(10) NOT NULL,
      CHEK (Tipo IN ('roto' , 'defetuoso', 'bueno')),
      FOREING KEY (Código_compra) REFERENCES Pedido(Código_compra)
        ON UPDATE CASCADE ON DELETE RETSRICT
      );
    ```
    Esta tabla contiene las cajas ya llenas con azulejos clasificados por diferentes estados. Los posibles estados están definidos el la variable `Tipo`.  Esta variable solo puede tener uno de estos valores: `roto`, `defectuoso` o `bueno`. Cada caja llena pertenece a un pedido.

   ### Tabla Azulejo
    ```sql
    CREATE TABLE Azulejo (
      N_Serie VARCHAR(10) PRIMARY KEY,
      Estado CHAR(10) NOT NULL,
      ID_Lote VARCHAR(10) NOT NULL,
      CHEK (estado IN ('roto' , 'defectuoso' , 'bueno' )),
      FOREING KEY (ID_Lote) REFRENCES Caja_Llena(ID_Lote)
        ON UPDATE CASCADE ON DELETE RETSRICT
      );
    ```
    Esta tabla es la encargada de almacenar cada azulejo individual con su código identificador único (`N_Serie`), su estado y la caja a la que pertenece. Cada azulejo pertenece a una caja llena.

  ### Tabla Proveedor
  ```sql
  CREATE TABLE Proveedor(
    NIF VARCHAR(10) PRIMARY KEY,
    Telefono VARCHAR(15) NOT NULL,
    Direccion VARCHAR(100) NOT NULL,
    Correo VARCHAR(150) NOT NULL
  );
  ```
  Llegados a este punto de la base de datos, la tabla de proveedor almacena los proveedores de cajas vacías, ya que la fábrica de azulejos ha optado por subcontratar a otra emrpresa para el empaquetado de los azulejos.

  ### Tabla Caja_Vacía
  ```sql
  CREATE TABLE Caja_Vacía(
    N_Lote VARCHAR(10) PRIMARY KEY,
    Tamano INT NOT NULL
  );
  ```
  En cuanto a esta tabla, reserva ciertas similitudes a la tabla de `Caja_Llena`. SIn embargo, al tratarse de una caja vacía no se requiere saber el estado de los azulejos que va a almacenar.

  ### Taba Compra
  ```sql
  CREATE TABLE Compra(
    NIF_Proveedor VARCHAR(10) NOT NULL,
    N_Lote VARCHAR(10) NOT NULL,
    Fecha_compra DATE NOT NULL,
    Precio_final REAL NOT NULL,
    PRIMARY KEY (NIF_Proveedor ) REFERENCES Proveedor(NIF),
    FOREING KEY (NIF_Proveedor) REFERENCE Proveedor(NIF),
    FOREING KEY (N_Lote) REFERENCE Caja_Vacía(N_Lote)
  );
  ```
  En esta última tabla definida se almacena el historial de compras de cajas vacías a proveedores.
  
  ## poblar_azulejos.sql
  El fichero `poblar_azulejos.sql` contiene el conjunto de instrucciones SQL necesarias para insertar datos reales en todas las tablas del esquema. Su objetivo es proporcionar un conjunto de datos coherente y completo. Este fichero ha sido realizado en gran mayoría con la ayuda de la Inteligencia Artificial.
   Al igual que el anteriore fichero, éste se ha organizado en 7 secciones, cada una correspondiente a una tabla del modelo.

  ### PROVEEDORES
  ```sql
  INSERT INTO Proveedor (NIF, Telefono, Direccion, Correo)
  VALUES
  ```
  En esta sección de código se insertan 9 proveedores reales, con datos completos:
    - NIF
    - Teléfono
    - Dirección
    - Correo Electrónico
  Estos proveedores suministran las cajas vacías que posteriormente se llenarán de azulejos.

  ### CAJA_VACÍA
  ```sql
  INSERT INTO Caja_Vacia(N_Lote, Tamano)
  VALUES
  ```
  Así pues, en este casos se insertan 7 cajas. Estas cajas son las unidades básicas que se compran a proveedores.
  
  ### COMPRA
  Se registra un historial apliado de compras donde se almacena el proveedor, el lote comprado, su fecha y el precio final. Cada compra debe cumplir:
    - `NIF_Proveedor`
    - `N_Lote`
  
  ### CLIENTE
  ```sql
  INSERT INTO Cliente (NIF, Telefono, Correo, DIreccion)
  VALUES
  ```
  De igual manera, se insertan 10 clientes, cada uno con su correspondiente `NIF`, `Teléfono`, `Correo`y `Dirección`. estos clientes serán los destinatarios de los pedidos.
  
  ### PEDIDO
  ```sql
  INSERT INTO Pedido (codigo_compra, Precio, Fecha_compra, NIF_Cliente)
  VALUES
  ```
  Aquí, se insertan 13 pedidos, cada uno asociado a un cliente.
  
  ### CAJA_LLENA
  ```sql
  INSERT INTO Caja_Llena(ID_Lote, Tamano, Tipo, Código_compra)
  VALUES
  ```
  Se insertan 17 cajas llenas, clasificadas por:
    - Tamaño
    - Tipo
    - Pedido al que pertenecen
    - Código_compra
  
  ### AZULEJOS
  ```sql
  INSERT INTO Azulejo (N_Serie, Estado, ID_Lote)
  VALUES
  ```
  Finalmente, se insertan más de 70 azulejos individuales, cada uno con su respectivo número de serie, estado, lote al que pertenecen y ID. Asimismo, los azulejos están organizados por lotes según el estado en el que se encuentren.

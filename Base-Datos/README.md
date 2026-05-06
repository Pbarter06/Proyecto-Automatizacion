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

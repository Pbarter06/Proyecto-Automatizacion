CREATE SCHEMA azulejos;
SET search_path TO azulejos;

-- ============================================
-- CLIENTE
-- ============================================
CREATE TABLE Cliente (
    NIF           VARCHAR(9) PRIMARY KEY,
    Telefono      VARCHAR(15) NOT NULL,
    Correo        VARCHAR(150) NOT NULL,
    Direccion     VARCHAR(100) NOT NULL
);

-- ============================================
-- PEDIDO
-- ============================================
CREATE TABLE Pedido (
    Codigo_Compra   VARCHAR(10) PRIMARY KEY,
    Precio          REAL NOT NULL,
    Fecha_Compra    DATE NOT NULL,
    NIF_cliente     VARCHAR(9) NOT NULL,

    CONSTRAINT fk_Pedido_Cliente
        FOREIGN KEY (NIF_Cliente)
        REFERENCES Cliente(NIF)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

-- ============================================
-- CAJA LLENA
-- ============================================
CREATE TABLE Caja_llena (
    ID_lote        VARCHAR(10) PRIMARY KEY,
    Tamano         REAL NOT NULL,
    Tipo           CHAR(12) NOT NULL,
    Codigo_Compra  VARCHAR(10) NOT NULL,

    CONSTRAINT ck_Tipo
        CHECK (Tipo IN ('roto', 'defectuoso', 'bueno')),

    CONSTRAINT fk_Caja_Pedido
        FOREIGN KEY (Codigo_Compra)
        REFERENCES Pedido(Codigo_Compra)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

-- ============================================
-- AZULEJO
-- ============================================
CREATE TABLE Azulejo (
    N_serie   VARCHAR(10) PRIMARY KEY,
    Estado    CHAR(12) NOT NULL,
    ID_lote   VARCHAR(10) NOT NULL,

    CONSTRAINT ck_Estado
        CHECK (Estado IN ('roto', 'defectuoso', 'bueno')),

    CONSTRAINT fk_Azulejo_Caja
        FOREIGN KEY (ID_lote)
        REFERENCES Caja_llena(ID_lote)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

-- ============================================
-- PROVEEDOR
-- ============================================
CREATE TABLE Proveedor (
    NIF        VARCHAR(10) PRIMARY KEY,
    Telefono   VARCHAR(15) NOT NULL,
    Direccion  VARCHAR(100) NOT NULL,
    Correo     VARCHAR(150) NOT NULL
);

-- ============================================
-- CAJA VACIA
-- ============================================
CREATE TABLE Caja_Vacia (
    N_lote   VARCHAR(10) PRIMARY KEY,
    Tamano   INT NOT NULL
);

-- ============================================
-- COMPRA
-- ============================================
CREATE TABLE Compra (
    NIF_proveedor   VARCHAR(10) NOT NULL,
    N_lote          VARCHAR(10) NOT NULL,
    Fecha_Compra    DATE NOT NULL,
    Precio_Final    REAL NOT NULL,

    CONSTRAINT pk_Compra
        PRIMARY KEY (NIF_Proveedor, N_lote, Fecha_Compra),

    CONSTRAINT fk_Compra_Proveedor
        FOREIGN KEY (NIF_Proveedor)
        REFERENCES Proveedor(NIF)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_Compra_Caja
        FOREIGN KEY (N_lote)
        REFERENCES Caja_vacia(N_lote)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

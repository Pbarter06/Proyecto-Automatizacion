CREATE SCHEMA azulejos;
SET search_path TO azulejos;

-- ============================================
-- CLIENTE
-- ============================================
CREATE TABLE cliente (
    nif           VARCHAR(9) PRIMARY KEY,
    telefono      VARCHAR(15) NOT NULL,
    correo        VARCHAR(150) NOT NULL,
    direccion     VARCHAR(100) NOT NULL
);

-- ============================================
-- PEDIDO
-- ============================================
CREATE TABLE pedido (
    codigo_compra   VARCHAR(10) PRIMARY KEY,
    precio          REAL NOT NULL,
    fecha_compra    DATE NOT NULL,
    nif_cliente     VARCHAR(9) NOT NULL,

    CONSTRAINT fk_pedido_cliente
        FOREIGN KEY (nif_cliente)
        REFERENCES cliente(nif)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

-- ============================================
-- CAJA LLENA
-- ============================================
CREATE TABLE caja_llena (
    id_lote        VARCHAR(10) PRIMARY KEY,
    tamano         REAL NOT NULL,
    tipo           CHAR(12) NOT NULL,
    codigo_compra  VARCHAR(10) NOT NULL,

    CONSTRAINT ck_tipo
        CHECK (tipo IN ('roto', 'defectuoso', 'bueno')),

    CONSTRAINT fk_caja_pedido
        FOREIGN KEY (codigo_compra)
        REFERENCES pedido(codigo_compra)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

-- ============================================
-- AZULEJOS
-- ============================================
CREATE TABLE azulejo (
    n_serie   VARCHAR(10) PRIMARY KEY,
    estado    CHAR(12) NOT NULL,
    id_lote   VARCHAR(10) NOT NULL,

    CONSTRAINT ck_estado
        CHECK (estado IN ('roto', 'defectuoso', 'bueno')),

    CONSTRAINT fk_azulejo_caja
        FOREIGN KEY (id_lote)
        REFERENCES caja_llena(id_lote)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

-- ============================================
-- PROVEEDOR
-- ============================================
CREATE TABLE proveedores (
    nif        VARCHAR(10) PRIMARY KEY,
    telefono   VARCHAR(15) NOT NULL,
    direccion  VARCHAR(100) NOT NULL,
    correo     VARCHAR(150) NOT NULL
);

-- ============================================
-- CAJA VACIA
-- ============================================
CREATE TABLE caja_vacia (
    n_lote   VARCHAR(10) PRIMARY KEY,
    tamano   INT NOT NULL
);

-- ============================================
-- COMPRA
-- ============================================
CREATE TABLE compra (
    nif_proveedor   VARCHAR(10) NOT NULL,
    n_lote          VARCHAR(10) NOT NULL,
    fecha_compra    DATE NOT NULL,
    precio_final    REAL NOT NULL,

    CONSTRAINT pk_compra
        PRIMARY KEY (nif_proveedor, n_lote, fecha_compra),

    CONSTRAINT fk_compra_proveedor
        FOREIGN KEY (nif_proveedor)
        REFERENCES proveedor(nif)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_compra_caja
        FOREIGN KEY (n_lote)
        REFERENCES caja_vacia(n_lote)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

SET search_path TO azulejos;

-- ============================================
-- 1. PROVEEDORES
-- ============================================
INSERT INTO proveedores (nif, telefono, direccion, correo)
VALUES
('A11111111', '961000001', 'Pol. Ind. El Palleter, Valencia', 'ventas@porcelanas-levante.com'),
('B22222222', '964000002', 'Camino del Barro 45, Castellón', 'pedidos@azulejos-castellon.es'),
('C33333333', '910000003', 'Av. de la Cerámica 12, Madrid', 'contacto@suministros-global.com'),
('D44444444', '933000004', 'Carrer de la Terrissa 8, Barcelona', 'info@tiles-bcn.cat'),
('E55555555', '954000005', 'Pol. Ind. Navas, Sevilla', 'andalucia.dist@ceramica.es'),
('F66666666', '981000006', 'Rúa do Torno, A Coruña', 'galicia.tiles@export.es'),
('G77777777', '964111222', 'Pol. Ind. Mijares, Onda', 'logistica@onda-ceramics.com'),
('H88888888', '912333444', 'Calle de los Artesanos 5, Talavera', 'pedidos@talavera-arte.es'),
('I99999999', '935666777', 'Av. Diagonal 400, Barcelona', 'premium@luxe-tiles.com');

-- ============================================
-- 2. CAJAS VACÍAS
-- ============================================
INSERT INTO cajas_vacias (n_lote, tamano)
VALUES
('V-PEQ', 10), ('V-MED', 25), ('V-GRA', 50), ('V-IND', 100),
('V-XTRA', 200), ('V-MUESTR', 5), ('V-ZOC', 15);

-- ============================================
-- 3. COMPRAS (Historial ampliado)
-- ============================================
INSERT INTO compra (nif_proveedor, n_lote, fecha_compra, precio_final)
VALUES
('A11111111', 'V-GRA', '2024-11-10', 500.00), 
('B22222222', 'V-MED', '2024-11-15', 250.00),
('C33333333', 'V-PEQ', '2024-12-01', 100.00), 
('D44444444', 'V-IND', '2024-12-20', 1200.00),
('E55555555', 'V-GRA', '2025-01-05', 550.00), 
('F66666666', 'V-MED', '2025-01-15', 280.00),
('A11111111', 'V-IND', '2025-02-01', 1150.00), 
('B22222222', 'V-PEQ', '2025-02-10', 110.00),
('C33333333', 'V-MED', '2025-03-01', 260.00), 
('D44444444', 'V-GRA', '2025-03-15', 520.00),
('G77777777', 'V-IND', '2025-04-05', 1300.00),
('H88888888', 'V-PEQ', '2025-04-12', 125.50),
('I99999999', 'V-GRA', '2025-04-20', 600.00);

-- ============================================
-- 4. CLIENTES
-- ============================================
INSERT INTO clientes (nif, telefono, correo, direccion)
VALUES
('10101010A', '600000001', 'reformas.juan@gmail.com', 'Calle Mayor 1, Valencia'),
('20202020B', '600000002', 'ana.garcia@outlook.com', 'Av. del Puerto 45, Gandia'),
('30303030C', '600000003', 'proyectos.ruiz@sl.es', 'Calle Colón 10, Alicante'),
('40404040D', '600000004', 'pablo.obras@gmail.com', 'Plaza España 5, Castellón'),
('50505050E', '600000005', 'marta.design@interior.es', 'Gran Vía 12, Madrid'),
('60606060F', '600000006', 'hotel.med@costa.com', 'Paseo Marítimo 10, Benidorm'),
('70707070G', '600000007', 'estudio.luz@arquitectura.es', 'Calle Real 4, Toledo'),
('80808080H', '611222333', 'compras@promociones-levante.sl', 'Av. de Francia 20, Valencia'),
('90909090I', '644555666', 'carlos.martinez@gmail.com', 'Calle Mayor 5, Sagunto'),
('01010101J', '677888999', 'info@deco-interiores.es', 'Paseo de Gracia 88, Barcelona');

-- ============================================
-- 5. PEDIDOS
-- ============================================
INSERT INTO pedido (codigo_compra, precio, fecha_compra, nif_cliente)
VALUES
('P25-001', 1500.00, '2025-01-10', '60606060F'), 
('P25-002', 320.50,  '2025-01-12', '10101010A'),
('P25-003', 95.00,   '2025-01-15', '20202020B'), 
('P25-004', 2100.00, '2025-01-20', '30303030C'),
('P25-005', 450.75,  '2025-01-25', '10101010A'), 
('P25-006', 120.00,  '2025-02-05', '40404040D'),
('P25-007', 890.00,  '2025-02-10', '50505050E'), 
('P25-008', 3500.00, '2025-02-15', '60606060F'),
('P25-009', 150.25,  '2025-02-20', '70707070G'), 
('P25-010', 440.00,  '2025-03-01', '10101010A'),
('P25-011', 2800.00, '2025-04-05', '80808080H'),
('P25-012', 120.00,  '2025-04-18', '90909090I'),
('P25-013', 950.40,  '2025-04-25', '01010101J');

-- ============================================
-- 6. CAJAS LLENAS
-- ============================================
INSERT INTO cajas_llenas (id_lote, tamano, tipo, codigo_compra)
VALUES
('L-001', 100, 'bueno', 'P25-001'), ('L-002', 100, 'bueno', 'P25-001'),
('L-003', 25, 'bueno', 'P25-002'), ('L-004', 10, 'defectuoso', 'P25-003'),
('L-005', 50, 'bueno', 'P25-004'), ('L-006', 50, 'bueno', 'P25-004'),
('L-007', 25, 'bueno', 'P25-005'), ('L-008', 25, 'roto', 'P25-005'),
('L-009', 10, 'bueno', 'P25-006'), ('L-010', 50, 'bueno', 'P25-007'),
('L-011', 100, 'bueno', 'P25-008'), ('L-012', 100, 'bueno', 'P25-008'),
('L-013', 10, 'bueno', 'P25-009'), ('L-014', 25, 'bueno', 'P25-010'),
('L-015', 100, 'bueno', 'P25-011'), ('L-016', 10, 'bueno', 'P25-012'),
('L-017', 50, 'defectuoso', 'P25-013');

-- ============================================
-- 7. AZULEJOS
-- ============================================
INSERT INTO azulejos (n_serie, estado, id_lote)
VALUES
-- Lote L-001
('S1-001', 'bueno', 'L-001'), ('S1-002', 'bueno', 'L-001'), ('S1-003', 'bueno', 'L-001'), ('S1-004', 'bueno', 'L-001'), ('S1-005', 'bueno', 'L-001'),
-- Lote L-003
('S3-001', 'bueno', 'L-003'), ('S3-002', 'bueno', 'L-003'), ('S3-003', 'bueno', 'L-003'), ('S3-004', 'bueno', 'L-003'), ('S3-005', 'bueno', 'L-003'),
-- Lote L-004 (Defectuosos)
('S4-001', 'defectuoso', 'L-004'), ('S4-002', 'defectuoso', 'L-004'), ('S4-003', 'defectuoso', 'L-004'), ('S4-004', 'defectuoso', 'L-004'), ('S4-005', 'defectuoso', 'L-004'),
-- Lote L-008 (Rotos)
('S8-001', 'roto', 'L-008'), ('S8-002', 'roto', 'L-008'), ('S8-003', 'roto', 'L-008'), ('S8-004', 'roto', 'L-008'), ('S8-005', 'roto', 'L-008'),
-- Lote L-011
('S11-01', 'bueno', 'L-011'), ('S11-02', 'bueno', 'L-011'), ('S11-03', 'bueno', 'L-011'), ('S11-04', 'bueno', 'L-011'), ('S11-05', 'bueno', 'L-011'),
-- Lote L-014
('S14-01', 'bueno', 'L-014'), ('S14-02', 'bueno', 'L-014'), ('S14-03', 'bueno', 'L-014'), ('S14-04', 'bueno', 'L-014'), ('S14-05', 'bueno', 'L-014'),
-- Lote L-015 (Ampliación)
('S15-01', 'bueno', 'L-015'), ('S15-02', 'bueno', 'L-015'), ('S15-03', 'bueno', 'L-015'), ('S15-04', 'bueno', 'L-015'), ('S15-05', 'bueno', 'L-015'),
-- Lote L-016 (Ampliación)
('S16-01', 'bueno', 'L-016'), ('S16-02', 'bueno', 'L-016'), ('S16-03', 'bueno', 'L-016'), ('S16-04', 'bueno', 'L-016'), ('S16-05', 'bueno', 'L-016'),
-- Lote L-017 (Ampliación Defectuosos)
('S17-01', 'defectuoso', 'L-017'), ('S17-02', 'defectuoso', 'L-017'), ('S17-03', 'defectuoso', 'L-017'), ('S17-04', 'defectuoso', 'L-017'), ('S17-05', 'defectuoso', 'L-017');

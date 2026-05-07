
import psycopg 

conn = psycopg.connect(
    dbname = "proyecto",
    user = "postgres",
    password = "GDI.2026",
    host = "localhost",
    port = "5432"
)
print("Conexión exitosa a la base de datos")

cur = conn.cursor()

serie_inicial = 1
total_azulejos_a_insertar = 100

# Serie: S1-001, S1-002, ... S1-999, S2-001, ...
# Lote: L-001, L-002, ... (cada lote agrupa 10 azulejos)


def formatear_serie(numero_serie):
    bloque_serie = ((numero_serie - 1) // 999) + 1
    numero_en_bloque = ((numero_serie - 1) % 999) + 1
    return f"S{bloque_serie}-{numero_en_bloque:03d}"


for i in range(total_azulejos_a_insertar):
    numero_serie = serie_inicial + i
    serie = formatear_serie(numero_serie)
    numero_lote = ((numero_serie - 1) // 10) + 1
    lote = f"L-{numero_lote:03d}"

    # AZULEJO
    sql = """INSERT INTO Azulejo (N_serie, Estado, ID_lote)
    VALUES (%s, %s, %s)"""
    datos = (serie, 'bueno', lote)
    cur.execute(sql, datos)

    # CAJA LLENA (se registra cuando se completa cada bloque de 10 azulejos)
    if numero_serie % 10 == 0:
        sql = """INSERT INTO Caja_llena (ID_lote, Tamano, Tipo, Codigo_Compra)
        VALUES (%s, %s, %s, %s)"""
        datos = (lote, 10, 'bueno', f"P25-{numero_lote:03d}")
        cur.execute(sql, datos)

conn.commit()


cur.close()
conn.close()

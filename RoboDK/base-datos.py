
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

# AZULEJO

sql = """INSERT INTO Azulejo (N_serie, Estado, ID_lote)
VALUES (%s, %s, %s)"""
datos = ('S1-001', 'bueno', 'L-001')
cur.execute(sql, datos)
conn.commit()


# CAJA LLENA 

sql = """INSERT INTO Caja_llena (ID_lote, Tamano, Tipo, Codigo_Compra)
VALUES (%s, %s, %s, %s)"""
datos = ('L1-001', 100, 'bueno', 'P25-001')
cur.execute(sql, datos)
conn.commit()
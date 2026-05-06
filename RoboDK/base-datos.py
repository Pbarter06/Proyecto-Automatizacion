
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
datos = ('S1-001', 'Bueno', 'L-001')
cur.execute(sql, datos)
conn.commit()


# CAJA LLENA 

import time
from robodk import robolink    # RoboDK API
import psycopg

RDK = robolink.Robolink()

caja = RDK.Item('cajaA1')
fotocelula = RDK.Item('Fotocelula1')
frame = RDK.Item('CintaCaja1')
cinta = RDK.Item('Cajas1')
INCREMENTO_MM=406

while(True):
    lista_caja = frame.Childs()
    detectado = False

    while not detectado:
        cinta.MoveJ(cinta.Joints()+INCREMENTO_MM)
        for caja in lista_caja:
            if caja.Name():       
                if fotocelula.Collision(caja):
                    detectado = True
                    RDK.setParam('SenyalSensor1', 1)
                    break 


    while detectado:
        done = RDK.getParam('Done1')
        if done == 1:
            detectado = False
        time.sleep(0.1)

    conn = psycopg.connect(
            dbname = "Azulejos",
            user = "postgres",
            password = "8130",
            host = "localhost",
            port = "5432"
    )
    cur = conn.cursor()

    lote1 = int(RDK.getParam('Lote1'))
    lote2 = int(RDK.getParam('Lote2'))
    if lote1 == 0 and lote2 == 0:
        lote2 = 1
    elif lote1 > lote2:
        lote2 = lote1 + 1
    else:
        lote2 = lote2 + 1
    lote = f"L-{lote2:03d}"
        
    sql = """INSERT INTO azulejos.Caja_llena (ID_lote, Tamano, Tipo, Codigo_Compra)
    VALUES (%s, %s, %s, %s)"""
    datos = (lote, 10, 'bueno', f"P25-{lote2:03d}")
    cur.execute(sql, datos)
    conn.commit()
        
    RDK.setParam('Lote2', lote2)
    cur.close()
    conn.close()

    cinta.MoveJ(cinta.Joints()+INCREMENTO_MM)
    RDK.setParam('SenyalSensor1', 0)
    lista_caja = frame.Childs()

    for item in lista_caja:
        if item.Name().startswith('Azulejo'):
            item.Delete()

    RDK.setParam('Done1', 0)
    cinta.setJoints([0])

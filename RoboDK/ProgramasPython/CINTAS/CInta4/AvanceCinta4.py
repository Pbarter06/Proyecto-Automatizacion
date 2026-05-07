import time
from robodk import robolink    # RoboDK API
from robodk import robomath
import psycopg 

RDK = robolink.Robolink()

caja = RDK.Item('cajaC')
fotocelula = RDK.Item('Fotocelula4')
frame = RDK.Item('CintaCaja4')
cinta = RDK.Item('Cajas4')
INCREMENTO_MM=406

def spawnear_caja():

    template = RDK.Item('cajaBase')
    
    if not template.Valid():
        print("Error: No encuentro el template")
        return None

    template.Copy() 
    nueva_caja = RDK.Paste(frame) 
    nueva_caja.setName("cajaC") 
    nueva_caja.setVisible(True)
    nueva_caja.setPose(robomath.eye(4)) 
    
    return nueva_caja

while(True):
    lista_caja = frame.Childs()
    detectado = False
    Done = RDK.getParam('Done1')

    if Done == 1:
        conn = psycopg.connect(
            dbname = "proyecto",
            user = "postgres",
            password = "GDI.2026",
            host = "localhost",
            port = "5432"
        )
        cur = conn.cursor()
        time.sleep(1)
        while not detectado:
            cinta.MoveJ(cinta.Joints()+INCREMENTO_MM)
            for caja in lista_caja:
                if caja.Name().startswith("cajaC"):        
                    if fotocelula.Collision(caja):
                        detectado = True
                        RDK.setParam('SenyalSensor4', 1)
                        break 

        while detectado:
            for caja in lista_caja:
                if caja.Name().startswith("cajaC"):        
                    if not fotocelula.Collision(caja):
                        detectado = False
                        RDK.setParam('SenyalSensor4', 0)
                        break
            time.sleep(0.1)

        cinta.setJoints([0])
        caja = spawnear_caja()

        lote2 = RDK.getParam('Lote2')
        lote = f"L-{lote2:03d}"
        
        sql = """INSERT INTO Caja_llena (ID_lote, Tamano, Tipo, Codigo_Compra)
        VALUES (%s, %s, %s, %s)"""
        datos = (lote, 10, 'bueno', f"P25-{lote2:03d}")
        cur.execute(sql, datos)
        conn.commit()
        
        lote2 = lote2 + 1
        RDK.setParam('Lote2', lote2)
        cur.close()
        conn.close()

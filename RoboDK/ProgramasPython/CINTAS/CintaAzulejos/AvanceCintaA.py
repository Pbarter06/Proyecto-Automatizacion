import time
from robodk import robolink    # RoboDK API
from robodk import robomath
import psycopg 

conn = psycopg.connect(
    dbname = "proyecto",
    user = "postgres",
    password = "GDI.2026",
    host = "localhost",
    port = "5432"
)
cur = conn.cursor()

RDK = robolink.Robolink()

azulejo = RDK.Item('Azulejo')
fotocelula = RDK.Item('FotocelulaA')
frame = RDK.Item('CintaAzulejos')
cinta = RDK.Item('AzulejoAn')
INCREMENTO_MM = 1680 
INCREMENTO_B = 350
lista_azulejos = frame.Childs()
tipo = RDK.getParam('TipoAzulejo')

def spawnear_azulejo():

    template = RDK.Item('AzulejoBase')
    
    if not template.Valid():
        print("Error: No encuentro el template")
        return None

    template.Copy() 
    nuevo_azulejo = RDK.Paste(frame) 
    nuevo_azulejo.setName("Azulejo") 
    nuevo_azulejo.setVisible(True)
    nuevo_azulejo.setPose(robomath.eye(4)) 
    
    return nuevo_azulejo

def formatear_serie(numero_serie):
    bloque_serie = ((numero_serie - 1) // 999) + 1
    numero_en_bloque = ((numero_serie - 1) % 999) + 1
    return f"S{bloque_serie}-{numero_en_bloque:03d}"

serie_inicial = int(RDK.getParam('SerieInicial'))
total_azulejos_a_insertar = int(RDK.getParam('TotalAzulejos'))

for i in range(total_azulejos_a_insertar):
    lista_azulejos = frame.Childs()
    detectado = False

    while not detectado:
        cinta.MoveJ(cinta.Joints()+INCREMENTO_MM)
        for azulejo in lista_azulejos:
            if azulejo.Name().startswith("Azulejo"):        
                if fotocelula.Collision(azulejo):
                    detectado = True
                    RDK.setParam('SenyalSensorA', 1)
                    break 
    
    while detectado:
        tipo = RDK.getParam('TipoAzulejo')
        if tipo == 3:
            cinta.MoveJ(cinta.Joints() + INCREMENTO_B)
            for item in lista_azulejos:
                # 1. Comprobamos si el item es válido ANTES de preguntarle su nombre
                if item.Valid() and item.Name().startswith('Azulejo'):
                    item.Delete()
                    # 2. Lo borramos también de la lista de Python para no dejar "fantasmas"
                    lista_azulejos.remove(item)
                    break
            detectado = False
        for azulejo in lista_azulejos:
            if azulejo.Name().startswith("Azulejo"):        
                if not fotocelula.Collision(azulejo):
                    detectado = False
                    RDK.setParam('SenyalSensorA', 0)
                    break

        time.sleep(0.1)

    cinta.setJoints([0])
    azulejo = spawnear_azulejo()

    tipo = RDK.getParam('TipoAzulejos')
    lote1 = RDK.getParam('Lote1')
    lote2 = RDK.getParam('Lote2')


    if tipo == 1:
        estado = 'bueno'
        lote_aux = lote1
    elif tipo == 2:
        estado = 'defectuoso'
        lote_aux = lote2
    elif tipo == 3:
        estado = 'roto'
        lote_aux = -1

        
    #GDI

    numero_serie = serie_inicial + i
    serie = formatear_serie(numero_serie)
    lote = f"L-{lote_aux:03d}"

    sql = """INSERT INTO Azulejo (N_serie, Estado, ID_lote)
    VALUES (%s, %s, %s)"""
    datos = (serie, estado, lote)
    cur.execute(sql, datos)
    conn.commit()


cur.close()
conn.close()

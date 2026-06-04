# Type help("robodk.robolink") or help("robodk.robomath") for more information
# Press F5 to run the script
# Documentation: https://robodk.com/doc/en/RoboDK-API.html
# Reference:     https://robodk.com/doc/en/PythonAPI/robodk.html
# Note: It is not required to keep a copy of this file, your Python script is saved with your RDK project
import time
from robodk import robolink    # RoboDK API
from robodk import robomath    # Robot toolbox
import psycopg

RDK = robolink.Robolink()

conn = psycopg.connect(
    dbname = "Azulejos",
    user = "postgres",
    password = "8130",
    host = "localhost",
    port = "5432"
)
cur = conn.cursor()

#TIPO 3

INCREMENTO_B = 350
cinta = RDK.Item('AzulejoAn')
frame = RDK.Item('CintaAzulejos')
lista_azulejos = frame.Childs()

#ROBOT
robot = RDK.Item('UR5e', robolink.ITEM_TYPE_ROBOT)

#TARGETS
target_PPaso = RDK.Item('PuntoPaso1', robolink.ITEM_TYPE_TARGET)
target_Pick = RDK.Item('Pick', robolink.ITEM_TYPE_TARGET)
target_PrePick = RDK.Item('PrePick', robolink.ITEM_TYPE_TARGET)
target_Place1 = RDK.Item('Place1', robolink.ITEM_TYPE_TARGET)
target_Place2 = RDK.Item('Place2', robolink.ITEM_TYPE_TARGET)
target_PostPlace1 = RDK.Item('PostPlace1', robolink.ITEM_TYPE_TARGET)
target_PostPlace2 = RDK.Item('PostPlace2', robolink.ITEM_TYPE_TARGET)

#OBJETOS
azulejo = RDK.Item('Azulejo', robolink.ITEM_TYPE_OBJECT)

#HERRAMIENTA
ventosa = RDK.Item('SMC ZXP7A01-ZP20U-X1 Vacuum Gripper', robolink.ITEM_TYPE_TOOL)

#FRAMES
general = RDK.Item('general', robolink.ITEM_TYPE_FRAME)
frameCintaA = RDK.Item('Azulejos', robolink.ITEM_TYPE_FRAME)
frameAzulejo = RDK.Item('CintaAzulejos', robolink.ITEM_TYPE_FRAME)
frameCinta1 = RDK.Item('Cinta1', robolink.ITEM_TYPE_FRAME)
frameCinta2 = RDK.Item('Cinta2', robolink.ITEM_TYPE_FRAME)
frameCaja1 = RDK.Item('CintaCaja1', robolink.ITEM_TYPE_FRAME)
frameCaja2 = RDK.Item('CintaCaja2', robolink.ITEM_TYPE_FRAME)

target_PPaso.setParent(general)
target_Pick.setParent(frameCintaA)
target_PrePick.setParent(frameCintaA)
target_Place1.setParent(frameCinta1)
target_Place2.setParent(frameCinta2)
target_PostPlace1.setParent(frameCinta1)
target_PostPlace2.setParent(frameCinta2)

def formatear_serie(numero_serie):
    bloque_serie = ((numero_serie - 1) // 999) + 1
    numero_en_bloque = ((numero_serie - 1) % 999) + 1
    return f"S{bloque_serie}-{numero_en_bloque:03d}"

# --- CÓDIGO PRINCIPAL ---

while(True):
    cola_raw = RDK.getParam('ColaAzulejos')
    
    if isinstance(cola_raw, (float, int)):
        cola_actual = str(int(cola_raw))
    elif cola_raw:
        cola_actual = str(cola_raw)
    else:
        cola_actual = ""
    
    try:
        SensorA = int(RDK.getParam('SenyalSensorA'))
    except:
        SensorA = 0

    if SensorA == 1 and cola_actual:
        
        lista_ordenes = cola_actual.split(',')
        
        try:
            tipo_actual = int(lista_ordenes[0])
        except ValueError:
            tipo_actual = 0 
            
        if lista_ordenes[1:] == []:
            RDK.setParam('ColaAzulejos',1)
        else:
            elementos_restantes = lista_ordenes[1:]
            RDK.setParam('ColaAzulejos', ",".join(elementos_restantes))

        #GDI
        
        lote1 = int(RDK.getParam('Lote1'))
        lote2 = int(RDK.getParam('Lote2'))
        lote_aux = 0
        estado = 0

        if tipo_actual == 1:
            estado = 'bueno'
            lote_aux = lote2
        elif tipo_actual == 2:
            estado = 'defectuoso'
            lote_aux = lote1
        elif tipo_actual == 3:
            estado = 'roto'
            lote = 'Basura'

        ID = int(RDK.getParam('IDAzulejo'))
        
        numero_serie = ID + 1
        serie = formatear_serie(numero_serie)
        if tipo_actual == 1 or tipo_actual == 2:
            lote = f"L-{lote_aux:03d}"

        sql = """INSERT INTO azulejos.Azulejo (N_serie, Estado, ID_lote)
        VALUES (%s, %s, %s)"""
        datos = (serie, estado, lote)
        cur.execute(sql, datos)
        conn.commit()
        RDK.setParam('IDAzulejo', numero_serie)

        if tipo_actual != 3:

            # PICK
            robot.setPoseFrame(general)
            robot.setSpeed(500,100)
            robot.MoveJ(target_PPaso.Pose())

            robot.setPoseFrame(frameCintaA)
            robot.MoveJ(target_PrePick.Pose())
            robot.MoveL(target_Pick.Pose())

            azulejos_disponibles = frameAzulejo.Childs()

            if len(azulejos_disponibles) > 0:
                azulejo_actual = azulejos_disponibles[0]
                azulejo_actual.setParentStatic(ventosa)
            
            robot.MoveL(target_PrePick.Pose())

            match tipo_actual:
                
                case 1:
                    time.sleep(1)
                    while int(RDK.getParam('SenyalSensor1')) != 1:
                        time.sleep(0.1)

                    robot.setPoseFrame(general)
                    robot.setSpeed(500,100)
                    robot.MoveJ(target_PPaso.Pose())

                    try:
                        x1 = int(RDK.getParam('x1'))
                        z1 = int(RDK.getParam('z1'))
                    except:
                        x1, z1 = 0, 0

                    desplazamiento1 = robomath.transl(x1*-137, 0, z1*-10)
                    pose_place1 = target_Place1.Pose() * desplazamiento1

                    # Place1
                    robot.setPoseFrame(frameCinta1)
                    robot.MoveL(pose_place1 * robomath.transl([0,0,-120]))
                    robot.setSpeed(50,20)
                    robot.MoveL(pose_place1)
                    time.sleep(1)
                    azulejo_actual.setParentStatic(frameCaja1)

                    robot.setPoseFrame(frameCinta1)
                    robot.setSpeed(500,100)
                    robot.MoveL(target_PostPlace1.Pose())

                    robot.setPoseFrame(general)
                    robot.setSpeed(500,100)
                    robot.MoveJ(target_PPaso.Pose())        

                    if x1 < 2:
                        x1 = x1 + 1
                    if x1 == 2:
                        z1 = z1 + 1
                        x1 = 0
                    if z1 == 5:
                        x1 = 0
                        z1 = 0
                        RDK.setParam('Done1', 1)
                        time.sleep(2)                  

                    RDK.setParam('x1', str(x1)) 
                    RDK.setParam('z1', str(z1))
                
                case 2:
                    time.sleep(1)
                    while int(RDK.getParam('SenyalSensor2')) != 1:
                        time.sleep(0.1)
                
                    robot.setPoseFrame(general)
                    robot.setSpeed(500,100)
                    robot.MoveJ(target_PPaso.Pose())

                    try:
                        x2 = int(RDK.getParam('x2'))
                        z2 = int(RDK.getParam('z2'))
                    except:
                        x2, z2 = 0, 0

                    desplazamiento2 = robomath.transl(x2*-137, 0, z2*-10)
                    pose_place2 = target_Place2.Pose() * desplazamiento2

                    # Place2
                    robot.setPoseFrame(frameCinta2)
                    robot.MoveL(pose_place2 * robomath.transl([0,0,-120]))
                    robot.setSpeed(50,20)
                    robot.MoveL(pose_place2)
                    time.sleep(1)
                    azulejo_actual.setParentStatic(frameCaja2)

                    robot.setPoseFrame(frameCinta2)
                    robot.setSpeed(500,100)
                    robot.MoveL(target_PostPlace2.Pose())

                    robot.setPoseFrame(general)
                    robot.setSpeed(500,100)
                    robot.MoveJ(target_PPaso.Pose())        

                    if x2 < 2:
                        x2 = x2 + 1
                    if x2 == 2:
                        z2 = z2 + 1
                        x2 = 0
                    if z2 == 5:
                        x2 = 0
                        z2 = 0
                        RDK.setParam('Done2', 1)

                    RDK.setParam('x2', str(x2))
                    RDK.setParam('z2', str(z2))
        elif tipo_actual == 3:
            cinta.MoveJ(cinta.Joints() + INCREMENTO_B)
            for item in lista_azulejos:
                if item.Valid() and item.Name().startswith('Azulejo'):
                    item.Delete()
                    lista_azulejos.remove(item)
                    break

    else:
        time.sleep(0.1)

cur.close()
conn.close()

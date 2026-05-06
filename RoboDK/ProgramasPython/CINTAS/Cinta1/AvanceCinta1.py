import time
from robodk import robolink    # RoboDK API
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

    cinta.MoveJ(cinta.Joints()+INCREMENTO_MM)
    RDK.setParam('SenyalSensor1', 0)
    lista_caja = frame.Childs()

    for item in lista_caja:
        if item.Name().startswith('Azulejo'):
            item.Delete()

    RDK.setParam('Done1', 0)
    cinta.setJoints([0])

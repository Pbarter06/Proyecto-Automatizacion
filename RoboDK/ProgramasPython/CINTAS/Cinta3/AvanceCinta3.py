import time
from robodk import robolink    # RoboDK API
from robodk import robomath
RDK = robolink.Robolink()

caja = RDK.Item('cajaC')
fotocelula = RDK.Item('Fotocelula3')
frame = RDK.Item('CintaCaja3')
cinta = RDK.Item('Cajas3')
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
    Done = RDK.getParam('Done2')

    if Done == 1:
        time.sleep(1)
        while not detectado:
            cinta.MoveJ(cinta.Joints()+INCREMENTO_MM)
            for caja in lista_caja:
                if caja.Name().startswith("cajaC"):        
                    if fotocelula.Collision(caja):
                        detectado = True
                        RDK.setParam('SenyalSensor3', 1)
                        break 

        while detectado:
            for caja in lista_caja:
                if caja.Name().startswith("cajaC"):        
                    if not fotocelula.Collision(caja):
                        detectado = False
                        RDK.setParam('SenyalSensor3', 0)
                        break
            time.sleep(0.1)

        cinta.setJoints([0])
        caja = spawnear_caja()

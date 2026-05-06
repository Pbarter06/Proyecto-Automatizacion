import time
from robodk import robolink    # RoboDK API
from robodk import robomath
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

while(True):
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

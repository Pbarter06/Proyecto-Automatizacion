import time
from robodk import robolink    # RoboDK API
RDK = robolink.Robolink()


frame1 = RDK.Item('CintaCaja1')
frame2 = RDK.Item('CintaCaja2')
frame3 = RDK.Item('SMC ZXP7A01-ZP20U-X1 Vacuum Gripper')
lista_caja1 = frame1.Childs()
lista_caja2 = frame2.Childs()
lista_caja3 = frame3.Childs()

for item in lista_caja1:
    if item.Name().startswith('Azulejo'):
        item.Delete()

for item in lista_caja2:
    if item.Name().startswith('Azulejo'):
        item.Delete()

for item in lista_caja3:
    if item.Name().startswith('Azulejo'):
        item.Delete()

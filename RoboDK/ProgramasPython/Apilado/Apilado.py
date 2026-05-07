# Type help("robodk.robolink") or help("robodk.robomath") for more information
# Press F5 to run the script
# Documentation: https://robodk.com/doc/en/RoboDK-API.html
# Reference:     https://robodk.com/doc/en/PythonAPI/robodk.html
# Note: It is not required to keep a copy of this file, your Python script is saved with your RDK project

# You can also use the new version of the API:
import time
from robodk import robolink    # RoboDK API
from robodk import robomath    # Robot toolbox
RDK = robolink.Robolink()

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
frameCinta1 = RDK.Item('CintaCaja1', robolink.ITEM_TYPE_FRAME)
frameCinta2 = RDK.Item('CintaCaja2', robolink.ITEM_TYPE_FRAME)
frameCaja1 = RDK.Item('CintaCaja1', robolink.ITEM_TYPE_FRAME)
frameCaja2 = RDK.Item('CintaCaja2', robolink.ITEM_TYPE_FRAME)

#target_Reposo.setParent(general)
target_PPaso.setParent(general)
target_Pick.setParent(frameCintaA)
target_PrePick.setParent(frameCintaA)
target_Place1.setParent(frameCinta1)
target_Place2.setParent(frameCinta2)
target_PostPlace1.setParent(frameCaja1)
target_PostPlace2.setParent(frameCaja2)

#CÓDIGO

while(True):

    while int(RDK.getParam('SenyalSensorA')) != 1:
        time.sleep(0.1)
    
    SensorA = RDK.getParam('SenyalSensorA')
    Tipo = RDK.getParam('TipoAzulejo')

    if SensorA == 1 and Tipo != 3:

        #PICK
        
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

        Tipo = RDK.getParam('TipoAzulejo')

        match Tipo:
            
            case 1:
                
                while int(RDK.getParam('SenyalSensor1')) != 1:
                    time.sleep(0.1)

                robot.setPoseFrame(general)
                robot.setSpeed(500,100)
                robot.MoveJ(target_PPaso.Pose())

                x1 = RDK.getParam('x1')
                z1 = RDK.getParam('z1')

                desplazamiento1 = robomath.transl(x1*-137, 0, z1*-10)

                pose_place1 = target_Place1.Pose() * desplazamiento1

                #Place1

                robot.setPoseFrame(frameCinta1)
                robot.MoveL(pose_place1 * robomath.transl([0,0,-120]))
                robot.setSpeed(50,20)
                robot.MoveL(pose_place1)
                time.sleep(1)
                azulejo_actual.setParentStatic(frameCaja1)

                robot.setPoseFrame(frameCaja1)
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

                RDK.setParam('x1',x1)
                RDK.setParam('z1',z1)
                
            case 2:
                
                while int(RDK.getParam('SenyalSensor2')) != 1:
                    time.sleep(0.1)
                
                robot.setPoseFrame(general)
                robot.setSpeed(500,100)
                robot.MoveJ(target_PPaso.Pose())

                x2 = RDK.getParam('x2')
                z2 = RDK.getParam('z2')

                desplazamiento2 = robomath.transl(x2*-137, 0, z2*-10)

                pose_place2 = target_Place2.Pose() * desplazamiento2

                #Place2

                robot.setPoseFrame(frameCinta2)
                robot.MoveL(pose_place2 * robomath.transl([0,0,-120]))
                robot.setSpeed(50,20)
                robot.MoveL(pose_place2)
                time.sleep(1)
                azulejo_actual.setParentStatic(frameCaja2)

                robot.setPoseFrame(frameCaja2)
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
                 

                RDK.setParam('x2',x2)
                RDK.setParam('z2',z2)

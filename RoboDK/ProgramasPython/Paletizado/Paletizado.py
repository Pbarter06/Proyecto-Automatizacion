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

robot = RDK.Item('UR30', robolink.ITEM_TYPE_ROBOT)

#PROGRAMAS

prog1 = RDK.Item('Palet1ON')
prog2 = RDK.Item('Palet2ON')

#TARGETS

target_Reposo = RDK.Item('Reposo30', robolink.ITEM_TYPE_TARGET)
target_PPaso1 = RDK.Item('PPaso3', robolink.ITEM_TYPE_TARGET)
target_PPaso2 = RDK.Item('PPaso4', robolink.ITEM_TYPE_TARGET)
target_Pick1 = RDK.Item('Pick3', robolink.ITEM_TYPE_TARGET)
target_PrePick1 = RDK.Item('PrePick3', robolink.ITEM_TYPE_TARGET)
target_Pick2 = RDK.Item('Pick4', robolink.ITEM_TYPE_TARGET)
target_PrePick2 = RDK.Item('PrePick4', robolink.ITEM_TYPE_TARGET)
target_Place1 = RDK.Item('Place3', robolink.ITEM_TYPE_TARGET)
target_Place2 = RDK.Item('Place4', robolink.ITEM_TYPE_TARGET)

#OBJETOS

caja = RDK.Item('cajaC', robolink.ITEM_TYPE_OBJECT)

#HERRAMIENTA

ventosa = RDK.Item('OnRobot VGP20 Vacuum Gripper', robolink.ITEM_TYPE_TOOL)

#FRAMES

general = RDK.Item('general', robolink.ITEM_TYPE_FRAME)
frameCinta3 = RDK.Item('Cinta3', robolink.ITEM_TYPE_FRAME)
frameCinta4 = RDK.Item('Cinta4', robolink.ITEM_TYPE_FRAME)
frameCintaCaja3 = RDK.Item('CintaCaja3', robolink.ITEM_TYPE_FRAME)
frameCintaCaja4 = RDK.Item('CintaCaja4', robolink.ITEM_TYPE_FRAME)
framePalet1 = RDK.Item('Frame Pallet 1', robolink.ITEM_TYPE_FRAME)
framePalet2 = RDK.Item('Frame Pallet 2', robolink.ITEM_TYPE_FRAME)

target_Reposo.setParent(general)
target_PPaso1.setParent(framePalet1)
target_PPaso2.setParent(framePalet2)
target_Pick1.setParent(frameCinta3)
target_PrePick1.setParent(frameCinta3)
target_Pick2.setParent(frameCinta4)
target_PrePick2.setParent(frameCinta4)
target_Place1.setParent(framePalet1)
target_Place2.setParent(framePalet2)

#CÓDIGO

while(True):
    tipo = 0
    while int(RDK.getParam('SenyalSensor4')) != 1 and int(RDK.getParam('SenyalSensor3')) != 1:
        time.sleep(0.1)
    if int(RDK.getParam('SenyalSensor4')) == 1:
        tipo = 2
    elif int(RDK.getParam('SenyalSensor3')) == 1:
        tipo = 1
        
    match tipo:

        case 1:
            
            #PICK

            if int(RDK.getParam('LuzPalet1')) == 0:
            
                robot.setPoseFrame(general)
                robot.setSpeed(500,100)
                robot.MoveJ(target_Reposo.Pose())

                robot.setPoseFrame(frameCinta3)
                robot.MoveJ(target_PrePick1.Pose())
                robot.MoveL(target_Pick1.Pose())

                caja_disponible = frameCintaCaja3.Childs()

                if len(caja_disponible) > 0:
                    
                    caja_actual = caja_disponible[0]
                    caja_actual.setParentStatic(ventosa)
                
                robot.MoveL(target_PrePick1.Pose())

                robot.setPoseFrame(framePalet1)
                robot.setSpeed(500,100)
                robot.MoveJ(target_PPaso1.Pose())

                x3 = RDK.getParam('x3')
                y3 = RDK.getParam('y3')
                z3 = RDK.getParam('z3')
                luz1 = 0

                desplazamiento1 = robomath.transl(x3*180, y3*280, z3*-120)

                pose_place1 = target_Place1.Pose() * desplazamiento1

                #Place

                robot.MoveL(pose_place1 * robomath.transl([0,0,-120]))
                robot.setSpeed(50,20)
                robot.MoveL(pose_place1)
                time.sleep(1)
                caja_actual.setParentStatic(framePalet1)
                robot.setSpeed(500,100)
                robot.MoveL(target_PPaso1.Pose())

                if x3 < 3:
                    x3 = x3 + 1
                if x3 == 3:
                    y3 = y3 + 1
                    x3 = 0
                if y3 == 2:
                    x3 = 0
                    y3 = 0
                    z3 = z3 + 1
                if z3 == 3:
                    prog1.RunProgram()
                    luz1 = 1
                    x3 = 0
                    y3 = 0
                    z3 = 0

                RDK.setParam('x3',x3)
                RDK.setParam('y3',y3)
                RDK.setParam('z3',z3)
                RDK.setParam('LuzPalet1',luz1)

                robot.setPoseFrame(general)
                robot.setSpeed(500,100)
                robot.MoveJ(target_Reposo.Pose())

        case 2:

            #PICK

            if int(RDK.getParam('LuzPalet2')) == 0:
            
                robot.setPoseFrame(general)
                robot.setSpeed(500,100)
                robot.MoveJ(target_Reposo.Pose())

                robot.setPoseFrame(frameCinta4)
                robot.MoveJ(target_PrePick2.Pose())
                robot.MoveL(target_Pick2.Pose())

                caja_disponible = frameCintaCaja4.Childs()

                if len(caja_disponible) > 0:
                    
                    caja_actual = caja_disponible[0]
                    caja_actual.setParentStatic(ventosa)
                
                robot.MoveL(target_PrePick2.Pose())

                robot.setPoseFrame(framePalet2)
                robot.setSpeed(500,100)
                robot.MoveJ(target_PPaso2.Pose())

                x4 = RDK.getParam('x4')
                y4 = RDK.getParam('y4')
                z4 = RDK.getParam('z4')
                luz2 = 0

                desplazamiento2 = robomath.transl(x4*180, y4*280, z4*-120)

                pose_place2 = target_Place2.Pose() * desplazamiento2

                #Place

                robot.MoveL(pose_place2 * robomath.transl([0,0,-120]))
                robot.setSpeed(50,20)
                robot.MoveL(pose_place2)
                time.sleep(1)
                caja_actual.setParentStatic(framePalet2)
                robot.setSpeed(500,100)
                robot.MoveL(target_PPaso2.Pose())

                if x4 < 3:
                    x4 = x4 + 1
                if x4 == 3:
                    y4 = y4 + 1
                    x4 = 0
                if y4 == 2:
                    x4 = 0
                    y4 = 0
                    z4 = z4 + 1
                if z4 == 3:
                    prog2.RunProgram()
                    luz2 = 1
                    x4 = 0
                    y4 = 0
                    z4 = 0

                RDK.setParam('x4',x4)
                RDK.setParam('y4',y4)
                RDK.setParam('z4',z4)
                RDK.setParam('LuzPalet2',luz2)

                robot.setPoseFrame(general)
                robot.setSpeed(500,100)
                robot.MoveJ(target_Reposo.Pose())

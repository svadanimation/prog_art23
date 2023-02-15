"""
This is a tool used to build four poseable and differently colored robots.

Example:
- Run this script.
- Push the button in the Robot Selection window that corresponds to the robot that you want.
- Nathan is purple, Kent is gray, Ben is teal, and Jeremy is red.

ToDo:
- Add animations to the robots???

Author: Nathanael Perez
"""

#Imports Catalog
import maya.cmds as mc

#Create New Scene
mc.file(new = True, f = True)

#Define Shader
def make_shader(name, object = "", color = [1, 1, 1], type = "lambert", new = False):
    shader_name = name + "_shader"
    if mc.objExists(shader_name) and not new:
        shader_node = shader_name
    else:    
        shader_node = mc.shadingNode(type, asShader = True, n = shader_name)    
    mc.setAttr(shader_node + ".color", color[0], color[1], color[2], type = "double3")
    if object:
        mc.hyperShade(object, assign = shader_node)
    return shader_node

#Define Torso
def make_torso(name, shader):
    torso_name = name + "_torso"
    torso_cube = mc.polyCube(n = torso_name)[0]
    mc.scale(0.475, 0.908, 0.477, torso_cube)
    mc.move(0, 0.905, 0, torso_cube)
    mc.hyperShade(torso_cube, assign = shader)
    return torso_cube

#Define Legs
def make_leg(name, shader, side):
    leg_offset = (0.17, 0.303, 0)
    leg_name = name + "_" + side + "_leg"
    leg_cube = mc.polyCube(n = leg_name)[0]
    mc.scale(0.121, 0.6, 0.107, leg_cube)
    mc.xform(leg_cube, piv = [0, 0.20, 0], r = True)
    mc.hyperShade(leg_cube, assign = shader)
    if side == "right":
        mc.move(*leg_offset, leg_cube)
    if side == "left":
        mc.move(-leg_offset[0], leg_offset[1], leg_offset[2], leg_cube)
    return leg_cube
    
#Define Arms    
def make_arm(name, shader, side):
    arm_offset = (0.291, 0.759, 0)
    arm_name = name + "_" + side + "_arm"
    arm_cube = mc.polyCube(n = arm_name)[0]
    mc.scale(0.121, 0.6, 0.107, arm_cube)
    mc.hyperShade(arm_cube, assign = shader)
    if side == "right":
        mc.move(*arm_offset, arm_cube)
        mc.xform(arm_cube, piv = [-0.1, 0.20, 0], r = True) 
    if side == "left":
        mc.move(-arm_offset[0], arm_offset[1], arm_offset[2], arm_cube)
        mc.xform(arm_cube, piv = [0.1, 0.20, 0], r = True) 
    return arm_cube
    
#Define Skull
def make_skull(name, shader):
    skull_name = name + "_skull"
    skull_cube = mc.polyCube(n = skull_name)[0]
    mc.scale(1.2, 1, 1, skull_cube)
    mc.move(0, 1.649, 0, skull_cube)
    mc.hyperShade(skull_cube, assign = shader)
    return skull_cube

#Define Eyes
def make_eye(name, side, shader):
    eye_offset = (0.331, 1.639, 0.5)
    eye_name = name + "_" + side + "_eye"
    eye_sphere = mc.polySphere(n = eye_name, r = 0.2)[0]
    mc.hyperShade(eye_sphere, assign = shader)
    if side == "right":
        mc.move(*eye_offset, eye_sphere)
    if side == "left":
        mc.move(-eye_offset[0], eye_offset[1], eye_offset[2], eye_sphere)
    mc.parent
    return eye_sphere

#Define Cord
def make_cord(name, shader):
    cord_name = name + "_cord"
    cord_cylinder = mc.polyCylinder(n = cord_name)[0]
    mc.scale(0.040, 0.174, 0.040, cord_cylinder)
    mc.move(0, 2.259, 0)
    mc.hyperShade(cord_cylinder, assign = shader)
    return cord_cylinder

#Define Bulb
def make_bulb(name, shader):
    bulb_name = name + "_bulb"
    bulb_sphere = mc.polySphere(n = bulb_name, r = 0.15)[0]
    mc.move(0, 2.542, 0, bulb_sphere)
    mc.hyperShade(bulb_sphere, assign = shader)
    return bulb_sphere

#Define Antenna
def make_antenna(name, body_shader, glow_shader):
    antenna_name = name + "_antenna"
    cord = make_cord(name, body_shader)
    bulb = make_bulb(name, glow_shader)
    antenna_poly = mc.polyUnite(cord, bulb, n = antenna_name)
    mc.xform(antenna_poly, piv = [0, 2.00, 0], r = True)
    return antenna_poly

#Define Body
def make_body(name, shader):
    torso = make_torso(name, shader)
    right_leg = make_leg(name, shader, "right")
    left_leg = make_leg(name, shader, "left")
    mc.parent(right_leg, torso)
    mc.parent(left_leg, torso)
    right_arm = make_arm(name, shader, "right")
    left_arm = make_arm(name, shader, "left")
    mc.parent(right_arm, torso)
    mc.parent(left_arm, torso)
    return torso

#Define Head
def make_head(name, shader):
    skull = make_skull(name, shader)
    glow_shader = make_shader(name + "_glow", color = [30,30,0])
    right_eye = make_eye(name, "right", glow_shader)
    left_eye = make_eye(name, "left", glow_shader)
    mc.parent(right_eye, skull)
    mc.parent(left_eye, skull)
    antenna = make_antenna(name, shader, glow_shader)
    mc.parent(antenna, skull)
    return skull

#Define Robot
def make_robot(name, color):
    robot_group = mc.group(n = name, em = True)
    body_shader = make_shader(name, color = color)
    body = make_body(name, body_shader)
    head = make_head(name, body_shader)
    mc.parent(head, body)
    mc.parent(body, robot_group)
    mc.delete(robot_group, ch = True)
    mc.makeIdentity(a = True, t = True, r = True, s = True, n = False)
    mc.select(cl = True)
    return robot_group

#Define Button 1
def push_button1(*args):
  n = "Nathan"
  robot = make_robot(n, [0.2, 0.1, 0.2])
  mc.move(-7.5, 0, 0, robot)
  print(f"{n} has arrived!")

#Define Button 2
def push_button2(*args):
  n = "Kent"
  robot = make_robot(n, [0.4, 0.4, 0.4])
  mc.move(-2.5, 0, 0, robot)
  print(f"{n} has arrived!")

#Define Button 3
def push_button3(*args):
  n = "Ben"
  robot = make_robot(n, [0, 0.4, 0.4])
  mc.move(2.5, 0, 0, robot)
  print(f"{n} has arrived!")

#Define Button 4
def push_button4(*args):
  n = "Jeremy"
  robot = make_robot(n, [0.4, 0 ,0])
  mc.move(7.5, 0, 0, robot)
  print(f"{n} has arrived!")

#Selection Window
window_name = 'robot_selection'
if mc.window(window_name, ex = True):
    mc.deleteUI(window_name) 
window = cmds.window(window_name, t = "Robot Selection", w = 275)
cmds.columnLayout(adj = True)
cmds.button( l = 'Nathan', c = push_button1)
cmds.button( l = 'Kent', c = push_button2)
cmds.button( l = 'Ben', c = push_button3)
cmds.button( l = 'Jeremy', c = push_button4)
cmds.showWindow()
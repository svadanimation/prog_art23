
'''
Creates a UI that asks how many planets to build.
For every planet it creates it also has a chance of creating rings.
for every planet it chooses a different color.

Example:

Todo:
All that's left is to create the part of the UI that can create the colors more specifically.
and an animated ring around each other at different speeds.

Author:
Ada Morgan
'''

import maya.cmds as mc
import random


def create_ui():
    result = mc.promptDialog(
        title="Number of Planets",
        message="Enter the number of planets:",
        button=["Create", "Cancel"],
        defaultButton="Create",
        cancelButton="Cancel",
        dismissString="Cancel"
    )
    if result == "Create":
        num_planets = int(mc.promptDialog(query=True, text=True))
        create_solar_system(num_planets)

def assign_color(planet_group, color, shader_names, material_name):
    if mc.objExists(planet_group):
        material = mc.shadingNode('lambert', asShader=True, name=material_name)
        mc.setAttr(material + '.color', color[0], color[1], color[2], type='double3')
        # shader_name = random.choice(shader_names)
        mc.select(planet_group, r=True)
        mc.hyperShade(assign=material)
        mc.select(clear=True)
        
        '''
        shader = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=shader_name)
        mc.connectAttr('%s.outColor' % material, '%s.surfaceShader' % shader)
        if mc.listConnections('%s.surfaceShader' % planet_group):
            mc.disconnectAttr('%s.surfaceShader' % planet_group, '%s.outColor' % shader)
        mc.connectAttr('%s.outColor' % shader, '%s.surfaceShader' % planet_group)
        mc.setAttr('%s.color' % material, color[0], color[1], color[2], type='double3')
        '''
    else:
        if not mc.objExists(planet_group):
            print("Object " + planet_group + " does not exist.")

shader_names = ["planet_shader1", "planet_shader2", "planet_shader3"]

def create_planet(planet_name, index):
    print("Creating planet:", planet_name)
    radius = random.uniform(1, 10)
    sphere = mc.polySphere(n=planet_name, r=radius, sx=18, sy=18)[0]  # store sphere node
    print("Sphere:", sphere)
    ring_chance = random.uniform(0,1)
    if ring_chance > .5:
        ring_name = "rings_" + planet_name
        ring = create_rings(ring_name, radius)
        print("Ring:", ring)
        group_name = planet_name + "_group"
        mc.group(sphere,ring, n=group_name)
    else:
        group_name = planet_name + "_group"
        mc.group(sphere, n=group_name)
    print("Group:", group_name)
    
    '''
    nodes = mc.ls()
    print("Nodes:", nodes)
    transform_node = mc.listRelatives(group_name, parent=True)
    if transform_node is not None:
        transform_node = transform_node[0]
        print("Transform node created:", transform_node)
    else:
        print("Unable to find transform node for group:", group_name)
        transform_node = None
    return transform_node
    '''
    return group_name

def create_rings(ring_name, radius):
    rings_radius = radius + 2
    return mc.polyPipe(n=ring_name, r=rings_radius, sa=20, sh=1, h=1)

def create_solar_system(num_planets):
    # Define a list of shader names
    shader_names = ['planetShader', 'planetShader_0_blue', 'planetShader_0_purple']

    for i, _ in enumerate(range(num_planets)):
        planet_name = f"planet_{i}"
        planet_group = create_planet(planet_name=planet_name, index=i)
        # Generate a unique material name for each planet
        material_name = f"planet_{i}_material"
        # Choose a random shader from the list
        shader_name = random.choice(shader_names)
        r = random.uniform(0, 1)
        g = random.uniform(0, 1)
        b = random.uniform(0, 1)
        assign_color(planet_group, [r,g,b], shader_names, material_name)
        mc.move(i*20, 0, 0, planet_group)

if __name__=='__main__':
    create_ui()



'''
Select an object then run the program to rename both its shader and its shading group.
-Rileigh Juba
'''

import maya.cmds as mc

class Shader_renamer():
    def __init__(self, meshes):
        self.the_list = ''
        self.the_window = ''
        self.the_shader = ''
        self.the_sg = ''
        self.window_name = 're_win'
        self.meshes = meshes

        self.shader_renamer()

    def rename_shader(self, *args):
        selected_item = mc.textScrollList(self.the_list, q=True, si=True)[0]
        mc.rename(self.the_shader, selected_item + '_mat')
        mc.rename(self.the_sg, selected_item + '_SG')

        mc.deleteUI(self.the_window)
        mc.headsUpMessage( 'Shader renamed.', time=1.0 )

    def shader_renamer(self):
        meshes = self.meshes if isinstance(self.meshes, list) else [self.meshes]
        shade_dict = {}
        for mesh in meshes: 
            sel_shape = mc.listRelatives(mesh, shapes = True)
            sel_sg = mc.listConnections(sel_shape, type = 'shadingEngine')
            sel_shad = mc.hyperShade(lun = sel_sg[0], noShapes = True, noTransforms = True)
            shader = sel_shad.pop(0)
            if not shader in shade_dict.keys():
                shade_dict[shader] = set()
            shade_dict[shader].update(sel_shad)
            self.the_sg = sel_sg

        throwaway = [shape.split('|') for shape in shade_dict[shader]]
        poss_name = [nema[1] for nema in throwaway]
        shade_dict[shader] = poss_name
        
        for shader, filtered_meshes in shade_dict.items():
            self.the_shader = shader
            if len(filtered_meshes) > 1:
                if mc.window(self.window_name, ex = True):
                    mc.deleteUI(self.window_name)
                self.the_window = mc.window(self.window_name, t='Your shader\'s new name shall be:')
                mc.paneLayout()
                self.the_list = mc.textScrollList(numberOfRows=len(filtered_meshes), 
                                                  allowMultiSelection=False,
                                                  append=list(filtered_meshes),
                                                  dcc=self.rename_shader)
                mc.showWindow(self.the_window)
            else:
                print(self.the_sg)
                for shape in filtered_meshes:
                    name = ''
                    split = shape.split('|')
                    if len(split) >= 2:
                        name = split[-2] 
                    else:
                        name = split[-1]
                        
                mc.rename(shader, name + '_mat') 
                mc.rename(self.the_sg, name + '_SG')  
                mc.headsUpMessage( 'Shader renamed.', time=1.0 )



def select_mesh():
    sel = mc.ls(sl=True)
    if not sel:
        mc.warning("Nothing selected.")
        return
    shader_renamer = Shader_renamer(sel)
    
select_mesh()
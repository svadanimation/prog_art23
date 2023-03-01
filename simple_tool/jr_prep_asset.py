'''
This preps and cleans up your 3d models
Creates a group based on selection
Creates the proper hierarchy 
Organizes your assets by grouping and appending _mod 
Freezes transforms, resets pivot, and snaps to ground 

Example: Given a selection in your scene
    Select your model
    Use text box pop up to rename your item
    Select freeze transform or snap selection to ground

TODO:
Fix Global function callings(scope issue)

Author:
Jeremy Ramirez

'''
#import
import maya.cmds as mc
#This is  script to create a group hierarchy in order to prep your 3d model for publishing
# it is based on object selection
#make sure object your are selecting is not already in a group! 

def setup_asset():
    sel= mc.ls(sl=True)

    # NOTE =======================================
    # filter this based on selection type, what happens if someone selects components
    # try filtering for assemblies

    window='myWindow'
    # Group will be created based on selection.
    # Group and Object will be renamed based on text pop up

    # NOTE =======================================
    # add a title to your dialog

    result = mc.promptDialog(
            title='',
            message='Enter Name:',
            button=['OK', 'Cancel'],
            defaultButton='OK',
            cancelButton='Cancel',
            dismissString='Cancel')
    # Groups your selected object and creates a group hierarchy based on text in box

    # NOTE =======================================
    # try not to encumber your UI and execution code
    # it would be far better to have your if result == 'OK':
    # call a function like 'make_parent'

    if result == 'OK':
        text = mc.promptDialog(query=True, text=True)
        grp2 = mc.group(em=True,n=text)
        grp1 = mc.group(em=True, n=text+ '_mod')
        mc.parent(grp1,grp2)
        mc.parent(sel,grp1)
        for obj in sel:
            mc.rename(obj,text)
    #resets pivot and snaps it to the bottom of selected object    
        bbox = mc.exactWorldBoundingBox()
        bottom = [(bbox[0] + bbox[3])/2, bbox[1], (bbox[2] + bbox[5])/2]
        mc.xform(piv=bottom, ws=True)
        
        popUp()
        
    #Warning pop up box if script is canceled    
    else:
        mc.confirmDialog(title='Confirm', 
        message='No Group Created', 
        button=['OK'], 
        defaultButton='OK')
    #freezes transforms on object and deletes history     
def freeze(*args):
    # NOTE =======================================
    # getting a fresh selection, unfortunately, you'd need to use 
    # a class or the 'partial' module to pass in the selection

    sel= mc.ls(sl=True)
    for obj in sel:
        bbox = mc.exactWorldBoundingBox()
        bottom = [(bbox[0] + bbox[3])/2, bbox[1], (bbox[2] + bbox[5])/2]
        mc.xform(piv=bottom, ws=True)
        mc.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
        mc.delete(sel, constructionHistory = True)
        mc.deleteUI('myWindow')
    
# NOTE =======================================
# Tidy up your dialog title and button names
 
#snap sobject to ground plane, resets pivot to the bottom of the object, freezes transforms, and deletes history
def snapbot(*args):
    sel = mc.ls(sl=True)
    if not sel:
        mc.confirmDialog(title='GOOSE!!', 
        message='Pls Make A Selection', 
        button=['Yeah..Im Soo Silly!'], 
        defaultButton='OK')        
    bbox = mc.exactWorldBoundingBox()
    bottom = [(bbox[0] + bbox[3])/2, bbox[1], (bbox[2] + bbox[5])/2]
    mc.xform(piv=bottom, ws=True)
    mc.move(0, y=True)
    mc.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
    mc.delete(sel, constructionHistory = True)
    mc.deleteUI('myWindow')


#Maya pop up window to select which option you would like to contiue with


# NOTE =======================================
# Use a descriptive title
# call the window more descriptively than 'myWindow'. 'asset_window' for example
# apply that symbol change throughout

def popUp():
    mc.window('myWindow', title= 'What Shall We Do?', widthHeight=(300,60) )
    mc.columnLayout( adjustableColumn=True )
    mc.button( label='Freeze Transform', command=freeze )
    mc.button( label='Snap to Ground', command=snapbot)
    mc.showWindow('myWindow')


if __name__ == '__main__':
   setup_asset() 
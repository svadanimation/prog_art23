'''
This is a tool that allows you to toggle back and forth between the stepped and splined defualt settings.
It also allows you to change the tangents on any existing keys in a selection.

Example:
The UI has four buttons. The two buttons at the top will toggle the global default settings, while the two at the bottom will
change the tangents on a selected object's keys. For the selection buttons to work, there must be a selection, or a warning will pop up.

Author:
Kaleb Rivas
'''

import maya.cmds as mc

#This sets the defualt animation settings to stepped mode by changing the in tnagent to Clamped and the out tangent to Step
def setBlockingPrefs(*args):
    mc.keyTangent(edit = True, g = True, itt = 'clamped')
    mc.keyTangent(edit = True, g = True, ott = 'step')
    mc.keyTangent(edit = True, g = True, weightedTangents = 1)
    #here the buttons and text are edited and updated 
    updateButtons(True)
    updateText(True)

#This sets the defualt animation settings to splined mode by changing both the in tnagent and the out tangent to auto
def setSpliningPrefs(*args):
    mc.keyTangent(edit = True, g = True, itt = 'auto')
    mc.keyTangent(edit = True, g = True, ott = 'auto')
    mc.keyTangent(edit = True, g = True, weightedTangents = 1)
    #here the buttons and text are edited and updated 
    updateButtons(True)
    updateText(True)

#This function checks the current settings
def checkSettings():
    
    #These variables are given a string value such as Auto or Step
    ittValue = mc.keyTangent(query=True, g=True, itt=True)
    ottValue = mc.keyTangent(query=True, g=True, ott=True)
    
    #These variables are used for activating and deactivating the buttons 
    enableSpline = (ittValue[0] == 'auto' and ottValue[0] == 'auto') == False
    enableStep = (ittValue[0] == 'clamped' and ottValue[0] == 'step') == False

    return (enableSpline, enableStep)

#this function can create buttons or just edit them based on the parameters given    
def updateButtons(editVal):
    spline, stepped = checkSettings()
    #The buttons will be active based on which mode we are in
    mc.button("btnSpline", e=editVal, label="Change defualt to Splined", command=setSpliningPrefs, enable=spline)
    mc.button("btnStep", e=editVal, label="Change defualt to Stepped", command=setBlockingPrefs, enable=stepped)

#This function labels the buttons 
def updateText(editVal):
    isSpline, isStep = checkSettings()
    
    modeName = "an Unknown"
    
    if isSpline == False:
        modeName = "Splined"
    
    if isStep == False:
        modeName = "Stepped"
    
    mc.text("txtMessage", edit=editVal, label=f'You Are Currently In {modeName} Default settings', fn="boldLabelFont")

#This object sets the tangents of the selected objects to splined
def setSelSpline(*args):

    sel=mc.ls(sl=True)
    
    if not sel:
        mc.confirmDialog(title='oops', message='nothing selected')
        return
    
    for obj in sel:
        mc.keyTangent(obj, edit = True, itt = 'auto')
        mc.keyTangent(obj, edit = True, ott = 'auto')

#This function sets the tangents of the selected object to stepped
def setSelStepped(*args):

    sel=mc.ls(sl=True)
    
    if not sel:
        mc.confirmDialog(title='oops', message='nothing selected')
        return
    
    for obj in sel:
        mc.keyTangent(obj, edit = True, itt = 'clamped')
        mc.keyTangent(obj, edit = True, ott = 'step')

#this function creates buttons to manipulate the tangents of selected objects 
def SelBtn():
    mc.button(label='Set Selection to Splined', command=setSelSpline, enable=True)
    mc.button(label='Set Selection to Stepped', command=setSelStepped, enable= True)
    
def SelTxt():
    mc.text(label='Override the Tangents of Selected Objects')


#This function creates a UI with buttons
def UI():
    
    window1='_animation_prefernces'
    
    if mc.window(window1,exists=True):
        mc.deleteUI(window1)
    mc.window( window1, title= 'Animation Preferences', widthHeight = (400,310))
    mc.columnLayout( adjustableColumn=True )
    mc.separator(height=20)
    #This creates text rather than editing
    updateText(False)

    mc.separator(height=20)   
    #this creates buttons rather than editing 
    updateButtons(False)
    
    mc.separator(height=20) 
    SelTxt()
    mc.separator(height=20)
    SelBtn()
    mc.showWindow(window1)
    
if __name__ == "__main__":    
    UI()
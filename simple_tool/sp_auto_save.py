import maya.cmds as cmds

def setup_autosave():
    print ("stub, no functionality")
    pass

# This needs to be in a function
if __name__ == '__main__':
    # Set the autosave time interval to 10 minutes
    cmds.autoSave( int=5 )

    # Save automatically without confirmation
    cmds.autoSave(enable=True)

    # Show a confirmation dialog before auto saving
    result = cmds.confirmDialog(title='confirm save', message='¿do you want to save the scene?', button=['Yes', 'No'], defaultButton='Yes', cancelButton='No', dismissString='No')

    if result == 'Yes':
        # The user confirmed that they want to save the scene
        cmds.file(save=True, force=True)
    else:
        # The user did not confirm the save, disable autosave
        cmds.autoSave(enable=False)
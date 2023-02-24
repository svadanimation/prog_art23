
import maya.cmds as mc
from functools import partial

# from render_submit import vray_standaloneSubmit as vss

def edit_cell(row, column, value):
    return 1


def filter_keys(d: dict, keys: list):
    count = []
    for k, v in d.items():
        if isinstance(v, dict):
            filter_keys(v, count, keys)
        else:
            if k in keys:
                count.append(1)
    return len(count)

def cell_color(row, column):
    global hilight
    lvl = hilight[row-1][1]+1
    factor = 150

    value =1.0/float(lvl)*factor
    return [value, value, value]


def validateQubeDictUI(jobs):
    if( mc.window( 'submitDict', q = 1, ex = 1 ) ):mc.deleteUI( 'submitDict' )

    # only show these keys
    keys = ['name', 'cpus', 'imgHeight', 'imgWidth', 'padding', 'range', 'imgFile', 'renderpath', 'cluster', 'priority', 'reservations']
    jobsLength = filter_keys(jobs, keys)

    window = mc.window('submitDict', widthHeight=(400, 300))
    form = mc.formLayout()
    table = mc.scriptTable(rows=jobsLength, columns=2, label=[(1,"Key"), (2,"Value")], cellChangedCmd=edit_cell)
    mc.scriptTable(table, cw = [1,250], edit=True)
    mc.scriptTable(table, cw = [2,500], edit=True)
    mc.scriptTable(table, edit=True, cbc=cell_color)


    okButton = mc.button('okButton', label="Submit", command=partial(scrapeQubeDict, jobs, table))
    cancelButton = mc.button(label="Cancel",command="mc.deleteUI( 'submitDict' )")

    mc.formLayout(form, edit=True, attachForm=[(table, 'top', 0), (table, 'left', 0), (table, 'right', 0), (okButton, 'left', 0), (okButton, 'bottom', 0), (cancelButton, 'bottom', 0), (cancelButton, 'right', 0)], attachControl=(table, 'bottom', 0, okButton), attachNone=[(okButton, 'top'),(cancelButton, 'top')],  attachPosition=[(okButton, 'right', 0, 50), (cancelButton, 'left', 0, 50)] )


    visualise_dict(jobs, table=table, keys=keys)
    mc.setFocus(okButton)
    mc.showWindow( window )


def scrapeQubeDict(jobs, table, *args):
    renderPath = jobs['vray_job']['renderpath']
    rows = mc.scriptTable(table, rows=True, query=True)
    for row in range(1,rows):
        key = mc.scriptTable(table, cellIndex=(row,1), cellValue=True, query=True)[0]
        value = mc.scriptTable(table, cellIndex=(row,2), cellValue=True, query=True)[0]
        if value != '{}':
            #required because of some funky unicode encoding that happens during exec
            value = "'" + value.replace('\\', '\\\\') + "'"


        keys =  key.split(':')
        path = ''
        for k in keys:
            path += "['" + k + "']"
        #print path, value
        exec('jobs' + path +' = ' + value)
        #print mc.scriptTable(table, cellIndex=(row,2), cellValue=True, query=True)
    mc.deleteUI( 'submitDict' )

    #============================================================================================
    #Need to update the package cmdline to reflect changes to args
    #============================================================================================

    print ("Updating cmdline path")
    newPath = jobs['vray_job']['renderpath']
    cmdline = jobs['vray_job']['package']['cmdline']
    imgfile = jobs['vray_job']['package']['-imgFile']
    scenefile = jobs['vray_job']['package']['-sceneFile']
    jobs['vray_job']['package']['cmdline'] = cmdline.replace(renderPath, newPath)
    jobs['vray_job']['package']['-imgFile'] = imgfile.replace(renderPath, newPath)
    jobs['vray_job']['package']['-sceneFile'] = scenefile.replace(renderPath, newPath)

    return jobs


# this is awful need to figure out a better idea
index = [0]
def visualise_dict(d,lvl=0,parent='', table='', keys=[]):
    global hilight


    # go through the dictionary alphabetically
    for k in sorted(d):
        #print parent
        #print index


        # print the table header if we're at the beginning
        if lvl == 0 and k == sorted(d)[0]:
            index[0] = 0
            hilight = []

            #print('{:<45} {:<15} {:<10}'.format('KEY','LEVEL','TYPE'))
            #print('-'*79)


        #print index[0]

        indent = '  '*lvl # indent the table to visualise hierarchy
        t = str(type(d[k]))
        v = str((d[k]))
        if type(d[k])==dict:
            v='{}'

        # print details of each entry
        #print("{:<45} {:<15} {:<10}".format(indent+str(k),lvl,t))
        #mc.scriptTable(table, edit=True,insertRow=1)
        if k in keys:
            index[0]+=1
            mc.scriptTable(table, cellIndex=(index[0],1), edit=True, cellValue=str(parent+k))
            mc.scriptTable(table, cellIndex=(index[0],2), edit=True, cellValue=str(v))


            hilight.append((index[0],lvl))



        # if the entry is a dictionary
        if type(d[k])==dict:
            # visualise THAT dictionary with +1 indent
            visualise_dict(d[k],lvl+1,parent=(parent + k + ':'), table=table, keys=keys)

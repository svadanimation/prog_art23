'''
    Display a validation UI for the Qube job dictionary

'''

import maya.cmds as mc
from render_submit import vray_submit


class SubmitUI(object):
    '''
    Display a validation UI for the Qube job dictionary
    Creates a window with a table of the jobs and a button to submit the jobs

    '''
    WINDOW = 'submit_ui'
    keys = [['vray_job','name'],
            ['vray_job', 'cpus'],
            ['vray_job', 'package', '-imgHeight'],
            ['vray_job', 'package', '-imgWidth'],
            ['vray_job', 'package', 'padding'],
            ['vray_job', 'package', 'range'],
            ['vray_job', 'package', 'imgFile'],
            ['vray_job', 'package', 'renderpath'],
            ['vray_job', 'cluster'],
            ['vray_job', 'priority'],
            ['vray_job', 'reservations'],
            ['vray_job', 'validate_fileMinSize']]

    def __init__(self, jobs: dict = None):
        self.jobs = jobs
        if not jobs:
            self.jobs = vray_submit.get_jobs()
        self.window = None
        self.form = None
        self.table = None
        self.ok_button = None
        self.cancel_button = None
        self.hilight = None
        self.job_count = None

        vray_submit.vray_config()

    def show(self):
        '''Show the UI'''
        if mc.window( self.WINDOW, q = 1, ex = 1 ):
            mc.deleteUI( self.WINDOW)
        mc.showWindow( self.window )

    @staticmethod
    def deep_get(_dict, keys, default=None):
        """
        Safely gets a value in a nested dictionary given a list of keys.

        Args:
            nested_dict (dict): The nested dictionary to update.
            key_list (list): A list of keys specifying the path to the value to update.
            default: The default value to return if the key is not found.

        Returns:
            Requested key, None
        """
        for key in keys:
            if isinstance(_dict, dict):
                _dict = _dict.get(key, default)
            else:
                return default
        return _dict

    @staticmethod
    def deep_update(nested_dict, key_list, value, default=None):
        """
        Safely updates a value in a nested dictionary given a list of keys.
        If intermediate dictionaries or the key do not exist,
        they are created with the specified default value.

        Args:
            nested_dict (dict): The nested dictionary to update.
            key_list (list): A list of keys specifying the path to the value to update.
            value: The new value to set.
            default: The default value to use when creating intermediate dictionaries.

        Returns:
            None
        """
        if not isinstance(nested_dict, dict):
            return

        for key in key_list[:-1]:
            nested_dict = nested_dict.setdefault(key, {})
            if not isinstance(nested_dict, dict):
                return

        nested_dict.setdefault(key_list[-1], value if value is not None else default)

    def edit_cell(self):
        '''Callback for when a cell is edited in the table'''
        return 1

    def validate_submit_dict(self):
        '''Validate the Qube job dictionary

        :param jobs: dictonary of qube jobs
        :type jobs: dict
        '''

        # only show these keys

        self.window = mc.window('submit_ui', widthHeight=(400, 300))
        self.form = mc.formLayout()
        self.table = mc.scriptTable(rows=len(self.keys),
                            columns=2,
                            label=[(1,"Key"), (2,"Value")],
                            cellChangedCmd=self.edit_cell)
        mc.scriptTable(self.table, cw = [1,250], edit=True)
        mc.scriptTable(self.table, cw = [2,500], edit=True)

        ok_button = mc.button('okButton',
                            label="Submit",
                            command=self.scrape_table)

        self.cancel_button = mc.button(label="Cancel",command=f'mc.deleteUI({self.window})')

        mc.formLayout(self.form,
                    edit=True,
                    attachForm=[(self.table, 'top', 0),
                                (self.table, 'left', 0),
                                (self.table, 'right', 0),
                                (self.ok_button, 'left', 0),
                                (self.ok_button, 'bottom', 0),
                                (self.cancel_button, 'bottom', 0),
                                (self.cancel_button, 'right', 0)],
                    attachControl=(self.table, 'bottom', 0, ok_button),
                    attachNone=[(self.ok_button, 'top'),(self.cancel_button, 'top')],
                    attachPosition=[(self.ok_button, 'right', 0, 50),
                                    (self.cancel_button, 'left', 0, 50)] )

        self.draw_table()
        mc.setFocus(ok_button)

        self.show()

    def draw_table(self):
        '''Fill the table with the selected items from the jobs dictionary
        '''

        for i, key in enumerate(self.keys):
            value =''
            if isinstance(key, list):
                value = self.deep_get(self.jobs, key)
            else:
                value = self.jobs[key]

            colors = [(0.5,0.5,0.5), (0.3,0.3,0.3)]
            color = colors[i % 2]
            mc.scriptTable(self.table, cellIndex=(i,1),
                           edit=True, cellValue=str(':'.join(key)), cellColor=color)
            mc.scriptTable(self.table, cellIndex=(i,2),
                           edit=True, cellValue=str(value), cellColor=color)

    def scrape_table(self):
        '''Scrape the table and update the jobs dictionary
        '''
        rows = mc.scriptTable(self.table, rows=True, query=True)
        for row in range(1,rows):
            key = mc.scriptTable(self.table, cellIndex=(row,1), cellValue=True, query=True)[0]
            value = mc.scriptTable(self.table, cellIndex=(row,2), cellValue=True, query=True)[0]
            if value != dict:
                #required because of some funky unicode encoding that happens during exec
                value = "'" + value.replace('\\', '\\\\') + "'"

            keys =  key.split(':')
            for k in keys:
                self.deep_update(self.jobs, k, value)

        mc.deleteUI(self.window)
        vray_submit.submit_jobs(self.jobs)


if __name__ == '__main__':
    submit_ui = SubmitUI()

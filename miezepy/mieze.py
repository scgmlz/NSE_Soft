#  -*- coding: utf-8 -*-
# *****************************************************************************
# Copyright (c) 2017 by the NSE analysis contributors (see AUTHORS)
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# Module authors:
#   Alexander Schober <alex.schober@mac.com>
#
# *****************************************************************************


#############################
#import main components
from .core.core_handler             import Handler
from .gui.py_gui.window_handlers    import WindowHandler


class Mieze(Handler):

    '''
    ##############################################
    Here lies the main NSE tool manager class. It can be
    accessed in the python terminal through: 
    "from NSE.Main import Manager as NSE"
    ##############################################
    '''

    def __init__(self, GUI = False):

        ##############################################
        #initiate the core manager  
        Handler.__init__(self)

        ##############################################
        #initiate the GUI manager if need be
        if GUI == True:

            self.gui = WindowHandler(self)

    def run(self):
        self.gui.run()




if __name__ == '__main__':
    app = Mieze(GUI = True)
    app.gui.active_windows['MainWindow'].target.widgetClasses[0].addEnvironment()
    env = app.current_env
    env.io.loadFromPython(
        "Examples/file_3.py")#, 
        #app.gui.active_windows['Import'].target)
    #env.io.generate()
    # app.gui.active_windows['MainWindow'].target.openLoad(env.name)
    app.gui.active_windows['MainWindow'].target.widgetClasses[0].refreshData()


    #app.gui.active_windows['Import'].target.link(env.io)

    # for i in range(13):
    #     app.active_windows['Import'].target.addElement()

    # app.active_windows['Import'].target.setCurrentElement(0)

    # target = env.io.import_objects[0].meta_handler
    # target.buildMeta('/Users/alexanderschober/Downloads/Data_analysis_Schober/201806_RESEDA/data/00122186.tof')

    # target.selected_meta.append([
    #     'cbox_0a_fg_freq_value',
    #     'Hz',
    #     'Freq. first',
    #     '1'])
    # target.selected_meta.append([
    #     'cbox_0b_fg_freq_value',
    #     'Hz',
    #     'Freq. second',
    #     '1'])
    # target.selected_meta.append([
    #     'selector_lambda_value',
    #     'A',
    #     'Wavelength',
    #     '1.e-10'])
    # target.selected_meta.append([
    #     'psd_distance_value',
    #     'm',
    #     'lsd',
    #     '1.e9 '])
    # target.selected_meta.append([
    #     'monitor1',
    #     'm',
    #     'Monitor',
    #     '1'])

    # target.checkPresence()

    # app.active_windows['Import'].target.propagateMeta()

    
    # folder = '/Users/alexanderschober/Downloads/Data_analysis_Schober 2/201806_RESEDA/data/0012'

    # target = env.io.import_objects[0].file_handler
    # target.addFiles([folder+str(element)+'.tof' 
    # for element in range(2186, 2194)])

    # target = env.io.import_objects[1].file_handler
    # target.addFiles([folder+str(element)+'.tof' 
    # for element in range(2387, 2395)])

    # target = env.io.import_objects[2].file_handler
    # target.addFiles([folder+str(element)+'.tof' 
    # for element in [2396, 2398, 2401, 2402, 2403]])

    # target = env.io.import_objects[3].file_handler
    # target.addFiles([folder+str(element)+'.tof' 
    # for element in [2408, 2409, 2410]])

    # target = env.io.import_objects[4].file_handler
    # target.addFiles([folder+str(element)+'.tof' 
    # for element in [2412, 2413, 2374, 2375, 2376, 2377, 2378, 2379]])

    # target = env.io.import_objects[5].file_handler
    # target.addFiles([folder+str(element)+'.tof' 
    # for element in [2320, 2321, 2414, 2323, 2415, 2325, 2326, 2327]])
    
    # target = env.io.import_objects[6].file_handler
    # target.addFiles([folder+str(element)+'.tof' 
    # for element in [2348, 2349, 2350, 2351, 2352, 2353, 2354]])

    # target = env.io.import_objects[7].file_handler
    # target.addFiles([folder+str(element)+'.tof' 
    # for element in range(2334, 2342)])

    # target = env.io.import_objects[8].file_handler
    # target.addFiles([folder+str(element)+'.tof' 
    # for element in [2416]])

    # target = env.io.import_objects[9].file_handler
    # target.addFiles([folder+str(element)+'.tof' 
    # for element in range(2418, 2426)])

    # target = env.io.import_objects[10].file_handler
    # target.addFiles([folder+str(element)+'.tof' 
    # for element in [2362, 2363, 2364, 2365, 2366, 2426, 2368, 2369]])

    # target = env.io.import_objects[11].file_handler
    # target.addFiles([folder+str(element)+'.tof' 
    # for element in range(2434, 2442)])
    
    # target = env.io.import_objects[12].file_handler
    # target.addFiles([folder+str(element)+'.tof' 
    # for element in range(2306, 2314)])

    # app.active_windows['Import'].target.setFileList()
    # app.active_windows['Import'].target.setMetaList()

    # for i in range(len(app.active_windows['Import'].target.elements)):
    #     app.active_windows['Import'].target.setCurrentElement(row = i)
    #     app.active_windows['Import'].target.populate()

    # env.io.saveToPython("file.py")


    app.run()
    
        


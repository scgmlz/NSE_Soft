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

import os

class ScriptStructure:

    def __init__(self):
        '''
        The script part was initially implanted into 
        the process module but found to confuse its
        purpose. This is why a separate structure
        will now handle it.
        '''
        self.default_scripts = []
        with open(
            os.path.dirname(os.path.realpath(__file__))
            + '/import_process.py','r') as f:
            self.default_scripts.append(f.read())
        with open(
            os.path.dirname(os.path.realpath(__file__))
            + '/set_fit_process.py','r') as f:
            self.default_scripts.append(f.read())
        with open(
            os.path.dirname(os.path.realpath(__file__))
            + '/phase_process.py','r') as f:
            self.default_scripts.append(f.read())
        with open(
            os.path.dirname(os.path.realpath(__file__))
            + '/reduction_process.py','r') as f:
            self.default_scripts.append(f.read())
        with open(os.path.dirname(
            os.path.realpath(__file__))
            + '/post_process.py','r') as f:
            self.default_scripts.append(f.read())

        self.editable_scripts = list(self.default_scripts)

    def loadScripts(self, path):
        '''
        Initialize the default python scipts so that 
        the system can be set.

        Parameters
        ----------
        path : string
            The path of the file
        '''
        with open(path,'r') as f:
            text = f.read()

        if 'metadata_class.add_metadata' in text:
            text = self.reformatScript(text)

        check = text.split('##--FIT-PARA--##')
        if len(check) > 1:
            file_type = 'new'
        else:
            file_type = 'old'

        if file_type == 'old':
            strings = [
                text.split('##--IMPORT--##')[1],
                text.split('##--PHASE--##')[1].split(
                    'value = foils_in_echo)')[0]+'value = foils_in_echo)',
                'environnement = self.env\n'+text.split('##--PHASE--##')[1].split(
                    'value = foils_in_echo)')[1],
                text.split('##--REDUCTION--##')[1],
                text.split('##--POST--##')[1] ]
        elif file_type == 'new':
            strings = [
                text.split('##--IMPORT--##')[1],
                text.split('##--FIT-PARA--##')[1],
                text.split('##--PHASE--##')[1],
                text.split('##--REDUCTION--##')[1],
                text.split('##--POST--##')[1]]

        self.editable_scripts = list(strings)

    def saveScripts(self, path, strings):
        '''
        Initialize the default python scipts so that 
        the system can be set.

        Parameters
        ----------
        path : string
            The file path to be saved

        strings : string array
            The list of scripts to be saved
        '''
        string = (
            "##--IMPORT--##\n"
            + strings[0]
            + "\n##--IMPORT--##\n"
            "##--FIT-PARA--##\n"
            + strings[1]
            + "\n##--FIT-PARA--##\n"
            + "##--PHASE--##\n"
            + strings[2]
            + "\n##--PHASE--##\n"
            + "##--REDUCTION--##\n"
            + strings[3]
            + "\n##--REDUCTION--##\n"
            + "##--POST--##\n"
            + strings[4]
            + "\n##--POST--##\n")

        f = open(path, 'w')
        f.write(string)
        f.close()

    def reformatScript(self, text):
        '''
        This function will reformat the text input to meet the
        new specifications of our software. Most function calls
        have been updated.

        Parameters
        ----------
        text : string
            The formated text to be formater

        Returns
        ------- 
        text : string
            The formated text to returned to the text importer
        '''
        text = text.replace('add_metadata', 'addMetadata')
        text = text.replace('get_result', 'results.getLastResult')
        text = text.replace('calculate_echo', 'calculateEcho')
        text = text.replace('calculate_shift', 'calcShift')
        text = text.replace('calculate_ref_contrast', 'calcContrastRef')
        text = text.replace('calculate_contrast', 'calcContrastMain')
        text = text.replace('environnement.process.remove_foils()\n', '')
        text = text.replace(
            "environnement.fit.set_parameter( name = 'foils_in_echo', value = foils_in_echo)\n", 
            "environnement.fit.set_parameter( name = 'foils_in_echo', value = foils_in_echo)\n"
            +"environnement.fit.set_parameter( name = 'exposure', value = exposure)\n"
            +"environnement.instrument.setDetector(instrument, detector)\n")
        text = text.replace(
            "environnement.fit.set_parameter( name = 'Select',",
            "instrument = 'Reseda'\n"
            +"detector = None\n\n"
            +"exposure = False\n\n"
            +"environnement.fit.set_parameter( name = 'Select',")

        return text
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
            + '/script_modules/import_process.py','r') as f:
            self.default_scripts.append(f.read())
        with open(
            os.path.dirname(os.path.realpath(__file__))
            + '/script_modules/set_fit_process.py','r') as f:
            self.default_scripts.append(f.read())
        with open(
            os.path.dirname(os.path.realpath(__file__))
            + '/script_modules/phase_process.py','r') as f:
            self.default_scripts.append(f.read())
        with open(
            os.path.dirname(os.path.realpath(__file__))
            + '/script_modules/reduction_process.py','r') as f:
            self.default_scripts.append(f.read())
        with open(os.path.dirname(
            os.path.realpath(__file__))
            + '/script_modules/post_process.py','r') as f:
            self.default_scripts.append(f.read())

        self.editable_scripts = list(self.default_scripts)

    def resetScript(self,idx):
        '''
        Reset a script given by his index 
        value as integer.

        Parameters
        ----------
        idx : int
            The index of the script to reset
        '''
        self.editable_scripts[idx] = self.default_scripts[idx]

    def grabFromOther(self, other):
        '''
        This method is to allow cross 
        environnement transfer of the 
        elements.

        Parameters
        ----------
        other : ScriptStructure
            The script structure to use
        '''
        self.editable_scripts = list(other.editable_scripts)

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

    def saveScripts(self, path):
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
            + self.editable_scripts[0]
            + "\n##--IMPORT--##\n"
            "##--FIT-PARA--##\n"
            + self.editable_scripts[1]
            + "\n##--FIT-PARA--##\n"
            + "##--PHASE--##\n"
            + self.editable_scripts[2]
            + "\n##--PHASE--##\n"
            + "##--REDUCTION--##\n"
            + self.editable_scripts[3]
            + "\n##--REDUCTION--##\n"
            + "##--POST--##\n"
            + self.editable_scripts[4]
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

    def readFromScripts(self):
        '''
        Read from the scripts to produce a dictionary
        with all the information that can be set if it
        is found.
        '''
        #----------------------------------------#
        text_array = self.editable_scripts[0].split("\n")

        #Foils to consider
        filtered_text_array = [
            element if "metadata_class.addMetadata('Selected foils'" in element 
            else '' 
            for element in text_array]
        foil_check = []
        for element in filtered_text_array:
            if not element == '':
                foil_check = eval('['+element.split('[')[1].split(']')[0]+']')

        del text_array
        #----------------------------------------#
        text_array = self.editable_scripts[1].split("\n")

        #Foils
        filtered_text_array = [
            element if 'foils_in_echo.append(' in element else '' 
            for element in text_array]
        foils_in_echo = []
        for element in filtered_text_array:
            if not element == '':
                exec(element.strip())
            
        #Selected
        filtered_text_array = [
            element if 'Selected = [' in element else '' 
            for element in text_array]
        Selected = []
        for element in filtered_text_array:
            if not element == '':
                Selected = eval(element.split('Selected =' )[1])

        #Reference
        filtered_text_array = [
            element if 'Reference = [' in element else '' 
            for element in text_array]
        Reference = None
        for element in filtered_text_array:
            if not element == '':
                Reference = eval(element.split('Reference = ' )[1])

        #Background
        filtered_text_array = [
            element if 'Background = ' in element else '' 
            for element in text_array]
        Background = None
        for element in filtered_text_array:
            if not element == '':
                Background = eval(element.split('Background = ' )[1])

        #instrument
        filtered_text_array = [
            element if 'instrument = ' in element else '' 
            for element in text_array]
        instrument = None
        for element in filtered_text_array:
            if not element == '':
                instrument = eval(element.split('instrument = ' )[1])

        #detector
        filtered_text_array = [
            element if 'detector = ' in element else '' 
            for element in text_array]
        detector = None
        for element in filtered_text_array:
            if not element == '':
                detector = eval(element.split('detector = ' )[1])

        #exposure
        filtered_text_array = [
            element if 'exposure = ' in element else '' 
            for element in text_array]
        exposure = False
        for element in filtered_text_array:
            if not element == '':
                exposure = eval(element.split('exposure = ' )[1])

        #time_channels
        filtered_text_array = [
            element if 'TimeChannels = ' in element else '' 
            for element in text_array]
        time_channels = False
        for element in filtered_text_array:
            if not element == '':
                time_channels = eval(element.split('TimeChannels = ' )[1])

        del text_array
        #----------------------------------------#
        text_array = self.editable_scripts[2].split("\n")

        #masks
        filtered_text_array = [
            element if "mask.setMask(" in element 
            else '' 
            for element in text_array]
        phase_mask = []
        for element in filtered_text_array:
            if not element == '':
                phase_mask = eval(element.split('(')[1].split(')')[0])

        del text_array
        #----------------------------------------#
        text_array = self.editable_scripts[3].split("\n")

        #Foils to consider
        filtered_text_array = [
            element if "mask.setMask(" in element 
            else '' 
            for element in text_array]
        reduction_mask = []
        for element in filtered_text_array:
            if not element == '':
                reduction_mask = eval(element.split('(')[1].split(')')[0])

        del text_array
        container = {}
        container['foils_in_echo'] = foils_in_echo
        container['Selected']      = Selected
        container['Reference']     = Reference
        container['Background']    = Background
        container['foil_check']    = foil_check
        container['phase_mask']    = phase_mask
        container['reduction_mask']= reduction_mask
        container['instrument']    = instrument
        container['detector']      = detector
        container['exposure']      = exposure
        container['time_channels'] = time_channels
        
        return container

    def setEditable(self, index, code):
        '''
        Read from the scripts to produce a dictionary
        with all the information that can be set if it
        is found.

        Parameters
        ----------
        index : int
            The index of the code in the editable array

        script : string
            The code of the script to be set in
        '''
        code = self._cleanLines(code)

        self.editable_scripts[index] = str(code)

    def _cleanLines(self,text):
        '''
        Remove all the surplus of blank lines
        at the start and then end of the script

        Parameters
        ----------
        text : string
            The code of the script to be set in
        '''
        text_array  = text.split('\n')
        start       = 0
        start_found = False
        end         = 0

        for i, line in enumerate(text_array):
            if not start_found:
                if line == '':
                    start = i
                else:
                    start_found = True
            else:
                if not line == '':
                    end = i

        return self._concatenateText([text_array[start:end+1]])

    def preprocessScript(self, index):
        '''
        Read from the scripts to produce a dictionary
        with all the information that can be set if it
        is found.

        Parameters
        ----------
        text : string
            The formated text to be formater

        Returns
        ------- 
        text : string
            The formated text to returned to the text importer
        '''
        code_array = self._parseCode(self.editable_scripts[index])
        meta_array = self._parseMeta(code_array)

        return code_array, meta_array

    def _parseCode(self, code):
        '''
        This function will break down the code into smaller 
        parts to allow interpretation of the failed sequence
        as well as a meaningfull understanding of the progress.

        Parameters
        ----------
        text : string
            The text to be formater
        '''
        temp_code_array = []
        indentation     = False
        comment_bool    = False
        code_lines      = code.split('\n') 

        for line in code_lines:
            if line == '' or line[0] == '#':
                pass
            elif line[0] == "'" or line[0] == '"':
                comment_bool = not comment_bool

            elif line[0].isspace() and not line == '' and not comment_bool:
                if not indentation:
                    indentation = not indentation
                    temp = temp_code_array[-1]
                    temp.append(line)
                else:
                    temp.append(line)
            elif not comment_bool:
                if indentation:
                    indentation = not indentation
                temp_code_array.append([line])

        code_array = []
        for element in temp_code_array:
            if len(element) > 1:
                code_string = ''
                for sub_element in element:
                    code_string += sub_element + '\n'
                code_array.append(code_string)
            else:
                code_array.append(element[0])

        return code_array

    def _parseMeta(self, code_array):
        '''
        This function will try to identify the individual 
        function parts to provide nice insight on what is 
        being processed at the moment.
        '''
        meta_array = []
        for element in code_array:
            if len(element.split('for ')) > 1:
                meta_array.append(
                    "'for' loop over "+str(element.split(' in ')[1].split(':')[0]))
            elif '(' in element and ')' in element:
                meta_array.append(
                    "'function' "+element.split('(')[0]+' with the parameters ('+''.join(element.split('(')[1].split(')')[0])[0:30]+')')
            else:
                 meta_array.append(element[0:40])

        return meta_array

    def synthesizeDataScript(self, container):
        '''
        prepare the python script part that will
        manage the fit parameter part

        Parameters
        ----------
        container : misc items in dictionary
            The text to be formater
        '''         
        #find area to edit
        text = self.editable_scripts[0]
        text_array = text.split("\n")

        for i,element in enumerate(text_array):
            if "metadata_class.add_metadata('Selected foils'" in element:
                text_array[i] = element.split(".current_data.metadata_class.add_metadata(")[0]+".current_data.metadata_class.add_metadata('Selected foils', value = '"+str(container['checked'])+"' , logical_type = 'int_array', unit = '-')"
                break

        #find strings
        self.setEditable(0, self._concatenateText([text_array]))

    def synthesizeFitScript(self, container):
        '''
        prepare the python script part that will
        manage the fit parameter part

        Parameters
        ----------
        container : misc items in dictionary
            The text to be formater
        '''         
        python_string_init = ""

        #set the foils
        python_string_init += "\n#Set the foils (edit in GUI)\n"
        python_string_init += "foils_in_echo = []\n"
        for i,item in enumerate(container['foils_in_echo']):
            python_string_init += "foils_in_echo.append("+str(item)+")\n"

        #set the selected
        python_string_init += "\n#Set the selected (edit in GUI)\n"
        if not len(container['selected']) == 0:
            python_string_init += "Selected = [ "
            for i, item in enumerate(container['selected']):
                try:
                    python_string_init += str(float(item))+ ", "
                except:
                    python_string_init += "'"+str(item)+ "', "

            python_string_init = python_string_init[:-2]
            python_string_init += "]\n"
        else:
            python_string_init += "Selected = []\n"

        #set the time channels
        python_string_init += "\n#Set the time channels to use(edit in GUI)\n"
        python_string_init += "TimeChannels = "+str(container['time_channels'])+"\n"

        #set the background
        python_string_init += "\n#Set the background (edit in GUI)\n"
        python_string_init += "Background = "+container['Background']+"\n"

        #set the reference
        python_string_init += "\n#Set the reference (edit in GUI)\n"
        python_string_init += "Reference = "+container['Reference']+"\n"

        #set the instrument
        python_string_init += "\n#Instrument (edit in GUI)\n"
        python_string_init += "instrument = '"+container['Instrument']+"'\n"

        #set the detector
        python_string_init += "\n#Detector(edit in GUI)\n"
        python_string_init += "detector = "+container['detector']+"\n"

        #set the exposure setting
        python_string_init += "\n#Use the high exposure setting (edit in GUI)\n"
        python_string_init += "exposure = "+container['exposure']+"\n"

        #find area to edit
        text = self.editable_scripts[1]
        text_array = text.split("\n")

        edit_start = 0
        edit_end = len(text_array)

        for i,line in enumerate(text_array):
            if "self.env" in line:
                edit_start = i
            if ".fit.set_parameter( " in line:
                edit_end = i
                break

        text_array = self._concatenateText([
            text_array[0:edit_start+1],
            python_string_init.split("\n"),
            text_array[edit_end-1:]])

        self.setEditable(1, text_array)

    def synthesizePhaseScript(self, container):
        '''
        prepare the python script part that will
        manage the phase parameter part

        Parameters
        ----------
        container : misc items in dictionary
            The text to be formater
        '''         
        #find area to edit
        text = self.editable_scripts[2]
        text_array = text.split("\n")

        for i,element in enumerate(text_array):
            if "mask.setMask(" in element:
                text_array[i] = element.split(".mask.setMask(")[0]+".mask.setMask('"+container['mask']+"')"
                break

        #find strings
        self.setEditable(2, self._concatenateText([text_array]))

    def synthesizeReductionScript(self, container):
        '''
        prepare the python script part that will
        manage the phase parameter part

        Parameters
        ----------
        container : misc items in dictionary
            The text to be formater
        '''         
        #find area to edit
        text = self.editable_scripts[3]
        text_array = text.split("\n")

        for i,element in enumerate(text_array):
            if "mask.setMask(" in element:
                text_array[i] = element.split(".mask.setMask(")[0]+".mask.setMask('"+container['mask']+"')"
                break

        #find strings
        self.setEditable(3, self._concatenateText([text_array]))

    def _concatenateText(self, element_arrays):
        '''
        Sticks the array together into a single 
        string item
        '''
        output = ''
        for element in element_arrays:
            for line in element:
                output += line + "\n"

        return output

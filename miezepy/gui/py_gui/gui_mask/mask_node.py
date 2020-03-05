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

from PyQt5 import QtWidgets, QtGui, QtCore

from simpleplot.models.session_node         import SessionNode
from simpleplot.models.parameter_class      import ParameterHandler
from simpleplot.models.widget_constructors  import comboBoxConstructor

from .parameter_handlers import RectangleHandler
from .parameter_handlers import TriangleHandler
from .parameter_handlers import PieHandler
from .parameter_handlers import EllipseHandler
 

class MaskElementNode(ParameterHandler):
    def __init__(self,name ='Mask Element', parent = None, value = 'arc'):
        '''
        This node will be the main node for a
        mask element and will contain by default a 
        parameter node and if it becomes a combination
        the child node
        '''
        SessionNode.__init__(self, name, parent)
        self._value = value
        self.handlers = {}

    def data(self, column):
        if column == 0: return self._name
        elif column == 1: return self._value
            
    def setData(self, column, value):
        if column == 0: 
            self._name = value
        elif column == 1: 
            self._value = value
        
    def flags(self, index):
        if index.column() in [0,1]: 
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable
        else:
            return QtCore.Qt.ItemIsEnabled

    def createWidget(self, parent, index):
        '''
        create the widget for the delegate
        '''
        return self._constructor.create(parent,index =  index)

    def setEditorData(self, editor, index):
        '''
        set the data of the editor
        '''
        self._constructor.setEditorData(editor)

    def retrieveData(self, editor, index):
        '''
        set the data of the editor
        '''
        return self._constructor.retrieveData(editor)
    
    def updateValue(self, value):
        '''
        The values here will be set manually
        '''
        if value in self.kwargs['choices']:
            self._value = value
            self._model.dataChanged.emit(self.index(),self.index())

    def setParameters(self, parameter_dict):
        '''
        Set the parameters of the node through 
        the interfaces
        '''
        handler = self.handlers[self._value]
        self.load(parameter_dict)
        # for key in parameter_dict.keys():
        #     self.load(parameter_dict[key])
        #     if key != 'Type' and key != 'Name':
        #         if isinstance(parameter_dict[key], list):
        #             handler[key] = parameter_dict[key][-1]
        #         else:
        #             handler[key] = [
        #                 parameter_dict[key][subkey][-1] 
        #                 for subkey in parameter_dict[key].keys()]

    def synthesize(self):
        '''
        This will go through parameters and send out
        the dictionary
        '''
        output = self.save()
        output['Name'] = self._name
        output['Type'] = self._value

        return output


class MaskNode(MaskElementNode):
    def __init__(self,name ='Mask Element', parent = None):
        '''
        This node will be the main node for a
        mask element and will contain by default a 
        parameter node and if it becomes a combination
        the child node
        '''
        MaskElementNode.__init__(self,name = name, parent=parent)
        self.kwargs = {}
        self.kwargs['choices'] = ['Rectangle','Pie','Triangle','Ellipse']
        self.kwargs['method'] = self.typeChanged
        self._value = 'Rectangle'
        self._constructor = comboBoxConstructor(self)
        self._buildParameterHandlers()

    def _buildParameterHandlers(self):
        '''
        Define all the handlers that can be put in. 
        The fact of not destroying them in 
        case the user changes assures the safeguard
        of the data loaded in it.
        '''
        self.handlers = {}
        self.handlers['Rectangle']  = RectangleHandler()
        self.handlers['Triangle']   = TriangleHandler()
        self.handlers['Pie']        = PieHandler()
        self.handlers['Ellipse']    = EllipseHandler()

    def typeChanged(self):
        '''
        This machinery is developed in order to remove the 
        previous handler and insert the new one
        '''
        self._model.removeRows(0,len(self._children), self)
        self.items = self.handlers[self._value].items
        self._model.insertRows(
            0,len(self.handlers[self._value]._children), 
            self.handlers[self._value]._children[::-1],self)
        self.freezOrder()
        self.setCurrentTags('2D')

    def flags(self, index):
        if index.column() == 1: 
            return QtCore.Qt.ItemIsEnabled  | QtCore.Qt.ItemIsEditable
        else:
            return QtCore.Qt.ItemIsEnabled 

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
from .parameter_handlers import ArcHandler
from .parameter_handlers import RadialHandler
from .parameter_handlers import LinearHandler
 
class MaskNode(SessionNode):
    def __init__(self, name = 'None', parent = None, value = 'arc'):
        SessionNode.__init__(self, name, parent)
        self._value = value

    def data(self, column):
        if column is 0: return self._name
        elif column is 1: return self._value
            
    def setData(self, column, value):
        if column is 1: 
            self._value = value
        
    def flags(self, index):
        if index.column() is 1: 
            return QtCore.Qt.ItemIsEnabled  | QtCore.Qt.ItemIsEditable
        else:
            return QtCore.Qt.ItemIsEnabled 

class MaskElementNode(MaskNode):
    def __init__(self,name ='Mask Element', parent = None):
        '''
        This node will be the main node for a
        mask element and will contain by default a 
        parameter node and if it becomes a combination
        the child node
        '''
        MaskNode.__init__(self,name, parent)
        self.handlers = {}

    def createWidget(self, parent, index):
        '''
        create the widget for the delegate
        '''
        return self._constructor.create(parent,index =  index)

    def setEditorData(self, editor):
        '''
        set the data of the editor
        '''
        self._constructor.setEditorData(editor)

    def retrieveData(self, editor):
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
        for key in parameter_dict.keys():
            if key is not 'Name' and key is not 'child':
                handler[key] = parameter_dict[key]

        if 'composition' in self._value and 'child' in parameter_dict.keys():
            self._motif.setParameters(parameter_dict['child'])

    def synthesize(self):
        '''
        This will go through parameters and send out
        the dictionary
        '''
        output = {}
        output['Name'] = self._value

        parameter_idx = None
        child_idx = None
        for i,child in enumerate(self._children):
            if child._name == 'Parameters':
                parameter_idx = i
            if child._name == 'Child':
                child_idx = i

        for child in self.child(parameter_idx)._children:
            output[child._name] = child.getValue()

        if not child_idx == None:
            output['child'] = {'Name':self.child(child_idx)._value}
            for child in self.child(child_idx).child(0)._children:
                output['child'][child._name] = child.getValue()

        return output

    def flags(self, index):
        if index.column() is 1: 
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable
        else:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

class MaskMajorNode(MaskElementNode):

    def __init__(self,name ='Mask Element', parent = None):
        '''
        This node will be the main node for a
        mask element and will contain by default a 
        parameter node and if it becomes a combination
        the child node
        '''
        MaskElementNode.__init__(self,name = name, parent=parent)
        self.kwargs = {}
        self.kwargs['choices'] = [
            'Rectangle','Arc','Triangle',
            'Linear composition','Radial composition']
        self.kwargs['method'] = self.typeChanged
        self._value = 'Rectangle'
        self._composition = False
        
        self._constructor = comboBoxConstructor(self)
        self._buildParameterHandlers()
        self.addChild(self.handlers[self._value])

    def _buildParameterHandlers(self):
        '''
        Define all the handlers that can be put in. 
        The fact of not destroying them in 
        case the user changes assures the safeguard
        of the data loaded in it.
        '''
        self.handlers = {}
        self.handlers['Rectangle']          = RectangleHandler()
        self.handlers['Triangle']           = TriangleHandler()
        self.handlers['Arc']                = ArcHandler()
        self.handlers['Radial composition'] = RadialHandler()
        self.handlers['Linear composition'] = LinearHandler()

        self._motif = MaskMinorNode('Child')

    def typeChanged(self):
        '''
        This machinery is developed in order to remove the 
        previous handler and insert the new one
        '''
        self._model._update = False
        if not self.childCount() == 0:
            self._model.removeRows(0,self.childCount(), self)

        self._model._update = True
        if 'composition' in self._value: 
            self._model.insertRows(
                0,2, [self._motif, self.handlers[self._value]],self)
            self._composition = True

        else:
            self._model.insertRows(
                0,1, [self.handlers[self._value]],self)

class MaskMinorNode(MaskElementNode):
    def __init__(self,name ='Mask Element', parent = None):
        '''
        This node will be the main node for a
        mask element and will contain by default a 
        parameter node and if it becomes a combination
        the child node
        '''
        MaskElementNode.__init__(self,name = name, parent=parent)
        self.kwargs = {}
        self.kwargs['choices'] = ['Rectangle','Arc','Triangle']
        self.kwargs['method'] = self.typeChanged
        self._value = 'Rectangle'
        
        self._constructor = comboBoxConstructor(self)
        self._buildParameterHandlers()
        self.addChild(self.handlers[self._value])

    def _buildParameterHandlers(self):
        '''
        Define all the handlers that can be put in. 
        The fact of not destroying them in 
        case the user changes assures the safeguard
        of the data loaded in it.
        '''
        self.handlers = {}
        self.handlers['Rectangle']          = RectangleHandler()
        self.handlers['Triangle']           = TriangleHandler()
        self.handlers['Arc']                = ArcHandler()

    def typeChanged(self):
        '''
        This machinery is developed in order to remove the 
        previous handler and insert the new one
        '''
        self._model.removeRows(0,1, self)

        self._model.insertRows(
            0,1, [self.handlers[self._value]],self)

    def flags(self, index):
        if index.column() is 1: 
            return QtCore.Qt.ItemIsEnabled  | QtCore.Qt.ItemIsEditable
        else:
            return QtCore.Qt.ItemIsEnabled 
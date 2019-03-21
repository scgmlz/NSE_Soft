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

from PyQt5 import QtCore, QtGui
import traceback, sys
from functools import partial


class WorkerPool(QtCore.QObject):
    '''
    In this instance we will manage the workers
    and tell them to complete a task when done
    an then move on to the next task
    '''
    finished    = QtCore.pyqtSignal()

    def __init__(self, processes):
        super(WorkerPool, self).__init__()
        self.workers    = []
        self.processes  = processes
        self._createThreads()

    def _createThreads(self):
        '''
        create here the threads that will be used
        '''
        self.threads = [QtCore.QThread() for i in range(self.processes)]
        self.mainThread = QtCore.QThread.currentThread()

    def addWorker(self, worker):
        '''
        add a worker to the list
        '''
        self.workers.append(worker)

    def preparePool(self):
        '''
        setup the slot modifications about
        the workers and there state
        '''
        self.idx        = 0
        self.states     = [False for i in self.workers]
        self.results    = [None for i in self.workers]
        self.startPool()
        
    def setState(self, worker_idx):
        '''
        set the completion state of a worker to True
        '''
        
        self.results[worker_idx]            = self.workers[worker_idx].result
        self.states[worker_idx]             = True
        self.subset[worker_idx-self.idx]    = True

        print('deleting thread: ', worker_idx-self.idx)
        self.threads[worker_idx-self.idx].quit()
        self.threads[worker_idx-self.idx].deleteLater()


        self.checkStates()

    @QtCore.pyqtSlot()
    def checkStates(self):
        '''
        Will check all states of the workers and then 
        report back if completeted
        '''
        if all(self.states):
            self.finished.emit()
            print("FINISHED")
        elif not all(self.states) and all(self.subset):
            self.idx += self.processes
            self._createThreads()
            self.startPool()

    def startPool(self):
        '''
        start a pool of subelements
        '''
        self.subset = []
        idx = int(self.idx)
        limit = self.idx + self.processes

        while idx < limit and idx < len(self.workers):
            print('IDX_0 :', idx)
            self.subset.append(False)
            idx += 1

        idx = int(self.idx)
        while idx < limit and idx < len(self.workers):
            print('IDX_1 :', idx, ' thread ', idx - self.idx)
            self.workers[idx].moveToThread(self.threads[idx - self.idx])
            self.workers[idx].finished.connect(partial(self.setState, idx))
            self.threads[idx - self.idx].started.connect(self.workers[idx].run)
            self.threads[idx - self.idx].start()
            idx += 1
        
class Worker(QtCore.QObject):
    '''
    This thread will be the worker for the given mask 
    section
    '''
    finished = QtCore.pyqtSignal()
    intReady = QtCore.pyqtSignal(int)

    def __init__(self,function, *args, **kwargs):
        super(Worker, self).__init__()
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs

    @QtCore.pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed self.args, self.kwargs.
        '''
        self.result = self.function(*self.args, **self.kwargs)
        self.finished.emit()

        # try:
        #     self.result = self.function(*self.args, **self.kwargs)#,
        #         # status=self.signals.status,
        #         # progress=self.signals.progress)
        # except:
        #     pass
        #     # traceback.print_exc()
        #     # exctype, value = sys.exc_info()[:2],
        #     # self.signals.error.emit((exctype, value, traceback.format_exc()))
        # finally:
        #     self.finished.emit()  # Done


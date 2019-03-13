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

import multiprocessing as mp
from time import sleep

class WorkerPool():
    '''
    In this instance we will manage the workers
    and tell them to complete a task when done
    an then move on to the next task
    '''

    def __init__(self, processes):
        self.workers    = []
        self.processes  = processes
        self.queue      = mp.Queue()
        self.manager    = mp.Manager()
        self.result_dict= self.manager.dict()

    def addWorker(self, worker):
        '''
        add a worker to the list
        '''
        self.workers.append(mp.Process(target = worker[0], args = worker[1:] + [self.result_dict]))

    def startPool(self):
        '''
        start a pool of subelements
        '''
        idx = 0
        while idx < len(self.workers):
            limit   = int(idx + self.processes)
            temp    = []

            while idx < limit and idx < len(self.workers):
                self.workers[idx].start()
                temp.append(idx)
                idx += 1
            
            for i in temp:
                self.workers[i].join()

        return dict(self.result_dict)
            
            

        
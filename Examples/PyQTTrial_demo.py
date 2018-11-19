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
#   Alexander Schober <alexander.schober@mac.com>
#
# *****************************************************************************

import os
from mieze_python.Main import Manager as NSE
from pprint import pprint
import sys 

 
def main():
 
    tool = NSE()
    vertical_env = tool.new_environment(title = 'vertical MIEZE', select = 'MIEZE')
    vertical_env.io.load_MIEZE_TOF('trial_vis_2.txt')
    vertical_env.mask.select_template(key = 'Pre_SkX_peak_SkXCon')
    foils_in_echo = []
    for i in range(5):
        foils_in_echo.append([1,1,1,1,1,1])
    foils_in_echo.append([1,1,0,1,1,1])
    foils_in_echo.append([1,1,0,1,1,1])
    foils_in_echo.append([0,0,0,0,1,0])

    #set the values to be processed as data
    Select = [28.40, 28.60, 28.80, 28.95, 29.05, 29.15, 29.25, 29.35, 29.45, 29.60, 29.75]

    #set the reference value
    Reference = [28.6,0]

    #set the background
    Background = None

    vertical_env.fit.set_parameter( name = 'Select',        value = Select       )
    vertical_env.fit.set_parameter( name = 'Reference',     value = Reference    )
    vertical_env.fit.set_parameter( name = 'Background',    value = Background   )
    vertical_env.fit.set_parameter( name = 'foils_in_echo', value = foils_in_echo)

    vertical_env.process.calculate_echo()
    vertical_env.process.remove_foils()
    vertical_env.process.calculate_shift()
    vertical_env.mask.select_template(key = 'SkX_peak_SkXCon')

    tool.launch_sp(vertical_env)


 
if __name__ == '__main__':
    main()


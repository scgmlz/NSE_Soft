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

def generateSingleName(title, title_list):
    '''
    This method tries to increase an integer at the end
    of name if it is present in title_list and then
    returns the found element.

    Parameters
    ----------
    title : str
        The string we are trying to set

    title_list: [str]
        The list of strings already present we are trying to avoid

    Returns
    -------
    found_str : str
        The found string not in the list that we can use
    '''
    #check if the title is in the list (if yes return)
    if not title in title_list:
        return title

    #initialise
    present = True
    index   = 0
    if title.split('_')[-1].isdigit():
        index = int(title.split('_')[-1])
        title = '_'.join(title.split('_')[0:-1])
    else:
        index = 0

    #loop
    while present:
        if title+'_'+str(index) in title_list:
            index += 1
        else:
            present = False

    return title+'_'+str(index)


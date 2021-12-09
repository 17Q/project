# -*- coding: utf-8 -*-

'''
    Patriot Add-on

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


import os
from resources.lib.modules import control, log_utils


def get():
    try:
        changelogfile = os.path.join(control.addonPath, 'changelog.txt')
        head = 'Patriot  -- Changelog --'
        control.textViewer(file=changelogfile, heading=head)
    except:
        control.infoDialog('Error opening changelog', sound=True)
        log_utils.log('changeloglog_view_fail', 1)


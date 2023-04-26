# -*- coding: utf-8 -*-
import sys
from xbmc import executebuiltin

executebuiltin('RunPlugin(%s)' % sys.listitem.getProperty('david_options_params'))

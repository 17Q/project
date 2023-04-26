# -*- coding: utf-8 -*-
"""
	Fenomscrapers Module
"""

from qscrapers.modules.control import addonPath, addonVersion, joinPath
from qscrapers.windows.textviewer import TextViewerXML


def get(file):
	qscrapers_path = addonPath()
	qscrapers_version = addonVersion()
	helpFile = joinPath(qscrapers_path, 'lib', 'qscrapers', 'help', file + '.txt')
	r = open(helpFile, 'r', encoding='utf-8', errors='ignore')
	text = r.read()
	r.close()
	heading = '[B]QScrapers -  v%s - %s[/B]' % (qscrapers_version, file)
	windows = TextViewerXML('textviewer.xml', qscrapers_path, heading=heading, text=text)
	windows.run()
	del windows
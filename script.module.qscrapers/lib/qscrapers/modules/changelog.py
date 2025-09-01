# -*- coding: utf-8 -*-
"""
	Qscrapers Module
"""

from qscrapers.modules.control import addonPath, addonVersion, joinPath
from qscrapers.windows.textviewer import TextViewerXML


def get():
	qscrapers_path = addonPath()
	qscrapers_version = addonVersion()
	changelogfile = joinPath(qscrapers_path, 'changelog.txt')
	r = open(changelogfile, 'r', encoding='utf-8', errors='ignore')
	text = r.read()
	r.close()
	heading = '[B]QScrapers -  v%s - ChangeLog[/B]' % qscrapers_version
	windows = TextViewerXML('textviewer.xml', qscrapers_path, heading=heading, text=text)
	windows.run()
	del windows
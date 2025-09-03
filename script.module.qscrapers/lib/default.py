# -*- coding: utf-8 -*-
"""
	Qscrapers Module
"""

from sys import argv
from urllib.parse import parse_qsl
from qscrapers import sources_qscrapers
from qscrapers.modules import control

params = dict(parse_qsl(argv[2].replace('?', '')))
action = params.get('action')

if action is None:
	control.openSettings('0.0', 'script.module.qscrapers')

if action == "QScrapersSettings":
	control.openSettings('0.0', 'script.module.qscrapers')

elif action == 'ShowChangelog':
	from qscrapers.modules import changelog
	changelog.get()

elif action == 'ShowHelp':
	from qscrapers.help import help
	help.get(params.get('name'))

elif action == "Defaults":
	control.setProviderDefaults()

elif action == "toggleAll":
	sourceList = []
	sourceList = sources_qscrapers.all_providers
	for i in sourceList:
		source_setting = 'provider.' + i
		control.setSetting(source_setting, params['setting'])

elif action == "toggleAllHosters":
	sourceList = []
	sourceList = sources_qscrapers.hoster_providers
	for i in sourceList:
		source_setting = 'provider.' + i
		control.setSetting(source_setting, params['setting'])

elif action == "toggleAllTorrent":
	sourceList = []
	sourceList = sources_qscrapers.torrent_providers
	for i in sourceList:
		source_setting = 'provider.' + i
		control.setSetting(source_setting, params['setting'])

elif action == "toggleAllPackTorrent":
	control.execute('RunPlugin(plugin://script.module.qscrapers/?action=toggleAllTorrent&amp;setting=false)')
	control.sleep(500)
	sourceList = []
	from qscrapers import pack_sources
	sourceList = pack_sources()
	for i in sourceList:
		source_setting = 'provider.' + i
		control.setSetting(source_setting, params['setting'])

elif action == 'cleanSettings':
	control.clean_settings()

elif action == 'undesirablesSelect':
	from qscrapers.modules.undesirables import undesirablesSelect
	undesirablesSelect()

elif action == 'undesirablesInput':
	from qscrapers.modules.undesirables import undesirablesInput
	undesirablesInput()

elif action == 'undesirablesUserRemove':
	from qscrapers.modules.undesirables import undesirablesUserRemove
	undesirablesUserRemove()

elif action == 'undesirablesUserRemoveAll':
	from qscrapers.modules.undesirables import undesirablesUserRemoveAll
	undesirablesUserRemoveAll()

elif action == 'tools_clearLogFile':
	from qscrapers.modules import log_utils
	cleared = log_utils.clear_logFile()
	if cleared == 'canceled': pass
	elif cleared: control.notification(message='QScrapers Log File Successfully Cleared')
	else: control.notification(message='Error clearing QScrapers Log File, see kodi.log for more info')

elif action == 'tools_viewLogFile':
	from qscrapers.modules import log_utils
	log_utils.view_LogFile(params.get('name'))

elif action == 'tools_viewTorrentStats':
	from qscrapers.modules import log_utils
	log_utils.view_TorrentStats(params.get('name'))

elif action == 'tools_uploadLogFile':
	from qscrapers.modules import log_utils
	log_utils.upload_LogFile()

elif action == 'plexAuth':
	from qscrapers.modules import plex
	plex.Plex().auth()

elif action == 'plexRevoke':
	from qscrapers.modules import plex
	plex.Plex().revoke()

elif action == 'plexSelectShare':
	from qscrapers.modules import plex
	plex.Plex().get_plexshare_resource()

elif action == 'plexSeeShare':
	from qscrapers.modules import plex
	plex.Plex().see_active_shares()

elif action == 'ShowOKDialog':
	control.okDialog(params.get('title', 'default'), int(params.get('message', '')))

elif action == 'TestProwlarrConnection':
	from qscrapers.modules.prowlarr import Prowlarr
	prowlarr = Prowlarr()
	prowlarr.test()

elif action == 'ProwlarrIndexers':
	from qscrapers.modules.prowlarr import Prowlarr
	prowlarr = Prowlarr()
	prowlarr.get_indexers()

elif action == 'mediafusionAuth':
	from qscrapers.modules.mediafusion import MediaFusion
	mediafusion = MediaFusion()
	mediafusion.auth()

elif action == 'mediafusionReset':
	from qscrapers.modules.mediafusion import MediaFusion
	mediafusion = MediaFusion()
	mediafusion.clear()
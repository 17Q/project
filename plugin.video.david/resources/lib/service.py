# -*- coding: utf-8 -*-
from modules import service_functions
from modules.kodi_utils import Thread, get_property, set_property, xbmc_monitor, make_settings_dict, get_setting, logger, local_string as ls

david_str = ls(32036).upper()
OnNotificationActions = service_functions.OnNotificationActions()

class DavidMonitor(xbmc_monitor):
	def __init__ (self):
		xbmc_monitor.__init__(self)
		self.startUpServices()
	
	def startUpServices(self):
		set_property('plugin.video.david.service_pause_time', '20')
		try: service_functions.InitializeDatabases().run()
		except: pass
		Thread(target=service_functions.DatabaseMaintenance().run).start()
		try: service_functions.CheckSettingsFile().run()
		except: pass
		try: service_functions.SetStartingWindowProperties().run()
		except: pass
		try: service_functions.CheckUpdateActions().run()
		except: pass
		try: service_functions.ReuseLanguageInvokerCheck().run()
		except: pass
		Thread(target=service_functions.TraktMonitor().run).start()
		try: service_functions.ClearSubs().run()
		except: pass
		try: service_functions.AutoRun().run()
		except: pass
		set_property('plugin.video.david.service_finished', 'true')

	def onSettingsChanged(self):
		if get_property('david_pause_onSettingsChanged') != 'true': make_settings_dict()

	def onNotification(self, sender, method, data):
		OnNotificationActions.run(sender, method, data)

logger(david_str, 'Main Monitor Service Starting')
logger(david_str, 'Settings Monitor Service Starting')
DavidMonitor().waitForAbort()
logger(david_str, 'Settings Monitor Service Finished')
logger(david_str, 'Main Monitor Service Finished')
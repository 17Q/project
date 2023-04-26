# -*- coding: utf-8 -*-
import time
import datetime
import xml.etree.ElementTree as ET
from caches import check_databases, clean_databases
from apis.trakt_api import trakt_sync_activities
from modules import kodi_utils, settings
from modules.utils import string_to_float

logger, notification, json, execute_builtin, confirm_dialog = kodi_utils.logger, kodi_utils.notification, kodi_utils.json, kodi_utils.execute_builtin, kodi_utils.confirm_dialog
ls, monitor, path_exists, translate_path, is_playing = kodi_utils.local_string, kodi_utils.monitor, kodi_utils.path_exists, kodi_utils.translate_path, kodi_utils.player.isPlaying
get_property, set_property, clear_property, get_visibility = kodi_utils.get_property, kodi_utils.set_property, kodi_utils.clear_property, kodi_utils.get_visibility
make_directories, widget_refresh, list_dirs, delete_file = kodi_utils.make_directories, kodi_utils.widget_refresh, kodi_utils.list_dirs, kodi_utils.delete_file
get_setting, set_setting, make_settings_dict = kodi_utils.get_setting, kodi_utils.set_setting, kodi_utils.make_settings_dict
pause_settings_change, unpause_settings_change = kodi_utils.pause_settings_change, kodi_utils.unpause_settings_change
set_view_properties, set_highlight_property = kodi_utils.set_view_properties, kodi_utils.set_highlight_property
disable_enable_addon, update_local_addons = kodi_utils.disable_enable_addon, kodi_utils.update_local_addons
david_str = ls(32036).upper()

class InitializeDatabases:
	def run(self):
		logger(david_str, 'InitializeDatabases Service Starting')
		check_databases()
		return logger(david_str, 'InitializeDatabases Service Finished')

class DatabaseMaintenance:
	def run(self):
		logger(david_str, 'Database Maintenance Service Starting')
		time = datetime.datetime.now()
		current_time = self._get_timestamp(time)
		due_clean = int(get_setting('database.maintenance.due', '0'))
		if due_clean == 0:
			next_clean = str(int(self._get_timestamp(time + datetime.timedelta(days=3))))
			set_setting('database.maintenance.due', next_clean)
			return logger(david_str, 'Database Maintenance Service First Run - Skipping')
		if current_time >= due_clean:
			clean_databases(current_time, database_check=False, silent=True)
			next_clean = str(int(self._get_timestamp(time + datetime.timedelta(days=3))))
			set_setting('database.maintenance.due', next_clean)
			return logger(david_str, 'Database Maintenance Service Finished')
		else: return logger(david_str, 'Database Maintenance Service Finished - Not Run')

	def _get_timestamp(self, date_time):
		return int(time.mktime(date_time.timetuple()))

class CheckSettingsFile:
	def run(self):
		logger(david_str, 'CheckSettingsFile Service Starting')
		clear_property('david_settings')
		profile_dir = kodi_utils.userdata_path
		if not path_exists(profile_dir): make_directories(profile_dir)
		settings_xml = translate_path('special://profile/addon_data/plugin.video.david/settings.xml')
		if not path_exists(settings_xml):
			__addon__ = kodi_utils.addon()
			addon_version = __addon__.getAddonInfo('version')
			set_setting('version_number', addon_version)
			monitor.waitForAbort(0.5)
		make_settings_dict()
		set_property('david_kodi_menu_cache', get_setting('kodi_menu_cache'))
		return logger(david_str, 'CheckSettingsFile Service Finished')

class CheckUpdateActions:
	def run(self):
		logger(david_str, 'CheckUpdateActions Service Starting')
		addon_version, settings_version =  self.remove_alpha(kodi_utils.addon().getAddonInfo('version')), self.remove_alpha(get_setting('version_number'))
		if addon_version != settings_version:
			set_setting('version_number', addon_version)
			logger(david_str, 'CheckUpdateActions Running Update Actions....')
			self.update_action()
		return logger(david_str, 'CheckUpdateActions Service Finished')

	def update_action(self):
		''' Put code that needs to run once on update here'''
		return


	def remove_alpha(self, string):
		return ''.join(c for c in string if (c.isdigit() or c =='.'))

class TraktMonitor:
	def run(self):
		logger(david_str, 'TraktMonitor Service Starting')
		trakt_service_string = 'TraktMonitor Service Update %s - %s - '
		update_string = 'Next Update in %s minutes...'
		if not get_property('david_traktmonitor_first_run_complete') == 'true': set_property('david_traktmonitor_first_run_complete', 'true')
		while not monitor.abortRequested():
			try:
				while is_playing() or get_visibility('Container().isUpdating') or get_property('david_pause_services') == 'true': monitor.waitForAbort(10)
				value, interval = settings.trakt_sync_interval()
				next_update_string = update_string % value
				status = trakt_sync_activities()
				if status == 'success':
					logger(david_str, trakt_service_string % ('Success', 'Trakt Update Performed'))
					if settings.trakt_sync_refresh_widgets():
						widget_refresh()
						logger(david_str, trakt_service_string % ('Widgets Refresh', 'Setting Activated. Widget Refresh Performed'))
					else: logger(david_str, trakt_service_string % ('Widgets Refresh', 'Setting Disabled. Skipping Widget Refresh'))
				elif status == 'no account': logger(david_str, trakt_service_string % ('Aborted. No Trakt Account Active', next_update_string))
				elif status == 'failed': logger(david_str, trakt_service_string % ('Failed. Error from Trakt', next_update_string))
				else: logger(david_str, trakt_service_string % ('Success. No Changes Needed', next_update_string))# 'not needed'
					
			except Exception as e: logger(david_str, trakt_service_string % ('Failed', 'The following Error Occured: %s' % str(e)))
			set_property('david_startup_trakt_sync_complete', 'true')
			monitor.waitForAbort(interval)
		return logger(david_str, 'TraktMonitor Service Finished')

class ClearSubs:
	def run(self):
		logger(david_str, 'Clear Subtitles Service Starting')
		sub_formats = ('.srt', '.ssa', '.smi', '.sub', '.idx', '.nfo')
		subtitle_path = 'special://temp/%s'
		files = list_dirs(translate_path('special://temp/'))[1]
		for i in files:
			if i.startswith('DAVIDSubs_') or i.endswith(sub_formats): delete_file(translate_path(subtitle_path % i))
		return logger(david_str, 'Clear Subtitles Service Finished')

class SetStartingWindowProperties:
	def run(self):
		logger(david_str, 'SetStartingWindowProperties Service Starting')
		set_view_properties()
		set_highlight_property(get_setting('david.highlight', 'dodgerblue'))
		return logger(david_str, 'SetStartingWindowProperties Service Finished')

class AutoRun:
	def run(self):
		logger(david_str, 'AutoRun Service Starting')
		if settings.auto_start_david(): execute_builtin('RunAddon(plugin.video.david)')
		return logger(david_str, 'AutoRun Service Finished')

class ReuseLanguageInvokerCheck:
	def run(self):
		logger(david_str, 'ReuseLanguageInvokerCheck Service Starting')
		addon_xml = translate_path('special://home/addons/plugin.video.david/addon.xml')
		tree = ET.parse(addon_xml)
		root = tree.getroot()
		current_addon_setting = get_setting('reuse_language_invoker', 'true')
		refresh, text = True, '%s\n%s' % (ls(33021), ls(33020))
		for item in root.iter('reuselanguageinvoker'):
			if item.text == current_addon_setting: refresh = False; break
			item.text = current_addon_setting
			tree.write(addon_xml)
			break
		if refresh and confirm_dialog(text=text):
			update_local_addons()
			disable_enable_addon()
		return logger(david_str, 'ReuseLanguageInvokerCheck Service Finished')

class OnNotificationActions:
	def run(self, sender, method, data):
		if sender == 'xbmc':
			if method in ('GUI.OnScreensaverActivated', 'System.OnSleep'): set_property('david_pause_services', 'true')
			elif method in ('GUI.OnScreensaverDeactivated', 'System.OnWake'): clear_property('david_pause_services')

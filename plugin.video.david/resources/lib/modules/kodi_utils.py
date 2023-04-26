# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcplugin, xbmcvfs
from xbmcaddon import Addon
import sys
import json
import requests
import _strptime
import sqlite3 as database
from threading import Thread, activeCount
from urllib.parse import unquote, unquote_plus, urlencode, quote, parse_qsl, urlparse
from modules import icons

__addon__ = Addon(id='plugin.video.david')
player, xbmc_player, numeric_input, xbmc_monitor, translatePath = xbmc.Player(), xbmc.Player, xbmcgui.INPUT_NUMERIC, xbmc.Monitor, xbmcvfs.translatePath
get_infolabel, get_visibility, execute_JSON, window_xml_dialog = xbmc.getInfoLabel, xbmc.getCondVisibility, xbmc.executeJSONRPC, xbmcgui.WindowXMLDialog
monitor, window, dialog, progressDialog, progressDialogBG = xbmc.Monitor(), xbmcgui.Window(10000), xbmcgui.Dialog(), xbmcgui.DialogProgress(), xbmcgui.DialogProgressBG()
window_xml_left_action, window_xml_right_action, window_xml_up_action, window_xml_down_action, window_xml_info_action = 1, 2, 3, 4, 11
window_xml_selection_actions, window_xml_closing_actions, window_xml_context_actions = (7, 100), (9, 10, 13, 92), (101, 108, 117)
empty_poster, item_jump, item_next = icons.box_office, icons.item_jump, icons.item_next
tmdb_default_api, fanarttv_default_api = '6e6a68c545dffdce0e054d1060fdd6e0', '0083bfd32f3d91876dc62556b451641e'
img_url = 'https://i.imgur.com/%s'
database_path_raw = 'special://profile/addon_data/plugin.video.david/databases/'
current_dbs = ('navigator.db', 'watched.db', 'favorites.db', 'views.db', 'traktcache4.db', 'maincache.db', 'metacache.db', 'debridcache.db', 'providerscache2.db')
david_settings_str, kodi_menu_cache_str, david_kodi_menu_cache_str = 'david_settings', 'kodi_menu_cache', 'david_kodi_menu_cache'
databases_path = translatePath(database_path_raw)
navigator_db = translatePath(''.join([database_path_raw, current_dbs[0]]))
watched_db = translatePath(''.join([database_path_raw, current_dbs[1]]))
favorites_db = translatePath(''.join([database_path_raw, current_dbs[2]]))
views_db = translatePath(''.join([database_path_raw, current_dbs[3]]))
trakt_db = translatePath(''.join([database_path_raw, current_dbs[4]]))
maincache_db = translatePath(''.join([database_path_raw, current_dbs[5]]))
metacache_db = translatePath(''.join([database_path_raw, current_dbs[6]]))
debridcache_db = translatePath(''.join([database_path_raw, current_dbs[7]]))
external_db = translatePath(''.join([database_path_raw, current_dbs[8]]))
userdata_path = translatePath('special://profile/addon_data/plugin.video.david/')
addon_settings = translatePath('special://home/addons/plugin.video.david/resources/settings.xml')
user_settings = translatePath('special://profile/addon_data/plugin.video.david/settings.xml')
addon_icon, addon_fanart = translatePath('special://home/addons/plugin.video.david/icon.png'), translatePath('special://home/addons/plugin.video.david/fanart.png')
myvideos_db_paths = {18: '116', 19: '119', 20: '119'}
movie_dict_removals = ('fanart_added', 'cast', 'poster', 'rootname', 'imdb_id', 'tmdb_id', 'tvdb_id', 'all_trailers', 'fanart', 'banner', 'clearlogo', 'clearlogo2', 'clearart',
			'landscape', 'discart', 'original_title', 'english_title', 'extra_info', 'alternative_titles', 'country_codes', 'fanarttv_fanart', 'fanarttv_poster', 'fanart2','poster2',
			'keyart', 'images')
tvshow_dict_removals = ('fanart_added', 'cast', 'poster', 'rootname', 'imdb_id', 'tmdb_id', 'tvdb_id', 'all_trailers', 'discart', 'total_episodes', 'total_seasons', 'fanart',
			'banner', 'clearlogo', 'clearlogo2', 'clearart', 'landscape', 'season_data', 'original_title', 'extra_info', 'alternative_titles', 'english_title', 'season_summary',
			'country_codes', 'fanarttv_fanart', 'fanarttv_poster', 'total_aired_eps', 'fanart2', 'poster2', 'keyart', 'images')
episode_dict_removals = ('thumb', 'guest_stars')

def append_path(_path):
	sys.path.append(translatePath(_path))

def local_string(string):
	try: string = int(string)
	except: return string
	try: string = str(__addon__.getLocalizedString(string))
	except: string = __addon__.getLocalizedString(string)
	return string

def build_url(url_params):
	return ''.join(['plugin://plugin.video.david/?', urlencode(url_params)])

def remove_meta_keys(dict_item, dict_removals):
	for k in dict_removals: dict_item.pop(k, None)
	return dict_item

def add_dir(url_params, list_name, handle, iconImage='folder', fanartImage=None, isFolder=True):
	fanart = fanartImage or addon_fanart
	icon = get_icon(iconImage)
	url = build_url(url_params)
	listitem = make_listitem()
	listitem.setLabel(list_name)
	listitem.setArt({'icon': icon, 'poster': icon, 'thumb': icon, 'fanart': fanart, 'banner': icon})
	add_item(handle, url, listitem, isFolder)

def set_view_mode(view_type, content='files'):
	view_id = get_property('david_view_type_%s' % view_type)
	if not view_id:
		try:
			dbcon = database.connect(views_db, timeout=40.0, isolation_level=None)
			dbcur = dbcon.cursor()
			dbcur.execute("SELECT view_id FROM views WHERE view_type = ?", (str(view_type),))
			view_id = dbcur.fetchone()[0]
		except: return
	try:
		hold = 0
		sleep(100)
		while not container_content() == content:
			hold += 1
			if hold < 5000: sleep(1)
			else: return
		if view_id: execute_builtin('Container.SetViewMode(%s)' % view_id)
	except: return

def get_icon(image_name):
	return getattr(icons, image_name)

def logger(heading, function):
	xbmc.log('###%s###: %s' % (heading, function), 1)

def get_property(prop):
	return window.getProperty(prop)

def set_property(prop, value):
	return window.setProperty(prop, value)

def clear_property(prop):
	return window.clearProperty(prop)

def addon(addon_id='plugin.video.david'):
	return Addon(id=addon_id)

def addon_installed(addon_id):
	return get_visibility('System.HasAddon(%s)' % addon_id)

def addon_enabled(addon_id):
	return get_visibility('System.AddonIsEnabled(%s)' % addon_id)

def add_item(handle, url, listitem, isFolder):
	xbmcplugin.addDirectoryItem(handle, url, listitem, isFolder)

def add_items(handle, item_list):
	xbmcplugin.addDirectoryItems(handle, item_list)

def set_content(handle, content):
	xbmcplugin.setContent(handle, content)

def set_category(handle, category):
	xbmcplugin.setPluginCategory(handle, category)

def set_sort_method(handle, method):
	if method == 'episodes': sort_method = xbmcplugin.SORT_METHOD_EPISODE
	elif method == 'files': sort_method = xbmcplugin.SORT_METHOD_FILE
	else: sort_method = xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE#label
	xbmcplugin.addSortMethod(handle, sort_method)

def end_directory(handle, cacheToDisc=None):
	if cacheToDisc == None: cacheToDisc = get_property(david_kodi_menu_cache_str) == 'true'
	xbmcplugin.endOfDirectory(handle, cacheToDisc=cacheToDisc)

def make_session(url='https://'):
	session = requests.Session()
	session.mount(url, requests.adapters.HTTPAdapter(pool_maxsize=100))
	return session	

def make_requests():
	return requests

def make_playlist(_type='video'):
	return xbmc.PlayList(xbmc.PLAYLIST_VIDEO) if _type == 'video' else xbmc.PlayList(xbmc.PLAYLIST_MUSIC)

def convert_language(lang):
	return xbmc.convertLanguage(lang, xbmc.ISO_639_2)

def supported_media():
	return xbmc.getSupportedMedia('video')

def path_exists(path):
	return xbmcvfs.exists(path)

def make_directory(path):
	xbmcvfs.mkdir(path)

def make_directories(path):
	xbmcvfs.mkdirs(path)

def open_file(_file, mode='r'):
	return xbmcvfs.File(_file, mode)

def copy_file(source, destination):
	return xbmcvfs.copy(source, destination)

def delete_file(_file):
	xbmcvfs.delete(_file)

def delete_folder(_folder, force=False):
	xbmcvfs.rmdir(_folder, force)

def rename_file(old, new):
	xbmcvfs.rename(old, new)

def list_dirs(location):
	return xbmcvfs.listdir(location)

def make_listitem():
	return xbmcgui.ListItem(offscreen=True)

def translate_path(path):
	return translatePath(path)

def sleep(time):
	return xbmc.sleep(time)

def execute_builtin(command):
	return xbmc.executebuiltin(command)

def get_kodi_version():
	return int(get_infolabel('System.BuildVersion')[0:2])

def current_skin():
	return xbmc.getSkinDir()

def current_window_id():
	return xbmcgui.Window(xbmcgui.getCurrentWindowId())

def get_video_database_path():
	return translate_path('special://profile/Database/MyVideos%s.db' % myvideos_db_paths[get_kodi_version()])

def show_busy_dialog():
	return execute_builtin('ActivateWindow(busydialognocancel)')

def hide_busy_dialog():
	execute_builtin('Dialog.Close(busydialognocancel)')
	execute_builtin('Dialog.Close(busydialog)')

def close_all_dialog():
	execute_builtin('Dialog.Close(all,true)')

def container_content():
	return get_infolabel('Container.Content')

def external_browse():
	return 'david' not in get_infolabel('Container.PluginName')

def widget_refresh():
	return execute_builtin('UpdateLibrary(video,special://skin/foo)')

def run_plugin(params):
	if isinstance(params, dict): params = build_url(params)
	return xbmc.executebuiltin('RunPlugin(%s)' % params)

def container_update(params):
	if isinstance(params, dict): params = build_url(params)
	return execute_builtin('Container.Update(%s)' % params)

def container_refresh():
	return execute_builtin('Container.Refresh')

def disable_enable_addon(addon_name='plugin.video.david'):
	try:
		execute_JSON(json.dumps({'jsonrpc': '2.0', 'id': 1, 'method': 'Addons.SetAddonEnabled', 'params': {'addonid': addon_name, 'enabled': False}}))
		execute_JSON(json.dumps({'jsonrpc': '2.0', 'id': 1, 'method': 'Addons.SetAddonEnabled', 'params': {'addonid': addon_name, 'enabled': True}}))
	except: pass

def update_local_addons():
	execute_builtin('UpdateLocalAddons')
	sleep(2500)

def progress_dialog(heading=32036, icon=addon_icon):
	from windows import create_window
	if isinstance(heading, int): heading = local_string(heading)
	progress_dialog = create_window(('windows.progress', 'Progress'), 'progress.xml', heading=heading, icon=icon)
	Thread(target=progress_dialog.run).start()
	return progress_dialog

def ok_dialog(heading=32036, text='', ok_label=32839, top_space=True):
	from windows import open_window
	if isinstance(heading, int): heading = local_string(heading)
	if isinstance(text, int): text = local_string(text)
	if isinstance(ok_label, int): ok_label = local_string(ok_label)
	if not text: text = '[CR][CR]%s' % local_string(32760)
	elif top_space: text = '[CR][CR]%s' % text
	kwargs = {'heading': heading, 'text': text, 'ok_label': ok_label}
	return open_window(('windows.select_ok', 'OK'), 'ok.xml', **kwargs)

def confirm_dialog(heading=32036, text='', ok_label=32839, cancel_label=32840, top_space=True, default_control=11):
	from windows import open_window
	if isinstance(heading, int): heading = local_string(heading)
	if isinstance(text, int): text = local_string(text)
	if isinstance(ok_label, int): ok_label = local_string(ok_label)
	if isinstance(cancel_label, int): cancel_label = local_string(cancel_label)
	if not text: text = '[CR][CR]%s' % local_string(32580)
	elif top_space: text = '[CR][CR]%s' % text
	kwargs = {'heading': heading, 'text': text, 'ok_label': ok_label, 'cancel_label': cancel_label, 'default_control': default_control}
	return open_window(('windows.select_ok', 'Confirm'), 'confirm.xml', **kwargs)

def select_dialog(function_list, **kwargs):
	from windows import open_window
	window_xml = kwargs.get('window_xml', 'select.xml')
	selection = open_window(('windows.select_ok', 'Select'), window_xml, **kwargs)
	if selection in ([], None): return None
	if kwargs.get('multi_choice', 'false') == 'true': return [function_list[i] for i in selection]
	return function_list[selection]

def confirm_progress_media(meta, text='', enable_buttons=False, true_button=32824, false_button=32828, focus_button=11, percent=0):
	if enable_buttons:
		from windows import open_window
		if isinstance(text, int): text = local_string(text)
		if isinstance(true_button, int): true_button = local_string(true_button)
		if isinstance(false_button, int): false_button = local_string(false_button)
		kwargs = {'meta': meta, 'text': text, 'enable_buttons': enable_buttons, 'true_button': true_button, 'false_button': false_button, 'focus_button': focus_button}
		return open_window(('windows.confirm_progress_media', 'ConfirmProgressMedia'), 'confirm_progress_media.xml', **kwargs)
	else:
		from windows import create_window
		progress_dialog = create_window(('windows.confirm_progress_media', 'ConfirmProgressMedia'), 'confirm_progress_media.xml', meta=meta)
		Thread(target=progress_dialog.run).start()
		return progress_dialog

def show_text(heading, text=None, file=None, font_size='small', kodi_log=False):
	from windows import open_window
	if isinstance(heading, int): heading = local_string(heading)
	if isinstance(text, int): text = local_string(text)
	heading = heading.replace('[B]', '').replace('[/B]', '')
	if file:
		with open(file, encoding='utf-8') as r: text = r.readlines()
	if kodi_log:
		confirm = confirm_dialog(text=32855, ok_label=32824, cancel_label=32828)
		if confirm == None: return
		if confirm: text = [i for i in text if any(x in i.lower() for x in ('exception', 'error'))]
	text = ''.join(text)
	return open_window(('windows.textviewer', 'TextViewer'), 'textviewer.xml', heading=heading, text=text, font_size=font_size)

def notification(line1, time=5000, icon=None, sound=False):
	if isinstance(line1, int): line1 = local_string(line1)
	icon = icon or addon_icon
	xbmcgui.Dialog().notification(local_string(32036), line1, icon, time, sound)

def choose_view(view_type, content):
	handle = int(sys.argv[1])
	set_view_str = local_string(32547)
	settings_icon = get_icon('settings')
	listitem = make_listitem()
	listitem.setLabel(set_view_str)
	params_url = build_url({'mode': 'set_view', 'view_type': view_type})
	listitem.setArt({'icon': settings_icon, 'poster': settings_icon, 'thumb': settings_icon, 'fanart': addon_fanart, 'banner': settings_icon})
	add_item(handle, params_url, listitem, False)
	set_content(handle, content)
	end_directory(handle)
	set_view_mode(view_type, content)

def set_view(view_type):
	view_id = str(current_window_id().getFocusId())
	dbcon = database.connect(views_db, timeout=40.0, isolation_level=None)
	dbcur = dbcon.cursor()
	dbcur.execute('''PRAGMA synchronous = OFF''')
	dbcur.execute('''PRAGMA journal_mode = OFF''')
	dbcur.execute("INSERT OR REPLACE INTO views VALUES (?, ?)", (view_type, view_id))
	set_view_property(view_type, view_id)
	notification(get_infolabel('Container.Viewmode').upper(), time=500)

def set_view_property(view_type, view_id):
	set_property('david_view_type_%s' % view_type, view_id)

def set_view_properties():
	dbcon = database.connect(views_db, timeout=40.0, isolation_level=None)
	dbcur = dbcon.cursor()
	dbcur.execute('''PRAGMA synchronous = OFF''')
	dbcur.execute('''PRAGMA journal_mode = OFF''')
	dbcur.execute("SELECT * FROM views")
	view_ids = dbcur.fetchall()
	for item in view_ids: set_view_property(item[0], item[1])

def set_highlight_property(setting_value):
	set_property('david.highlight', setting_value)

def timeIt(func):
	# Thanks to 123Venom
	import time
	fnc_name = func.__name__
	def wrap(*args, **kwargs):
		started_at = time.time()
		result = func(*args, **kwargs)
		logger('%s.%s' % (__name__ , fnc_name), (time.time() - started_at))
		return result
	return wrap

def volume_checker(volume_setting):
	# 0% == -60db, 100% == 0db
	try:
		if get_visibility('Player.Muted'): return
		from modules.utils import string_alphanum_to_num
		max_volume = int(min(int(volume_setting), 100))
		current_volume_db = int(string_alphanum_to_num(get_infolabel('Player.Volume').split('.')[0]))
		current_volume_percent = int(100 - ((float(current_volume_db)/60)*100))
		if current_volume_percent > max_volume: execute_builtin('SetVolume(%d)' % int(max_volume))
	except: pass

def focus_index(index, sleep_time=100):
	sleep(sleep_time)
	current_window = current_window_id()
	focus_id = current_window.getFocusId()
	try: current_window.getControl(focus_id).selectItem(index)
	except: pass

def clear_settings_window_properties():
	clear_property('david_settings')
	notification(32576, 2500)

def fetch_kodi_imagecache(image):
	result = None
	try:
		dbcon = database.connect(translate_path('special://database/Textures13.db'), timeout=40.0)
		dbcur = dbcon.cursor()
		dbcur.execute("SELECT cachedurl FROM texture WHERE url = ?", (image,))
		result = dbcur.fetchone()[0]
	except: pass
	return result

def get_all_icon_vars(include_values=False):
	if include_values: return [(k, v) for k, v in vars(icons).items() if not k.startswith('__') and (v.endswith('.png') or v.endswith('.jpg'))]
	else: return [k for k, v in vars(icons).items() if not k.startswith('__') and (v.endswith('.png') or v.endswith('.jpg'))]

def toggle_language_invoker():
	import xml.etree.ElementTree as ET
	close_all_dialog()
	sleep(100)
	addon_xml = translate_path('special://home/addons/plugin.video.david/addon.xml')
	current_addon_setting = get_setting('reuse_language_invoker', 'true')
	new_value = 'false' if current_addon_setting == 'true' else 'true'
	if not confirm_dialog(text=local_string(33018) % (current_addon_setting.upper(), new_value.upper()), top_space=False): return
	if new_value == 'true' and not confirm_dialog(text=33019): return
	tree = ET.parse(addon_xml)
	root = tree.getroot()
	for item in root.iter('reuselanguageinvoker'):
		item.text = new_value
		tree.write(addon_xml)
		break
	set_setting('reuse_language_invoker', new_value)
	ok_dialog(text=32576)
	execute_builtin('ActivateWindow(Home)')
	update_local_addons()
	disable_enable_addon()

def upload_logfile():
	# Thanks 123Venom
	if not confirm_dialog(text=32580): return
	show_busy_dialog()
	url = 'https://paste.kodi.tv/'
	log_file = translate_path('special://logpath/kodi.log')
	if not path_exists(log_file): return ok_dialog(text=33039)
	try:
		with open_file(log_file) as f: text = f.read()
		UserAgent = 'David %s' % __addon__.getAddonInfo('version')
		response = requests.post(''.join([url, 'documents']), data=text.encode('utf-8', errors='ignore'), headers={'User-Agent': UserAgent}).json()
		if 'key' in response: ok_dialog(text=''.join([url, response['key']]))
		else: ok_dialog(text=33039)
	except: ok_dialog(text=33039)
	hide_busy_dialog()

def open_settings(query, addon='plugin.video.david'):
	hide_busy_dialog()
	if query:
		try:
			button, control = 100, 80
			menu, function = query.split('.')
			execute_builtin('Addon.OpenSettings(%s)' % addon)
			execute_builtin('SetFocus(%i)' % (int(menu) - button))
			execute_builtin('SetFocus(%i)' % (int(function) - control))
		except: execute_builtin('Addon.OpenSettings(%s)' % addon)
	else: execute_builtin('Addon.OpenSettings(%s)' % addon)

def clean_settings():
	import xml.etree.ElementTree as ET
	def _make_content(dict_object):
		content = '<settings version="2">'
		new_line = '\n    '
		for item in dict_object:
			_id = item['id']
			if _id in active_settings:
				if 'default' in item and 'value' in item: content += '%s<setting id="%s" default="%s">%s</setting>' % (new_line, _id, item['default'], item['value'])
				elif 'default' in item: content += '%s<setting id="%s" default="%s"></setting>' % (new_line, _id, item['default'])
				elif 'value' in item: content += '%s<setting id="%s">%s</setting>' % (new_line, _id, item['value'])
				else: content += '%s<setting id="%s"></setting>' % new_line
		content += '\n</settings>'
		return content
	close_all_dialog()
	active_settings, current_user_settings = [], []
	active_append, current_append = active_settings.append, current_user_settings.append
	root = ET.parse(addon_settings).getroot()
	for i in root.findall('./category/setting'):
		setting_id = i.get('id')
		if setting_id: active_append(setting_id)
	root = ET.parse(user_settings).getroot()
	for i in root:
		dict_item = {}
		setting_id = i.get('id')
		setting_default = i.get('default')
		setting_value = i.text
		dict_item['id'] = setting_id
		if setting_value: dict_item['value'] = setting_value
		if setting_default: dict_item['default'] = setting_default
		current_append(dict_item)
	new_content = _make_content(current_user_settings)
	with open_file(user_settings, 'w') as f: f.write(new_content)
	notification(32576, 2500)

def set_setting(setting_id, value):
	addon().setSetting(setting_id, value)

def get_setting(setting_id, fallback=None):
	try: settings_dict = json.loads(get_property(david_settings_str))
	except: settings_dict = make_settings_dict()
	if settings_dict is None: settings_dict = get_setting_fallback(setting_id)
	value = settings_dict.get(setting_id, '')
	if fallback is None: return value
	if value == '': return fallback
	return value

def get_setting_fallback(setting_id):
	return {setting_id: addon().getSetting(setting_id)}

def make_settings_dict():
	import xml.etree.ElementTree as ET
	settings_dict = None
	clear_property(david_settings_str)
	try:
		if not path_exists(userdata_path): make_directories(userdata_path)
		root = ET.parse(user_settings).getroot()
		settings_dict = {}
		dict_update = settings_dict.update
		for item in root:
			setting_id = item.get('id')
			setting_value = item.text
			if setting_value is None: setting_value = ''
			dict_item = {setting_id: setting_value}
			dict_update(dict_item)
		set_property(david_settings_str, json.dumps(settings_dict))
		set_property(david_kodi_menu_cache_str, get_setting(kodi_menu_cache_str))
	except: pass
	return settings_dict

def pause_settings_change():
	set_property('david_pause_onSettingsChanged', 'true')

def unpause_settings_change():
	clear_property('david_pause_onSettingsChanged')
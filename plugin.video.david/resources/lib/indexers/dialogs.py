# -*- coding: utf-8 -*-
import metadata
from windows import open_window
from caches import refresh_cached_data
from modules import kodi_utils, source_utils, settings
from modules.utils import get_datetime
# logger = kodi_utils.logger

ok_dialog, container_content, container_refresh, close_all_dialog = kodi_utils.ok_dialog, kodi_utils.container_content, kodi_utils.container_refresh, kodi_utils.close_all_dialog
get_property, open_settings, set_property, get_icon, dialog = kodi_utils.get_property, kodi_utils.open_settings, kodi_utils.set_property, kodi_utils.get_icon, kodi_utils.dialog
show_busy_dialog, hide_busy_dialog, notification, confirm_dialog = kodi_utils.show_busy_dialog, kodi_utils.hide_busy_dialog, kodi_utils.notification, kodi_utils.confirm_dialog
pause_settings_change, unpause_settings_change, img_url, sleep = kodi_utils.pause_settings_change, kodi_utils.unpause_settings_change, kodi_utils.img_url, kodi_utils.sleep
get_setting, set_setting, make_settings_dict, execute_builtin = kodi_utils.get_setting, kodi_utils.set_setting, kodi_utils.make_settings_dict, kodi_utils.execute_builtin
json, ls, build_url, translate_path, select_dialog = kodi_utils.json, kodi_utils.local_string, kodi_utils.build_url, kodi_utils.translate_path, kodi_utils.select_dialog
run_plugin, metadata_user_info, autoplay_next_episode, quality_filter = kodi_utils.run_plugin, settings.metadata_user_info, settings.autoplay_next_episode, settings.quality_filter
get_language, extras_enabled_menus, active_internal_scrapers, auto_play = settings.get_language, settings.extras_enabled_menus, settings.active_internal_scrapers, settings.auto_play
display_uncached_torrents, quality_filter, watched_indicators = settings.display_uncached_torrents, settings.quality_filter, settings.watched_indicators
clear_and_rescrape, scrape_with_default, scrape_with_disabled = source_utils.clear_and_rescrape, source_utils.scrape_with_default, source_utils.scrape_with_disabled
toggle_all, enable_disable, set_default_scrapers = source_utils.toggle_all, source_utils.enable_disable, source_utils.set_default_scrapers
scrape_with_filters_ignored, scrape_with_aliases = source_utils.scrape_with_filters_ignored, source_utils.scrape_with_aliases
scrape_with_custom_values, clear_scrapers_cache = source_utils.scrape_with_custom_values, source_utils.clear_scrapers_cache
david_str = ls(32036)

def trailer_choice(media_type, poster, tmdb_id, trailer_url, all_trailers=[]):
	if get_language() != 'en' and not trailer_url and not all_trailers:
		show_busy_dialog()
		from apis.tmdb_api import tmdb_media_videos
		try: all_trailers = tmdb_media_videos(media_type, tmdb_id)['results']
		except: pass
		hide_busy_dialog()
	if all_trailers:
		from modules.utils import clean_file_name
		if len(all_trailers) == 1: video_id = all_trailers[0].get('key')
		else:
			list_items = [{'line1': clean_file_name(i['name']), 'icon': poster} for i in all_trailers]
			kwargs = {'items': json.dumps(list_items), 'window_xml': 'media_select.xml'}
			video_id = select_dialog([i['key'] for i in all_trailers], **kwargs)
			if video_id == None: return 'canceled'
		trailer_url = 'plugin://plugin.video.youtube/play/?video_id=%s' % video_id
	return trailer_url

def genres_choice(media_type, genres, poster, return_genres=False):
	from modules.meta_lists import movie_genres, tvshow_genres
	def _process_dicts(genre_str, _dict):
		final_genres_list = []
		append = final_genres_list.append
		for key, value in _dict.items():
			if key in genre_str: append({'genre': key, 'value': value})
		return final_genres_list
	if media_type in ('movie', 'movies'): genre_action, meta_type, action = movie_genres, 'movie', 'tmdb_movies_genres'
	else: genre_action, meta_type, action = tvshow_genres, 'tvshow', 'tmdb_tv_genres'
	genre_list = _process_dicts(genres, genre_action)
	if return_genres: return genre_list
	if len(genre_list) == 0:
		notification(32760, 2500)
		return None
	mode = 'build_%s_list' % meta_type
	list_items = [{'line1': i['genre'], 'icon': poster} for i in genre_list]
	kwargs = {'items': json.dumps(list_items), 'window_xml': 'media_select.xml'}
	return select_dialog([{'mode': mode, 'action': action, 'genre_id': i['value'][0]} for i in genre_list], **kwargs)

def imdb_keywords_choice(media_type, imdb_id, poster):
	from apis.imdb_api import imdb_keywords
	show_busy_dialog()
	keywords_info = imdb_keywords(imdb_id)
	if len(keywords_info) == 0:
		hide_busy_dialog()
		notification(32760, 2500)
		return None
	meta_type = 'movie' if media_type == 'movies' else 'tvshow'
	mode = 'build_%s_list' % meta_type
	list_items = [{'line1': i, 'icon': poster} for i in keywords_info]
	kwargs = {'items': json.dumps(list_items), 'enable_context_menu': 'true', 'media_type': media_type, 'window_xml': 'media_select.xml'}
	hide_busy_dialog()
	return select_dialog([{'mode': mode, 'action': 'imdb_keywords_list_contents', 'list_id': i, 'media_type': media_type} for i in keywords_info], **kwargs)

def imdb_videos_choice(videos, poster):
	try: videos = json.loads(videos)
	except: pass
	videos.sort(key=lambda x: x['quality_rank'])
	list_items = [{'line1': i['quality'], 'icon': poster} for i in videos]
	kwargs = {'items': json.dumps(list_items), 'window_xml': 'media_select.xml'}
	return select_dialog([i['url'] for i in videos], **kwargs)

def random_choice(params):
	tmdb_id, poster, return_choice, window_xml = params.get('tmdb_id'), params.get('poster'), params.get('return_choice', 'false'), params.get('window_xml', 'select.xml'), 
	list_items = [{'line1': ls(32541), 'icon': poster}, {'line1': ls(32542), 'icon': poster}]
	choices = ['play_random', 'play_random_continual']
	kwargs = {'items': json.dumps(list_items), 'heading': ls(32540), 'window_xml': window_xml}
	choice = select_dialog(choices, **kwargs)
	if return_choice == 'true': return choice
	if choice == None: return
	from modules.utils import manual_function_import
	function = manual_function_import('modules.episode_tools', choice)
	function(tmdb_id)

def trakt_manager_choice(params):
	if not get_setting('trakt.user', ''): return notification(32760, 3500)
	icon = params.get('icon', None) or get_icon('trakt')
	choices = [('%s %s...' % (ls(32602), ls(32199)), 'Add'), ('%s %s...' % (ls(32603), ls(32199)), 'Remove')]
	list_items = [{'line1': item[0], 'icon': icon} for item in choices]
	kwargs = {'items': json.dumps(list_items), 'heading': ls(32198).replace('[B]', '').replace('[/B]', ''), 'window_xml': params.get('window_xml', 'select.xml')}
	choice = select_dialog([i[1] for i in choices], **kwargs)
	if choice == None: return
	if choice == 'Add':
		from apis.trakt_api import trakt_add_to_list
		trakt_add_to_list(params)
	else:
		from apis.trakt_api import trakt_remove_from_list
		trakt_remove_from_list(params)

def playback_choice(media_type, poster, meta, season, episode, window_xml):
	items = []
	items += [{'line': ls(32014), 'function': 'clear_and_rescrape'}]
	items += [{'line': ls(32185), 'function': 'scrape_with_default'}]
	items += [{'line': ls(32006), 'function': 'scrape_with_disabled'}]
	items += [{'line': ls(32807), 'function': 'scrape_with_filters_ignored'}]
	if meta['alternative_titles']: items += [{'line': ls(32212), 'function': 'scrape_with_aliases'}]
	items += [{'line': ls(32135), 'function': 'scrape_with_custom_values'}]
	list_items = [{'line1': i['line'], 'icon': poster} for i in items]
	kwargs = {'items': json.dumps(list_items), 'heading': ls(32174), 'window_xml': window_xml}
	choice = select_dialog([i['function'] for i in items], **kwargs)
	if choice == None: return
	if choice == 'clear_and_rescrape': clear_and_rescrape(media_type, meta, season, episode)
	elif choice == 'scrape_with_default': scrape_with_default(media_type, meta, season, episode)
	elif choice == 'scrape_with_disabled': scrape_with_disabled(media_type, meta, season, episode)
	elif choice == 'scrape_with_filters_ignored': scrape_with_filters_ignored(media_type, meta, season, episode)
	elif choice == 'scrape_with_aliases': scrape_with_aliases(media_type, meta, season, episode)
	else: scrape_with_custom_values(media_type, meta, season, episode)

def set_quality_choice(quality_setting):
	include = ls(32188)
	dl = ['%s SD' % include, '%s 720p' % include, '%s 1080p' % include, '%s 4K' % include]
	fl = ['SD', '720p', '1080p', '4K']
	try: preselect = [fl.index(i) for i in get_setting(quality_setting).split(', ')]
	except: preselect = []
	list_items = [{'line1': item} for item in dl]
	kwargs = {'items': json.dumps(list_items), 'heading': david_str, 'multi_choice': 'true', 'preselect': preselect}
	choice = select_dialog(fl, **kwargs)
	if choice is None: return
	if choice == []:
		ok_dialog(text=32574)
		return set_quality_choice(quality_setting)
	set_setting(quality_setting, ', '.join(choice))

def extras_lists_choice():
	fl = [2050, 2051, 2052, 2053, 2054, 2055, 2056, 2057, 2058, 2059, 2060, 2061, 2062]
	dl = [
			{'name': ls(32664),                            'image': img_url % 'DrqssE5.jpg'},
			{'name': ls(32503),                            'image': img_url % 'FZ6xrxr.jpg'},
			{'name': ls(32607),                            'image': img_url % 'CAvVerM.jpg'},
			{'name': ls(32984),                            'image': img_url % 'nz8PVph.jpg'},
			{'name': ls(32986),                            'image': img_url % 'jmFttcs.jpg'},
			{'name': ls(32989),                            'image': img_url % 'H5JLFoD.jpg'},
			{'name': ls(33032),                            'image': img_url % 'cdpBetd.jpg'},
			{'name': ls(32616),                            'image': img_url % 'mbPvLrG.jpg'},
			{'name': ls(32617),                            'image': img_url % '6TVW6r8.jpg'},
			{'name': '%s %s' % (ls(32612), ls(32543)),     'image': img_url % '6cVE5WT.jpg'},
			{'name': '%s %s' % (ls(32612), ls(32470)),     'image': img_url % 'ahJK4ZX.jpg'},
			{'name': '%s %s' % (ls(32612), ls(32480)),     'image': img_url % 'adtLIuW.jpg'},
			{'name': '%s %s' % (ls(32612), ls(32499)),     'image': img_url % 'wn2MpHK.jpg'}
			]
	try: preselect = [fl.index(i) for i in extras_enabled_menus()]
	except: preselect = []
	kwargs = {'items': json.dumps(dl), 'preselect': preselect}
	selection = open_window(('windows.extras', 'ExtrasChooser'), 'extras_chooser.xml', **kwargs)
	if selection  == []: return set_setting('extras.enabled_menus', 'noop')
	elif selection == None: return
	selection = [str(fl[i]) for i in selection]
	set_setting('extras.enabled_menus', ','.join(selection))

def set_language_filter_choice(filter_setting):
	from modules.meta_lists import language_choices
	lang_choices = language_choices
	lang_choices.pop('None')
	dl = list(lang_choices.keys())
	fl = list(lang_choices.values())
	try: preselect = [fl.index(i) for i in get_setting(filter_setting).split(', ')]
	except: preselect = []
	list_items = [{'line1': item} for item in dl]
	kwargs = {'items': json.dumps(list_items), 'heading': david_str, 'multi_choice': 'true', 'preselect': preselect}
	choice = select_dialog(fl, **kwargs)
	if choice == None: return
	if choice == []: return set_setting(filter_setting, 'eng')
	set_setting(filter_setting, ', '.join(choice))

def enable_scrapers_choice():
	scrapers = ['external', 'furk', 'easynews', 'rd_cloud', 'pm_cloud', 'ad_cloud', 'folders']
	cloud_scrapers = {'rd_cloud': 'rd.enabled', 'pm_cloud': 'pm.enabled', 'ad_cloud': 'ad.enabled'}
	scraper_names = [ls(32118).upper(), ls(32069).upper(), ls(32070).upper(), ls(32098).upper(), ls(32097).upper(), ls(32099).upper(), ls(32108).upper()]
	preselect = [scrapers.index(i) for i in active_internal_scrapers()]
	list_items = [{'line1': item} for item in scraper_names]
	kwargs = {'items': json.dumps(list_items), 'heading': david_str, 'multi_choice': 'true', 'preselect': preselect}
	choice = select_dialog(scrapers, **kwargs)
	if choice is None: return
	for i in scrapers:
		set_setting('provider.%s' % i, ('true' if i in choice else 'false'))
		if i in cloud_scrapers and i in choice: set_setting(cloud_scrapers[i], 'true')

def folder_scraper_manager_choice(params):
	def _set_settings(refresh=True):
		set_setting(name_setting % setting_id, display_name)
		set_setting(settings_dict[media_type] % setting_id, folder_path)
		sleep(250)
		if refresh: container_refresh()
	setting_id, media_type, folder_path = params['setting_id'], params['media_type'], params.get('folder_path', '')
	display_name, default_name = params.get('display_name', ''), params['default_name']
	set_folder_path = True
	name_setting, movie_dir_setting, tvshow_dir_setting = '%s.display_name', '%s.movies_directory', '%s.tv_shows_directory'
	settings_dict = {'movie': movie_dir_setting, 'tvshow': tvshow_dir_setting}
	if folder_path:
		confirm = confirm_dialog(heading=display_name, text=ls(32529) % default_name, ok_label=32531, cancel_label=32530)
		if confirm is None: return
		elif confirm:
			ok_dialog(heading=default_name, text=ls(32532) % default_name)
			display_name, folder_path = default_name, 'None'
			_set_settings(refresh=False)
			media_type = 'tvshow' if media_type == 'movie' else 'movie'
			return _set_settings()
		else:
			if not confirm_dialog(heading=display_name, text=32640, default_control=10): set_folder_path = False
	if set_folder_path:
		folder_path = dialog.browse(0, david_str, '')
		if not folder_path:
			if confirm_dialog(heading=display_name, text=32704): return folder_scraper_manager_choice(params)
			else: return	
	display_name = dialog.input(ls(32115), defaultt=display_name or setting_id)
	if not display_name:
		if confirm_dialog(heading=display_name, text=32714): return folder_scraper_manager_choice(params)
		else: return
	_set_settings()

def results_sorting_choice():
	quality, provider, size = ls(32241), ls(32583), ls(32584)
	choices = [('%s, %s, %s' % (quality, provider, size), '0'), ('%s, %s, %s' % (quality, size, provider), '1'), ('%s, %s, %s' % (provider, quality, size), '2'),
			   ('%s, %s, %s' % (provider, size, quality), '3'), ('%s, %s, %s' % (size, quality, provider), '4'), ('%s, %s, %s' % (size, provider, quality), '5')]
	list_items = [{'line1': item[0]} for item in choices]
	kwargs = {'items': json.dumps(list_items), 'heading': david_str}
	choice = select_dialog(choices, **kwargs)
	if choice:
		set_setting('results.sort_order_display', choice[0])
		set_setting('results.sort_order', choice[1])

def results_layout_choice():
	xml_choices = [
					('List Default',                 img_url % '0Lb04hk.jpg'),
					('List Contrast Default',        img_url % 'DBsYcm6.jpg'),
					('List Details',                 img_url % 'nFC4UbE.jpg'),
					('List Contrast Details',        img_url % '2WfD4yD.jpg'),
					('InfoList Default',             img_url % 'P4AADhh.jpg'),
					('InfoList Contrast Default',    img_url % 'QQ44Cx2.jpg'),
					('InfoList Details',             img_url % 'uHiOrlI.jpg'),
					('InfoList Contrast Details',    img_url % 'wePo8Vv.jpg'),
					('Rows Default',                 img_url % 'qzRAmlJ.jpg'),
					('Rows Contrast Default',        img_url % 'orI2VTr.jpg'),
					('Rows Details',                 img_url % 'gz9iNyu.jpg'),
					('Rows Contrast Details',        img_url % '44OzIVW.jpg'),
					('Shift Default',                img_url % 'nhi1D6p.jpg'),
					('Shift Contrast Default',       img_url % 'WvIyls6.jpg'),
					('Shift Details',                img_url % 'gDZGrNB.jpg'),
					('Shift Contrast Details',       img_url % 'Z8AtLTn.jpg'),
					('Thumb Default',                img_url % 'qIeY87X.jpg'),
					('Thumb Contrast Default',       img_url % 'Tljq3fY.jpg'),
					('Thumb Details',                img_url % 'gNwGV0x.jpg'),
					('Thumb Contrast Details',       img_url % 'TLHIutH.jpg')
					]
	choice = open_window(('windows.sources', 'SourceResultsChooser'), 'sources_chooser.xml', xml_choices=xml_choices)
	if choice: set_setting('results.xml_style', choice)

def set_subtitle_choice():
	choices = ((ls(32192), '0'), (ls(32193), '1'), (ls(32027), '2'))
	list_items = [{'line1': item[0]} for item in choices]
	kwargs = {'items': json.dumps(list_items), 'heading': david_str}
	choice = select_dialog([i[1] for i in choices], **kwargs)
	if choice: return set_setting('subtitles.subs_action', choice)

def scraper_dialog_color_choice(setting):
	setting ='int_dialog_highlight' if setting == 'internal' else 'ext_dialog_highlight'
	chosen_color = color_choice()
	if chosen_color: set_setting(setting, chosen_color)

def scraper_quality_color_choice(setting):
	chosen_color = color_choice()
	if chosen_color: set_setting(setting, chosen_color)

def scraper_color_choice(setting):
	choices = [('furk', 'provider.furk_colour'),
				('easynews', 'provider.easynews_colour'),
				('debrid_cloud', 'provider.debrid_cloud_colour'),
				('folders', 'provider.folders_colour'),
				('hoster', 'hoster.identify'),
				('torrent', 'torrent.identify'),
				('rd', 'provider.rd_colour'),
				('pm', 'provider.pm_colour'),
				('ad', 'provider.ad_colour')]
	setting = [i[1] for i in choices if i[0] == setting][0]
	chosen_color = color_choice()
	if chosen_color: set_setting(setting, chosen_color)

def color_choice(msg_dialog=david_str, custom_color=False):
	from modules.meta_lists import colors
	color_chart = colors
	color_display = ['[COLOR=%s]%s[/COLOR]' % (i, i.capitalize()) for i in color_chart]
	if custom_color:
		color_chart.insert(0, 'HEX')
		color_display.insert(0, '[I]Input Custom Color (hexadecimal code).....[/I]')
	list_items = [{'line1': item} for item in color_display]
	kwargs = {'items': json.dumps(list_items), 'heading': david_str}
	choice = select_dialog(color_chart, **kwargs)
	if choice == None: return
	return choice

def highlight_choice():
	chosen_color = color_choice(custom_color=True)
	if chosen_color:
		if chosen_color == 'HEX':
			chosen_color = dialog.input(ls(32124))
			if not chosen_color: return
			chosen_color = chosen_color.upper()
			if not chosen_color.startswith('FF'): chosen_color = 'FF' + chosen_color
		set_setting('david.highlight', chosen_color)
		set_setting('david.highlight_name', '[COLOR=%s]%s[/COLOR]' % (chosen_color, chosen_color))
		set_property('david.highlight', chosen_color)

def meta_language_choice():
	from modules.meta_lists import meta_languages
	langs = meta_languages
	list_items = [{'line1': i['name']} for i in langs]
	kwargs = {'items': json.dumps(list_items), 'heading': ls(32145)}
	choice = select_dialog(langs, **kwargs)
	if choice == None: return None
	from caches.meta_cache import delete_meta_cache
	set_setting('meta_language', choice['iso'])
	set_setting('meta_language_display', choice['name'])
	delete_meta_cache(silent=True)

def favorites_choice(params):
	from modules.favorites import Favorites
	favorites = Favorites(params)
	media_type, tmdb_id, title = params['media_type'], params['tmdb_id'], params['title']
	current_favorites = favorites.get_favorites(media_type)
	if any(i['tmdb_id'] == tmdb_id for i in current_favorites): action, text = favorites.remove_from_favorites, '%s %s?' % (ls(32603), ls(32453))
	else: action, text = favorites.add_to_favorites, '%s %s?' % (ls(32602), ls(32453))
	if not confirm_dialog(heading=title, text=text): return
	action()

def external_scrapers_choice():
	icon = translate_path('special://home/addons/script.module.qscrapers/icon.png')
	all_color, hosters_color, torrent_color = 'mediumvioletred', get_setting('hoster.identify'), get_setting('torrent.identify')
	enable_string, disable_string, specific_string, all_string = ls(32055), ls(32024), ls(32536), ls(32129)
	scrapers_string, hosters_string, torrent_string = ls(32533), ls(33031), ls(32535)
	fs_default_string = ls(32137)
	all_scrapers_string = '%s %s' % (all_string, scrapers_string)
	hosters_scrapers_string = '%s %s' % (hosters_string, scrapers_string)
	torrent_scrapers_string = '%s %s' % (torrent_string, scrapers_string)
	enable_string_base = '%s %s %s %s' % (enable_string, all_string, '%s', scrapers_string)
	disable_string_base = '%s %s %s %s' % (disable_string, all_string, '%s', scrapers_string)
	enable_disable_string_base = '%s/%s %s %s %s' % (enable_string, disable_string, specific_string, '%s', scrapers_string)
	all_scrapers_base = '[COLOR %s]%s [/COLOR]' % (all_color, all_scrapers_string.upper())
	debrid_scrapers_base = '[COLOR %s]%s [/COLOR]' % (hosters_color, hosters_scrapers_string.upper())
	torrent_scrapers_base = '[COLOR %s]%s [/COLOR]' % (torrent_color, torrent_scrapers_string.upper())
	tools_menu = \
		[(all_scrapers_base, fs_default_string, {'mode': 'set_default_scrapers'}),
		(all_scrapers_base, enable_string_base % '', {'mode': 'toggle_all', 'folder': 'all', 'setting': 'true'}),
		(all_scrapers_base, disable_string_base % '', {'mode': 'toggle_all', 'folder': 'all', 'setting': 'false'}),
		(all_scrapers_base, enable_disable_string_base % '', {'mode': 'enable_disable', 'folder': 'all'}),
		(debrid_scrapers_base, enable_string_base % hosters_string, {'mode': 'toggle_all', 'folder': 'hosters', 'setting': 'true'}),
		(debrid_scrapers_base, disable_string_base % hosters_string, {'mode': 'toggle_all', 'folder': 'hosters', 'setting': 'false'}),
		(debrid_scrapers_base, enable_disable_string_base % hosters_string, {'mode': 'enable_disable', 'folder': 'hosters'}),
		(torrent_scrapers_base, enable_string_base % torrent_string, {'mode': 'toggle_all', 'folder': 'torrents', 'setting': 'true'}),
		(torrent_scrapers_base, disable_string_base % torrent_string, {'mode': 'toggle_all', 'folder': 'torrents', 'setting': 'false'}),
		(torrent_scrapers_base, enable_disable_string_base % torrent_string, {'mode': 'enable_disable', 'folder': 'torrents'})]
	list_items = [{'line1': item[0], 'line2': item[1], 'icon': icon} for item in tools_menu]
	kwargs = {'items': json.dumps(list_items), 'heading': david_str, 'multi_line': 'true'}
	chosen_tool = select_dialog(tools_menu, **kwargs)
	if chosen_tool == None: return
	params = chosen_tool[2]
	mode = params['mode']
	if mode == 'toggle_all': toggle_all(params['folder'], params['setting'])
	elif mode == 'enable_disable': enable_disable(params['folder'])
	elif mode == 'set_default_scrapers': set_default_scrapers()
	return external_scrapers_choice()

def options_menu(params, meta=None):
	def _builder():
		for item in listing:
			line1, line2 = item[0], item[1]
			if line2 == '': line2 = line1
			yield {'line1': line1, 'line2': line2, 'icon': poster}
	pause_settings_change()
	content, poster, window_xml = params.get('content', None), params.get('poster', None), params.get('window_xml', 'select.xml')
	if not content: content = container_content()[:-1]
	menu_type = content
	if content == 'episode_single': content = 'episode'
	if not meta:
		function = metadata.movie_meta if content == 'movie' else metadata.tvshow_meta
		meta = function('tmdb_id', params['tmdb_id'], metadata_user_info(), get_datetime())
	window_action = 'ActivateWindow(Videos,%s,return)' if params.get('is_widget') in (True, 'True', 'true') else 'Container.Update(%s)'
	listing = []
	if menu_type in ('movie', 'episode', 'episode_single'):
		listing += [(ls(32187), '%s %s' % (ls(32533), ls(32841)), 'playback_choice')]
		if menu_type == 'episode_single':
			listing += [(ls(32838), '%s %s' % (ls(32838), meta['title']), 'browse')]
			listing += [(ls(32544).replace(' %s', ''), ls(32544) % (meta['title'], params.get('season', '')), 'browse_season')]
			if watched_indicators() == 1: listing += [(ls(32599), '', 'nextep_manager')]
	if menu_type in ('movie', 'tvshow'):
		listing += [(ls(32198), '', 'trakt_manager')]
		listing += [(ls(32197), '', 'favorites_choice')]
		listing += [(ls(32503), ls(32004) % meta['rootname'], 'recommended')]
		if menu_type == 'tvshow': listing += [(ls(32613), ls(32004) % meta['rootname'], 'random')]
	if menu_type in ('movie', 'episode', 'episode_single'):
		base_str1, base_str2, on_str, off_str = '%s%s', '%s: [B]%s[/B]' % (ls(32598), '%s'), ls(32090), ls(32027)
		if auto_play(content): autoplay_status, autoplay_toggle, quality_setting = on_str, 'false', 'autoplay_quality_%s' % content
		else: autoplay_status, autoplay_toggle, quality_setting = off_str, 'true', 'results_quality_%s' % content
		current_subs_action = get_setting('subtitles.subs_action')
		current_subs_action_status = 'Auto' if current_subs_action == '0' else ls(32193) if current_subs_action == '1' else off_str
		active_int_scrapers = [i.replace('_', '') for i in active_internal_scrapers()]
		current_scrapers_status = ', '.join([i for i in active_int_scrapers]) if len(active_int_scrapers) > 0 else 'N/A'
		current_quality_status =  ', '.join(quality_filter(quality_setting))
		listing += [(base_str1 % (ls(32175), ' (%s)' % content), base_str2 % autoplay_status, 'toggle_autoplay')]
		if autoplay_status == on_str and menu_type in ('episode', 'episode_single'):
			autoplay_next_status, autoplay_next_toggle = (on_str, 'false') if autoplay_next_episode() else (off_str, 'true')
			listing += [(base_str1 % (ls(32178), ''), base_str2 % autoplay_next_status, 'toggle_autoplay_next')]
		listing += [(base_str1 % (ls(32105), ' (%s)' % content), base_str2 % current_quality_status, 'set_quality')]
		listing += [(base_str1 % ('', '%s %s' % (ls(32055), ls(32533))), base_str2 % current_scrapers_status, 'enable_scrapers')]
		if autoplay_status == off_str:
			results_xml_style_status = get_setting('results.xml_style', 'Default')
			results_sorting_status = get_setting('results.sort_order_display').replace('$ADDON[plugin.video.david 32582]', ls(32582))
			listing += [(base_str1 % ('', ls(32638)), base_str2 % results_xml_style_status, 'set_results_xml_display')]
			listing += [(base_str1 % ('', ls(32151)), base_str2 % results_sorting_status, 'set_results_sorting')]
		listing += [(base_str1 % ('', ls(32183)), base_str2 % current_subs_action_status, 'set_subs_action')]
		if 'external' in active_int_scrapers:
			uncached_torrents_status, uncached_torrents_toggle = (on_str, 'false') if display_uncached_torrents() else (off_str, 'true')
			listing += [(base_str1 % ('', ls(32160)), base_str2 % uncached_torrents_status, 'toggle_torrents_display_uncached')]
	listing += [(ls(32046), '', 'extras_lists_choice')]
	if menu_type in ('movie', 'tvshow'): listing += [(ls(32604) % (ls(32028) if menu_type == 'movie' else ls(32029)), '', 'clear_media_cache')]
	if menu_type in ('movie', 'episode', 'episode_single'): listing += [(ls(32637), '', 'clear_scrapers_cache')]
	listing += [('%s %s' % (ls(32118), ls(32513)), '', 'open_external_scrapers_choice')]
	listing += [('%s %s %s' % (ls(32598), ls(32036), ls(32247)), '', 'open_david_settings')]
	list_items = list(_builder())
	heading = meta.get('rootname', None) or ls(32646).replace('[B]', '').replace('[/B]', '')
	kwargs = {'items': json.dumps(list_items), 'heading': heading, 'multi_line': 'true', 'window_xml': window_xml}
	choice = select_dialog([i[2] for i in listing], **kwargs)
	if choice in (None, 'trakt_manager', 'favorites_choice', 'playback_choice', 'clear_media_cache', 'clear_scrapers_cache', 'open_external_scrapers_choice', 'open_david_settings',
				'browse', 'browse_season', 'nextep_manager', 'recommended', 'random'): unpause_settings_change()
	if choice == None: return
	elif choice == 'clear_media_cache':
		return refresh_cached_data(meta)
	elif choice == 'clear_scrapers_cache':
		return clear_scrapers_cache()
	elif choice == 'open_external_scrapers_choice':
		return external_scrapers_choice()
	elif choice == 'open_david_settings':
		return open_settings('0.0')
	elif choice == 'playback_choice':
		return playback_choice(content, poster, meta, params.get('season', None), params.get('episode', None), window_xml)
	elif choice == 'browse':
		return execute_builtin(window_action % build_url({'mode': 'build_season_list', 'tmdb_id': params['tmdb_id']}))
	elif choice == 'browse_season':
		return execute_builtin(window_action % build_url({'mode': 'build_episode_list', 'tmdb_id': params['tmdb_id'], 'season': params.get('season', None)}))
	elif choice == 'nextep_manager':
		return execute_builtin(window_action % build_url({'mode': 'build_next_episode_manager'}))
	elif choice == 'recommended':
		close_all_dialog()
		mode, action = ('build_movie_list', 'tmdb_movies_recommendations') if menu_type == 'movie' else ('build_tvshow_list', 'tmdb_tv_recommendations')
		return execute_builtin(window_action % build_url({'mode': mode, 'action': action, 'tmdb_id': params['tmdb_id']}))
	elif choice == 'random':
		close_all_dialog()
		return run_plugin({'mode': 'random_choice', 'tmdb_id': params['tmdb_id'], 'poster': poster})
	elif choice == 'trakt_manager':
		return trakt_manager_choice({'tmdb_id': params['tmdb_id'], 'imdb_id': meta.get('imdb_id'), 'tvdb_id': meta.get('tvdb_id', 'None'),
									'media_type': content, 'window_xml': window_xml, 'icon': poster})
	elif choice == 'favorites_choice':
		return favorites_choice({'tmdb_id': params['tmdb_id'], 'title': meta.get('title'), 'media_type': content})
	elif choice == 'toggle_autoplay':
		set_setting('auto_play_%s' % content, autoplay_toggle)
	elif choice == 'toggle_autoplay_next':
		set_setting('autoplay_next_episode', autoplay_next_toggle)
	elif choice == 'set_quality':
		set_quality_choice('autoplay_quality_%s' % content if autoplay_status == on_str else 'results_quality_%s' % content)
	elif choice == 'enable_scrapers':
		enable_scrapers_choice()
	elif choice == 'set_results_xml_display':
		results_layout_choice()
	elif choice == 'set_results_sorting':
		results_sorting_choice()
	elif choice == 'set_subs_action':
		set_subtitle_choice()
	elif choice == 'extras_lists_choice':
		extras_lists_choice()
	elif choice == 'toggle_torrents_display_uncached':
		set_setting('torrent.display.uncached', uncached_torrents_toggle)
	make_settings_dict()
	options_menu(params, meta=meta)

def extras_menu(params):
	show_busy_dialog()
	function = metadata.movie_meta if params['media_type'] == 'movie' else metadata.tvshow_meta
	meta = function('tmdb_id', params['tmdb_id'], metadata_user_info(), get_datetime())
	hide_busy_dialog()
	open_window(['windows.extras', 'Extras'], 'extras.xml', meta=meta, is_widget=params.get('is_widget', 'false'))

def media_extra_info(media_type, meta):
	extra_info, body = meta.get('extra_info', None), []
	append = body.append
	tagline_str, premiered_str, rating_str, votes_str, runtime_str = ls(32619), ls(32620), ls(32621), ls(32623), ls(32622)
	genres_str, budget_str, revenue_str, director_str, writer_str = ls(32624), ls(32625), ls(32626), ls(32627), ls(32628)
	studio_str, collection_str, homepage_str, status_str, type_str, classification_str = ls(32615), ls(32499), ls(32629), ls(32630), ls(32631), ls(32632)
	network_str, created_by_str, last_aired_str, next_aired_str, seasons_str, episodes_str = ls(32480), ls(32633), ls(32634), ls(32635), ls(32636), ls(32506)
	try:
		if media_type == 'movie':
			def _process_budget_revenue(info):
				if isinstance(info, int): info = '${:,}'.format(info)
				return info
			if 'tagline' in meta and meta['tagline']: append('[B]%s:[/B] %s' % (tagline_str, meta['tagline']))
			if 'alternative_titles' in meta and meta['alternative_titles']: append('[B]%s:[/B] %s' % ('Aliases', ', '.join(meta['alternative_titles'])))
			if 'status' in extra_info: append('[B]%s:[/B] %s' % (status_str, extra_info['status']))
			append('[B]%s:[/B] %s' % (premiered_str, meta['premiered']))
			append('[B]%s:[/B] %s (%s %s)' % (rating_str, meta['rating'], meta['votes'], votes_str))
			append('[B]%s:[/B] %d mins' % (runtime_str, int(float(meta['duration'])/60)))
			append('[B]%s:[/B] %s' % (genres_str, meta['genre']))
			if 'budget' in extra_info: append('[B]%s:[/B] %s' % (budget_str, _process_budget_revenue(extra_info['budget'])))
			if 'revenue' in extra_info: append('[B]%s:[/B] %s' % (revenue_str, _process_budget_revenue(extra_info['revenue'])))
			append('[B]%s:[/B] %s' % (director_str, meta['director']))
			append('[B]%s:[/B] %s' % (writer_str, meta['writer'] or 'N/A'))
			append('[B]%s:[/B] %s' % (studio_str, meta['studio'] or 'N/A'))
			if extra_info.get('collection_name'): append('[B]%s:[/B] %s' % (collection_str, extra_info['collection_name']))
			if extra_info.get('homepage'): append('[B]%s:[/B] %s' % (homepage_str, extra_info['homepage']))
		else:
			if 'type' in extra_info: append('[B]%s:[/B] %s' % (type_str, extra_info['type']))
			if 'alternative_titles' in meta and meta['alternative_titles']: append('[B]%s:[/B] %s' % ('Aliases', ', '.join(meta['alternative_titles'])))
			if 'status' in extra_info: append('[B]%s:[/B] %s' % (status_str, extra_info['status']))
			append('[B]%s:[/B] %s' % (premiered_str, meta['premiered']))
			append('[B]%s:[/B] %s (%s %s)' % (rating_str, meta['rating'], meta['votes'], votes_str))
			append('[B]%s:[/B] %d mins' % (runtime_str, int(float(meta['duration'])/60)))
			append('[B]%s:[/B] %s' % (classification_str, meta['mpaa']))
			append('[B]%s:[/B] %s' % (genres_str, meta['genre']))
			append('[B]%s:[/B] %s' % (network_str, meta['studio']))
			if 'created_by' in extra_info: append('[B]%s:[/B] %s' % (created_by_str, extra_info['created_by']))
			if extra_info.get('last_episode_to_air', False):
				last_ep = extra_info['last_episode_to_air']
				lastep_str = '[%s] S%.2dE%.2d - %s' % (last_ep['air_date'], last_ep['season_number'], last_ep['episode_number'], last_ep['name'])
				append('[B]%s:[/B] %s' % (last_aired_str, lastep_str))
			if extra_info.get('next_episode_to_air', False):
				next_ep = extra_info['next_episode_to_air']
				nextep_str = '[%s] S%.2dE%.2d - %s' % (next_ep['air_date'], next_ep['season_number'], next_ep['episode_number'], next_ep['name'])
				append('[B]%s:[/B] %s' % (next_aired_str, nextep_str))
			append('[B]%s:[/B] %s' % (seasons_str, meta['total_seasons']))
			append('[B]%s:[/B] %s' % (episodes_str, meta['total_aired_eps']))
			if 'homepage' in extra_info: append('[B]%s:[/B] %s' % (homepage_str, extra_info['homepage']))
	except: return notification(32574, 2000)
	return '[CR][CR]'.join(body)

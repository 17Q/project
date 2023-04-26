# -*- coding: utf-8 -*-
from metadata import tvshow_meta, season_episodes_meta, all_episodes_meta
from apis.trakt_api import trakt_fetch_collection_watchlist, trakt_get_hidden_items, trakt_get_my_calendar
from modules import kodi_utils, settings, watched_status as ws
from modules.utils import jsondate_to_datetime, adjust_premiered_date, make_day, get_datetime, title_key, date_difference, make_thread_list_enumerate
# logger = kodi_utils.logger

remove_meta_keys, set_view_mode, focus_index, external_browse = kodi_utils.remove_meta_keys, kodi_utils.set_view_mode, kodi_utils.focus_index, kodi_utils.external_browse
add_items, set_content, set_sort_method, end_directory = kodi_utils.add_items, kodi_utils.set_content, kodi_utils.set_sort_method, kodi_utils.end_directory
ls, make_listitem, build_url, dict_removals, sys = kodi_utils.local_string, kodi_utils.make_listitem, kodi_utils.build_url, kodi_utils.episode_dict_removals, kodi_utils.sys
get_art_provider, show_specials, calendar_sort_order, ignore_articles = settings.get_art_provider, settings.show_specials, settings.calendar_sort_order, settings.ignore_articles
nextep_content_settings, nextep_display_settings, calendar_focus_today = settings.nextep_content_settings, settings.nextep_display_settings, settings.calendar_focus_today
metadata_user_info, watched_indicators_info, show_unaired_info = settings.metadata_user_info, settings.watched_indicators, settings.show_unaired
date_offset_info, default_all_episodes = settings.date_offset, settings.default_all_episodes
single_ep_display_title, single_ep_format = settings.single_ep_display_title, settings.single_ep_format
tv_meta_function, season_meta_function, all_episodes_meta_function = tvshow_meta, season_episodes_meta, all_episodes_meta
adjust_premiered_date_function, jsondate_to_datetime_function = adjust_premiered_date, jsondate_to_datetime
date_difference_function, make_day_function, title_key_function, get_datetime_function = date_difference, make_day, title_key, get_datetime
get_progress_percent, get_watched_status, get_watched_info, get_bookmarks = ws.get_progress_percent, ws.get_watched_status_episode, ws.get_watched_info_tv, ws.get_bookmarks
get_in_progress_episodes, get_next_episodes, get_recently_watched = ws.get_in_progress_episodes, ws.get_next_episodes, ws.get_recently_watched
string, david_str, trakt_str, watched_str, unwatched_str, extras_str, options_str, clearprog_str = str, ls(32036), ls(32037), ls(32642), ls(32643), ls(32645), ls(32646), ls(32651)
upper = string.upper
poster_empty, fanart_empty = kodi_utils.empty_poster, kodi_utils.addon_fanart
run_plugin, unaired_label, tmdb_poster = 'RunPlugin(%s)', '[COLOR red][I]%s[/I][/COLOR]', 'https://image.tmdb.org/t/p/'

def build_episode_list(params):
	def _process():
		for item in episodes_data:
			try:
				cm = []
				listitem = make_listitem()
				set_properties = listitem.setProperties
				cm_append = cm.append
				item_get = item.get
				season, episode, ep_name = item_get('season'), item_get('episode'), item_get('title')
				episode_date, premiered = adjust_premiered_date_function(item_get('premiered'), adjust_hours)
				playcount, overlay = get_watched_status(watched_info, string(tmdb_id), season, episode)
				thumb = item_get('thumb', None) or fanart
				item.update({'trailer': trailer, 'tvshowtitle': title, 'premiered': premiered, 'genre': genre, 'duration': duration, 'mpaa': mpaa, 'studio': studio,
							'playcount': playcount, 'overlay': overlay})
				options_params = build_url({'mode': 'options_menu_choice', 'content': 'episode', 'tmdb_id': tmdb_id, 'season': season, 'episode': episode,
											'poster': show_poster, 'is_widget': is_widget})
				extras_params = build_url({'mode': 'extras_menu_choice', 'tmdb_id': tmdb_id, 'media_type': 'tvshow', 'is_widget': is_widget})
				url_params = build_url({'mode': 'play_media', 'media_type': 'episode', 'tmdb_id': tmdb_id, 'season': season, 'episode': episode})
				if not episode_date or current_date < episode_date:
					if not show_unaired: continue
					if season != 0:
						display, unaired = unaired_label % ep_name, True
						item['title'] = display
				else: display, unaired = ep_name, False
				cm_append((extras_str, run_plugin % extras_params))
				cm_append((options_str, run_plugin % options_params))
				clearprog_params, unwatched_params, watched_params = '', '', ''
				if not unaired:
					if playcount:
						if hide_watched: continue
						unwatched_params = build_url({'mode': 'mark_as_watched_unwatched_episode', 'action': 'mark_as_unwatched', 'tmdb_id': tmdb_id,
													'tvdb_id': tvdb_id, 'season': season, 'episode': episode,  'title': title, 'year': year})
						cm_append((unwatched_str % watched_title, run_plugin % unwatched_params))
					else:
						watched_params = build_url({'mode': 'mark_as_watched_unwatched_episode', 'action': 'mark_as_watched', 'tmdb_id': tmdb_id,
													'tvdb_id': tvdb_id, 'season': season, 'episode': episode,  'title': title, 'year': year})
						cm_append((watched_str % watched_title, run_plugin % watched_params))
					progress = get_progress_percent(bookmarks, tmdb_id, season, episode)
					if progress:
						clearprog_params = build_url({'mode': 'watched_unwatched_erase_bookmark', 'media_type': 'episode', 'tmdb_id': tmdb_id,
													'season': season, 'episode': episode, 'refresh': 'true'})
						cm_append((clearprog_str, run_plugin % clearprog_params))
						set_properties({'watchedprogress': progress, 'resumetime': progress, 'david_in_progress': 'true'})
				listitem.setLabel(display)
				listitem.addContextMenuItems(cm)
				listitem.setArt({'poster': show_poster, 'fanart': fanart, 'thumb': thumb, 'icon':thumb, 'banner': banner, 'clearart': clearart, 'clearlogo': clearlogo,
								'landscape': thumb, 'season.poster': season_poster, 'tvshow.poster': show_poster, 'tvshow.clearart': clearart, 'tvshow.clearlogo': clearlogo})
				listitem.setCast(cast + item_get('guest_stars', []))
				listitem.setUniqueIDs({'imdb': imdb_id, 'tmdb': string(tmdb_id), 'tvdb': string(tvdb_id)})
				listitem.setInfo('video', remove_meta_keys(item, dict_removals))
				if is_widget:
					set_properties({'david_widget': 'true', 'david_playcount': string(playcount), 'david_extras_params': extras_params, 'david_options_params': options_params,
									'david_unwatched_params': unwatched_params, 'david_watched_params': watched_params, 'david_clearprog_params': clearprog_params})
				else: set_properties({'david_widget': 'false'})
				yield (url_params, listitem, False)
			except: pass
	handle = int(sys.argv[1])
	try:
		item_list = []
		append = item_list.append
		meta_user_info, watched_indicators, watched_info, show_unaired, is_widget, fanart_enabled, hide_watched, current_date, adjust_hours, bookmarks = get_episode_info()
		poster_main, poster_backup, fanart_main, fanart_backup, clearlogo_main, clearlogo_backup = get_art_provider()
		all_episodes = True if params.get('season') == 'all' else False
		meta = tv_meta_function('tmdb_id', params.get('tmdb_id'), meta_user_info, current_date)
		meta_get = meta.get
		tmdb_id, tvdb_id, imdb_id = meta_get('tmdb_id'), meta_get('tvdb_id'), meta_get('imdb_id')
		title, year, rootname = meta_get('title'), meta_get('year'), meta_get('rootname')
		show_poster = meta_get(poster_main) or meta_get(poster_backup) or poster_empty
		fanart = meta_get(fanart_main) or meta_get(fanart_backup) or fanart_empty
		clearlogo = meta_get(clearlogo_main) or meta_get(clearlogo_backup) or ''
		if fanart_enabled: banner, clearart, landscape = meta_get('banner'), meta_get('clearart'), meta_get('landscape')
		else: banner, clearart, landscape = '', '', ''
		try:
			poster_path = [i['poster_path'] for i in meta_get('season_data') if i['season_number'] == int(params['season'])][0]
			season_poster =  ''.join([tmdb_poster, meta_user_info['image_resolution']['poster'], poster_path]) if poster_path is not None else show_poster
		except: season_poster = show_poster
		cast, mpaa, duration = meta_get('cast', []), meta_get('mpaa'), meta_get('duration')
		trailer, genre, studio = string(meta_get('trailer')), meta_get('genre'), meta_get('studio')
		tvshow_plot = meta_get('plot')
		watched_title = trakt_str if watched_indicators == 1 else david_str
		if all_episodes:
			episodes_data = all_episodes_meta_function(meta, meta_user_info)
			if not show_specials(): episodes_data = [i for i in episodes_data if not i['season'] == 0]
		else: episodes_data = season_meta_function(params['season'], meta, meta_user_info)
		add_items(handle, list(_process()))
	except: pass
	set_content(handle, 'episodes')
	set_sort_method(handle, 'episodes')
	end_directory(handle, False if is_widget else None)
	if not is_widget: set_view_mode('view.episodes', 'episodes')

def build_single_episode(list_type, data, handle):
	def _sort_results(items):
		if list_type_starts_with('next_episode'):
			def func(function):
				if sort_key == 'david_name': return title_key_function(function, ignore_articles_setting)
				elif sort_key == 'david_last_played': return jsondate_to_datetime_function(function, resformat)
				else: return function
			sort_key = nextep_settings['sort_key']
			sort_direction = nextep_settings['sort_direction']
			if nextep_settings['sort_airing_today_to_top']:
				airing_today = [i for i in items
								if date_difference_function(current_date, jsondate_to_datetime_function(i[1].getProperty('david_first_aired'), '%Y-%m-%d').date(), 0)]
				airing_today = sorted(airing_today, key=lambda i: i[1].getProperty('david_first_aired'))
				remainder = [i for i in items if not i in airing_today]
				remainder = sorted(remainder, key=lambda i: func(i[1].getProperty(sort_key)), reverse=sort_direction)
				unaired = [i for i in remainder if i[1].getProperty('david_unaired') == 'true']
				aired = [i for i in remainder if not i in unaired]
				remainder = aired + unaired
				items = airing_today + remainder
			else:
				items = sorted(items, key=lambda i: func(i[1].getProperty(sort_key)), reverse=sort_direction)
				unaired = [i for i in items if i[1].getProperty('david_unaired') == 'true']
				aired = [i for i in items if not i in unaired]
				items = aired + unaired
		else:
			items.sort(key=lambda k: int(k[1].getProperty('david_sort_order')))
			if list_type in ('trakt_calendar', 'trakt_recently_aired'):
				if list_type == 'trakt_calendar': reverse = calendar_sort_order() == 0
				else: reverse = True
				items.sort(key=lambda k: int(k[1].getProperty('david_sort_order')))
				items = sorted(items, key=lambda i: i[1].getProperty('david_first_aired'), reverse=reverse)
		return items
	def _process(item_position, ep_data):
		try:
			cm = []
			listitem = make_listitem()
			set_properties = listitem.setProperties
			cm_append = cm.append
			ep_data_get = ep_data.get
			meta = tv_meta_function('trakt_dict', ep_data_get('media_ids'), meta_user_info, current_date)
			if not meta: return
			meta_get = meta.get
			tmdb_id, tvdb_id, imdb_id = meta_get('tmdb_id'), meta_get('tvdb_id'), meta_get('imdb_id')
			title, year, rootname = meta_get('title'), meta_get('year'), meta_get('rootname')
			orig_season, orig_episode = ep_data_get('season'), ep_data_get('episode')
			show_poster = meta_get(poster_main) or meta_get(poster_backup) or poster_empty
			fanart = meta_get(fanart_main) or meta_get(fanart_backup) or fanart_empty
			clearlogo = meta_get(clearlogo_main) or meta_get(clearlogo_backup) or ''
			if fanart_enabled: banner, clearart, landscape = meta_get('banner'), meta_get('clearart'), meta_get('landscape')
			else: banner, clearart, landscape = '', '', ''
			try:
				poster_path = [i['poster_path'] for i in meta_get('season_data') if i['season_number'] == orig_season][0]
				season_poster =  ''.join([tmdb_poster, meta_user_info['image_resolution']['poster'], poster_path]) if poster_path is not None else show_poster
			except: season_poster = show_poster
			cast, mpaa, duration, tvshow_plot = meta_get('cast', []), meta_get('mpaa'), meta_get('duration'), meta_get('plot')
			trailer, genre, studio = string(meta_get('trailer')), meta_get('genre'), meta_get('studio')
			if list_type_starts_with('next_episode'):
				season_data = meta_get('season_data')
				curr_season_data = [i for i in season_data if i['season_number'] == orig_season][0]
				if orig_episode >= curr_season_data['episode_count']: orig_season, orig_episode, new_season = orig_season + 1, 1, True
				else: orig_episode, new_season = orig_episode + 1, False
			episodes_data = season_meta_function(orig_season, meta, meta_user_info)
			try: item = [i for i in episodes_data if i['episode'] == orig_episode][0]
			except: return
			item_get = item.get
			season, episode, ep_name = item_get('season'), item_get('episode'), item_get('title')
			str_season_zfill2, str_episode_zfill2 = string(season).zfill(2), string(episode).zfill(2)
			episode_date, premiered = adjust_premiered_date_function(item_get('premiered'), adjust_hours)
			if not episode_date or current_date < episode_date:
				if list_type_starts_with('next_episode'):
					if not nextep_include_unaired: return
					if episode_date and new_season and not date_difference_function(current_date, episode_date, 7): return
				elif not show_unaired: return
				unaired = True
				set_properties({'david_unaired': 'true'})
			else:
				unaired = False
				set_properties({'david_unaired': 'false'})
			playcount, overlay = get_watched_status(watched_info, string(tmdb_id), season, episode)
			if display_title == 0: title_string = ''.join([title, ': '])
			else: title_string = ''
			if display_title in (0,1): seas_ep = ''.join([str_season_zfill2, 'x', str_episode_zfill2, ' - '])
			else: seas_ep = ''
			if list_type_starts_with('next_episode'):
				unwatched = ep_data_get('unwatched', False)
				if episode_date: display_premiered = make_day_function(current_date, episode_date, date_format)
				else: display_premiered == 'UNKNOWN'
				airdate = ''.join(['[[COLOR magenta]', display_premiered, '[/COLOR]] ']) if nextep_include_airdate else ''
				highlight_color = nextep_unwatched_color if unwatched else nextep_unaired_color if unaired else ''
				italics_open, italics_close = ('[I]', '[/I]') if highlight_color else ('', '')
				if highlight_color: episode_info = ''.join([italics_open, '[COLOR', highlight_color, ']', seas_ep, ep_name, '[/COLOR]', italics_close])
				else: episode_info = ''.join([italics_open, seas_ep, ep_name, italics_close])
				display = ''.join([airdate, upper(title_string), episode_info])
			elif list_type == 'trakt_calendar':
				if episode_date: display_premiered = make_day_function(current_date, episode_date, date_format)
				else: display_premiered == 'UNKNOWN'
				display = ''.join(['[', display_premiered, '] ', upper(title_string), seas_ep, ep_name])
				if unaired:
					displays = display.split(']')
					display = ''.join(['[COLOR red]', displays[0], '][/COLOR]', displays[1]])
			else:
				color_tags = ('[COLOR red]', '[/COLOR]') if unaired else ('', '')
				display = ''.join([upper(title_string), color_tags[0], seas_ep, ep_name, color_tags[1]])
			thumb = item_get('thumb', None) or fanart
			item.update({'trailer': trailer, 'tvshowtitle': title, 'premiered': premiered, 'genre': genre, 'duration': duration,
						'mpaa': mpaa, 'studio': studio, 'playcount': playcount, 'overlay': overlay, 'title': display})
			options_params = build_url({'mode': 'options_menu_choice', 'content': 'episode_single', 'tmdb_id': tmdb_id, 'season': season, 'episode': episode,
										'poster': show_poster, 'is_widget': is_widget})
			extras_params = build_url({'mode': 'extras_menu_choice', 'tmdb_id': tmdb_id, 'media_type': 'tvshow', 'is_widget': is_widget})
			url_params = build_url({'mode': 'play_media', 'media_type': 'episode', 'tmdb_id': tmdb_id, 'season': season, 'episode': episode})
			cm_append((extras_str, run_plugin % extras_params))
			cm_append((options_str, run_plugin % options_params))
			clearprog_params, unwatched_params, watched_params = '', '', ''
			if not unaired:
				if playcount:
					if hide_watched: return
					unwatched_params = build_url({'mode': 'mark_as_watched_unwatched_episode', 'action': 'mark_as_unwatched', 'tmdb_id': tmdb_id,
												'tvdb_id': tvdb_id, 'season': season, 'episode': episode,  'title': title, 'year': year})
					cm_append((unwatched_str % watched_title, run_plugin % unwatched_params))
				else:
					watched_params = build_url({'mode': 'mark_as_watched_unwatched_episode', 'action': 'mark_as_watched', 'tmdb_id': tmdb_id,
												'tvdb_id': tvdb_id, 'season': season, 'episode': episode,  'title': title, 'year': year})
					cm_append((watched_str % watched_title, run_plugin % watched_params))
				progress = get_progress_percent(bookmarks, tmdb_id, season, episode)
				if progress:
					clearprog_params = build_url({'mode': 'watched_unwatched_erase_bookmark', 'media_type': 'episode', 'tmdb_id': tmdb_id,
												'season': season, 'episode': episode, 'refresh': 'true'})
					cm_append((clearprog_str, run_plugin % clearprog_params))
					set_properties({'WatchedProgress': progress, 'resumetime': progress, 'david_in_progress': 'true'})
			listitem.setLabel(display)
			listitem.addContextMenuItems(cm)
			listitem.setArt({'poster': show_poster, 'fanart': fanart, 'thumb': thumb, 'icon':thumb, 'banner': banner, 'clearart': clearart, 'clearlogo': clearlogo,
				'landscape': thumb, 'season.poster': season_poster, 'tvshow.clearart': clearart, 'tvshow.clearlogo': clearlogo, 'tvshow.landscape': thumb, 'tvshow.banner': banner})
			listitem.setCast(cast + item_get('guest_stars', []))
			listitem.setUniqueIDs({'imdb': imdb_id, 'tmdb': string(tmdb_id), 'tvdb': string(tvdb_id)})
			listitem.setInfo('video', remove_meta_keys(item, dict_removals))
			set_properties({'david_widget': 'false', 'david_first_aired': premiered, 'david_name': '%s - %sx%s' % (title, str_season_zfill2, str_episode_zfill2)})
			if list_type_starts_with('next_episode'):
				last_played = ep_data_get('last_played', resinsert)
				set_properties({'david_last_played': last_played})
			else: set_properties({'david_sort_order': string(item_position)})
			if is_widget:
				set_properties({'david_widget': 'true', 'david_playcount': string(playcount), 'david_extras_params': extras_params, 'david_options_params': options_params,
								'david_unwatched_params': unwatched_params, 'david_watched_params': watched_params, 'david_clearprog_params': clearprog_params})
			append((url_params, listitem, False))
		except: pass
	try:
		item_list = []
		append = item_list.append
		list_type_starts_with = list_type.startswith
		meta_user_info, watched_indicators, watched_info, show_unaired, is_widget, fanart_enabled, hide_watched, current_date, adjust_hours, bookmarks = get_episode_info()
		display_title, date_format, art_keys, all_episodes = get_single_episode_info()
		show_all_episodes = all_episodes in (1, 2)
		poster_main, poster_backup, fanart_main, fanart_backup, clearlogo_main, clearlogo_backup = art_keys
		ignore_articles_setting = ignore_articles()
		watched_title = trakt_str if watched_indicators == 1 else david_str
		if list_type_starts_with('next_episode'):
			nextep_settings, nextep_disp_settings = nextep_content_settings(), nextep_display_settings()
			nextep_unaired_color, nextep_unwatched_color = nextep_disp_settings['unaired_color'], nextep_disp_settings['unwatched_color']
			nextep_include_airdate, nextep_include_unaired = nextep_disp_settings['include_airdate'], nextep_settings['include_unaired']
			if watched_indicators == 1: resformat, resinsert = '%Y-%m-%dT%H:%M:%S.%fZ', '2000-01-01T00:00:00.000Z'
			else: resformat, resinsert = '%Y-%m-%d %H:%M:%S', '2000-01-01 00:00:00'
		threads = list(make_thread_list_enumerate(_process, data))
		[i.join() for i in threads]
		item_list = _sort_results(item_list)
		add_items(handle, item_list)
	except: pass
	set_content(handle, 'episodes')
	end_directory(handle, cacheToDisc=False)
	if not is_widget: set_view_mode('view.episodes', 'episodes')
	if list_type == 'trakt_calendar' and calendar_focus_today():
		try:
			today = upper('[%s]' % ls(32849))
			index = max([i for i, x in enumerate([i[1].getLabel() for i in item_list]) if today in x])
			focus_index(index)
		except: pass

def get_episode_info():
	meta_user_info = metadata_user_info()
	watched_indicators = watched_indicators_info()
	watched_info = get_watched_info(watched_indicators)
	show_unaired = show_unaired_info()
	is_widget = external_browse()
	fanart_enabled = meta_user_info['extra_fanart_enabled']
	hide_watched = is_widget and meta_user_info['widget_hide_watched']
	current_date = get_datetime_function()
	adjust_hours = date_offset_info()
	bookmarks = get_bookmarks(watched_indicators, 'episode')
	return meta_user_info, watched_indicators, watched_info, show_unaired, is_widget, fanart_enabled, hide_watched, current_date, adjust_hours, bookmarks

def get_single_episode_info():
	display_title = single_ep_display_title()
	date_format = single_ep_format()
	art_keys = get_art_provider()
	all_episodes = default_all_episodes()
	return display_title, date_format, art_keys, all_episodes

def build_in_progress_episode():
	data = get_in_progress_episodes()
	build_single_episode('progress', data, int(sys.argv[1]))

def build_recently_watched_episode():
	data = get_recently_watched('episode')[0]
	build_single_episode('recently_watched', data, int(sys.argv[1]))

def build_next_episode():
	nextep_settings = nextep_content_settings()
	include_unwatched = nextep_settings['include_unwatched']
	indicators = watched_indicators_info()
	watched_info = get_watched_info(indicators)
	data = get_next_episodes(watched_info)
	if indicators == 1:
		list_type = 'next_episode_trakt'
		try:
			hidden_data = trakt_get_hidden_items('progress_watched')
			data = [i for i in data if not i['media_ids']['tmdb'] in hidden_data]
		except: pass
	else: list_type = 'next_episode_david'
	if include_unwatched:
		try: unwatched = [{'media_ids': i['media_ids'], 'season': 1, 'episode': 0, 'unwatched': True} for i in trakt_fetch_collection_watchlist('watchlist', 'tvshow')]
		except: unwatched = []
		data += unwatched
	build_single_episode(list_type, data, int(sys.argv[1]))

def build_my_calendar(params):
	recently_aired = params.get('recently_aired', None)
	data = trakt_get_my_calendar(recently_aired, get_datetime())
	list_type = 'trakt_recently_aired' if recently_aired else 'trakt_calendar'
	data = sorted(data, key=lambda k: (k['sort_title'], k['first_aired']), reverse=True)
	build_single_episode(list_type, data, int(sys.argv[1]))
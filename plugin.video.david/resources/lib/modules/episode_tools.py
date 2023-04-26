# -*- coding: utf-8 -*-
from random import choice
from datetime import date
from windows import open_window
from apis.trakt_api import trakt_get_hidden_items
from metadata import tvshow_meta, season_episodes_meta, all_episodes_meta
from modules import kodi_utils, settings
from modules.sources import Sources
from modules.player import DavidPlayer
from modules.watched_status import get_next_episodes, get_watched_status_tvshow, get_watched_info_tv
from modules.utils import adjust_premiered_date, get_datetime, make_thread_list, title_key
# from modules.kodi_utils import logger

ls, sys, build_url, tv_meta_function, remove_meta_keys = kodi_utils.local_string, kodi_utils.sys, kodi_utils.build_url, tvshow_meta, kodi_utils.remove_meta_keys
dict_removals, make_listitem = kodi_utils.tvshow_dict_removals, kodi_utils.make_listitem
poster_empty, fanart_empty = kodi_utils.empty_poster, kodi_utils.addon_fanart
included_str, excluded_str, extras_str, browse_str, heading = ls(32804).upper(), ls(32805).upper(), ls(32645), ls(32652), ls(32806)
string = str

def build_next_episode_manager():
	def build_content(item):
		try:
			cm = []
			listitem = make_listitem()
			set_properties = listitem.setProperties
			cm_append = cm.append
			meta = tv_meta_function('trakt_dict', item['media_ids'], meta_user_info, current_date)
			meta_get = meta.get
			tmdb_id, tvdb_id, imdb_id = meta_get('tmdb_id'), meta_get('tvdb_id'), meta_get('imdb_id')
			total_aired_eps = meta_get('total_aired_eps')
			total_seasons = meta_get('total_seasons')
			title = meta_get('title')
			poster = meta_get(poster_main) or meta_get(poster_backup) or poster_empty
			fanart = meta_get(fanart_main) or meta_get(fanart_backup) or fanart_empty
			clearlogo = meta_get(clearlogo_main) or meta_get(clearlogo_backup) or ''
			playcount, overlay, total_watched, total_unwatched = get_watched_status_tvshow(watched_info, string(tmdb_id), total_aired_eps)
			meta.update({'playcount': playcount, 'overlay': overlay})
			if tmdb_id in exclude_list: color, action, status, sort_value = 'red', 'unhide', excluded_str, 1
			else: color, action, status, sort_value = 'green', 'hide', included_str, 0
			display = '[COLOR=%s][%s][/COLOR] %s' % (color, status, title)
			extras_params = {'mode': 'extras_menu_choice', 'tmdb_id': tmdb_id, 'media_type': 'tvshow', 'is_widget': 'False'}
			url_params = {'mode': 'trakt.hide_unhide_trakt_items', 'action': action, 'media_type': 'shows', 'media_id': imdb_id, 'section': 'progress_watched'}
			if fanart_enabled: banner, clearart, landscape = meta_get('banner'), meta_get('clearart'), meta_get('landscape')
			else: banner, clearart, landscape = '', '', ''
			url = build_url(url_params)
			if show_all_episodes:
				if all_episodes == 1 and total_seasons > 1: browse_params = {'mode': 'build_season_list', 'tmdb_id': tmdb_id}
				else: browse_params = {'mode': 'build_episode_list', 'tmdb_id': tmdb_id, 'season': 'all'}
			else: browse_params = {'mode': 'build_season_list', 'tmdb_id': tmdb_id}
			cm_append((extras_str, 'RunPlugin(%s)' % build_url(extras_params)))
			cm_append((browse_str,'Container.Update(%s)' % build_url(browse_params)))
			listitem.setLabel(display)
			set_properties({'watchedepisodes': string(total_watched), 'unwatchedepisodes': string(total_unwatched),
							'totalepisodes': string(total_aired_eps), 'totalseasons': string(total_seasons)})
			listitem.addContextMenuItems(cm)
			listitem.setArt({'poster': poster, 'fanart': fanart, 'icon': poster, 'banner': banner, 'clearart': clearart, 'clearlogo': clearlogo, 'landscape': landscape,
							'tvshow.clearart': clearart, 'tvshow.clearlogo': clearlogo, 'tvshow.landscape': landscape, 'tvshow.banner': banner})
			listitem.setCast(meta_get('cast', []))
			listitem.setUniqueIDs({'imdb': imdb_id, 'tmdb': string(tmdb_id), 'tvdb': string(tvdb_id)})
			listitem.setInfo('video', remove_meta_keys(meta, dict_removals))
			append({'listitem': (url, listitem, False), 'sort_value': sort_value, 'sort_title': title})
		except: pass
	handle = int(sys.argv[1])
	list_items = []
	append = list_items.append
	meta_user_info = settings.metadata_user_info()
	current_date = get_datetime()
	watched_indicators = settings.watched_indicators()
	watched_info = get_watched_info_tv(watched_indicators)
	all_episodes = settings.default_all_episodes()
	open_extras = settings.extras_open_action('tvshow')
	show_list = get_next_episodes(watched_info)
	poster_main, poster_backup, fanart_main, fanart_backup, clearlogo_main, clearlogo_backup = settings.get_art_provider()
	fanart_enabled = meta_user_info['extra_fanart_enabled']
	try: exclude_list = trakt_get_hidden_items('progress_watched')
	except: exclude_list = []
	show_all_episodes = True if all_episodes in (1, 2) else False
	threads = list(make_thread_list(build_content, show_list))
	[i.join() for i in threads]
	item_list = sorted(list_items, key=lambda k: (k['sort_value'], title_key(k['sort_title'], settings.ignore_articles())), reverse=False)
	item_list = [i['listitem'] for i in item_list]
	kodi_utils.add_dir({'mode': 'nill'}, '[I][COLOR=grey2]%s[/COLOR][/I]' % heading.upper(), handle, iconImage='settings', isFolder=False)
	kodi_utils.add_items(handle, item_list)
	kodi_utils.set_content(handle, 'tvshows')
	kodi_utils.end_directory(handle, cacheToDisc=False)
	if not kodi_utils.external_browse(): kodi_utils.set_view_mode('view.main', 'tvshows')
	kodi_utils.focus_index(1)

def nextep_playback_info(meta):
	def _build_next_episode_play():
		ep_data = season_episodes_meta(season, meta, settings.metadata_user_info())
		if not ep_data: return 'no_next_episode'
		ep_data = [i for i in ep_data if i['episode'] == episode][0]
		airdate = ep_data['premiered']
		d = airdate.split('-')
		episode_date = date(int(d[0]), int(d[1]), int(d[2]))
		if current_date < episode_date: return 'no_next_episode'
		custom_title = meta_get('custom_title', None)
		title = custom_title or meta_get('title')
		display_name = '%s - %dx%.2d' % (title, int(season), int(episode))
		meta.update({'media_type': 'episode', 'rootname': display_name, 'season': season, 'ep_name': ep_data['title'],
					'episode': episode, 'premiered': airdate, 'plot': ep_data['plot']})
		url_params = {'mode': 'play_media', 'media_type': 'episode', 'tmdb_id': tmdb_id, 'tvshowtitle': meta_get('rootname'), 'season': season,
					'episode': episode, 'background': 'true'}
		if custom_title: url_params['custom_title'] = custom_title
		if 'custom_year' in meta: url_params['custom_year'] = meta_get('custom_year')
		return url_params
	meta_get = meta.get
	tmdb_id, current_season, current_episode = meta_get('tmdb_id'), int(meta_get('season')), int(meta_get('episode'))
	try:
		current_date = get_datetime()
		season_data = meta_get('season_data')
		curr_season_data = [i for i in season_data if i['season_number'] == current_season][0]
		season = current_season if current_episode < curr_season_data['episode_count'] else current_season + 1
		episode = current_episode + 1 if current_episode < curr_season_data['episode_count'] else 1
		nextep_info = _build_next_episode_play()
	except: nextep_info = 'error'
	return meta, nextep_info

def execute_nextep(meta, nextep_settings):
	def _get_nextep_params():
		nextep_params = nextep_playback_info(meta)
		return nextep_params
	def _get_nextep_url():
		Sources().playback_prep(nextep_params)
		return kodi_utils.get_property('david_background_url')
	def _confirm_threshold():
		nextep_threshold = nextep_settings['threshold']
		if nextep_threshold == 0: return True
		try: current_number = int(kodi_utils.get_property('david_total_autoplays'))
		except: current_number = 1
		if current_number == nextep_threshold:
			current_number = 1
			kodi_utils.set_property('david_total_autoplays', str(current_number))
			if open_window(('windows.next_episode', 'NextEpisode'), 'next_episode.xml', meta=nextep_meta, function='confirm'): return True
			else:
				kodi_utils.notification(32736, 1500)
				return False
		else:
			current_number += 1
			kodi_utils.set_property('david_total_autoplays', str(current_number))
			return True
	def _continue_action():
		if run_popup: action = open_window(('windows.next_episode', 'NextEpisode'), 'next_episode.xml', meta=nextep_meta, function='next_ep')
		else: action = 'close'
		return action
	def _control():
		confirm_threshold, final_action = False, 'cancel'
		while player.isPlayingVideo():
			try:
				total_time = player.getTotalTime()
				curr_time = player.getTime()
				remaining_time = round(total_time - curr_time)
				if remaining_time <= nextep_threshold_check:
					if not confirm_threshold:
						confirm_threshold = _confirm_threshold()
						if not confirm_threshold:
							final_action = 'cancel'
							break
				if remaining_time <= display_nextep_popup:
					final_action = _continue_action()
					break
				kodi_utils.sleep(200)
			except: pass
		return final_action
	kodi_utils.clear_property('david_background_url')
	player = DavidPlayer()
	run_popup, display_nextep_popup = nextep_settings['run_popup'], nextep_settings['window_time']
	nextep_prep, nextep_threshold_check = nextep_settings['start_prep'], nextep_settings['threshold_check']
	nextep_meta, nextep_params = _get_nextep_params()
	if nextep_params == 'error': return kodi_utils.notification(32574, 3000)
	elif nextep_params == 'no_next_episode': return
	nextep_url = _get_nextep_url()
	if not nextep_url: return kodi_utils.notification(32760, 3000)
	action = _control()
	if action == 'cancel': return kodi_utils.notification(' '.join([ls(32071), ls(32736)]), 3000)
	elif action == 'play': player.stop()
	elif action == 'close':
		if not run_popup: kodi_utils.notification('%s %s S%02dE%02d' % (ls(32801), nextep_meta['title'], nextep_meta['season'], nextep_meta['episode']), 6500, nextep_meta['poster'])
		while player.isPlayingVideo(): kodi_utils.sleep(100)
	player.run(nextep_url)

def get_random_episode(tmdb_id, continual=False):
	meta_user_info, adjust_hours, current_date = settings.metadata_user_info(), settings.date_offset(), get_datetime()
	tmdb_key = str(tmdb_id)
	meta = tvshow_meta('tmdb_id', tmdb_id, meta_user_info, current_date)
	try:
		episodes_data = all_episodes_meta(meta, meta_user_info)
		episodes_data = [i for i in episodes_data if not i['season']  == 0 and adjust_premiered_date(i['premiered'], adjust_hours)[0] <= current_date]
	except: episodes_data = []
	if not episodes_data: return None
	if continual:
		episode_list = []
		try:
			episode_history = kodi_utils.json.loads(kodi_utils.get_property('david_random_episode_history'))
			if tmdb_key in episode_history: episode_list = episode_history[tmdb_key]
			else: kodi_utils.set_property('david_random_episode_history', '')
		except: pass
		first_run = len(episode_list) == 0
		episodes_data = [i for i in episodes_data if not i in episode_list]
		if not episodes_data:
			kodi_utils.set_property('david_random_episode_history', '')
			return get_random_episode(tmdb_id, continual=True)
	else: first_run = True
	chosen_episode = choice(episodes_data)
	if continual:
		episode_list.append(chosen_episode)
		episode_history = {str(tmdb_id): episode_list}
		kodi_utils.set_property('david_random_episode_history', kodi_utils.json.dumps(episode_history))
	title, season, episode = meta['title'], int(chosen_episode['season']), int(chosen_episode['episode'])
	query = title + ' S%.2dE%.2d' % (season, episode)
	display_name = '%s - %dx%.2d' % (title, season, episode)
	ep_name, plot = chosen_episode['title'], chosen_episode['plot']
	try: premiered = adjust_premiered_date(chosen_episode['premiered'], adjust_hours)[1]
	except: premiered = chosen_episode['premiered']
	meta.update({'media_type': 'episode', 'rootname': display_name, 'season': season, 'episode': episode, 'premiered': premiered, 'ep_name': ep_name, 'plot': plot})
	if continual: meta['random_continual'] = 'true'
	else: meta['random'] = 'true'
	url_params = {'mode': 'play_media', 'media_type': 'episode', 'tmdb_id': meta['tmdb_id'], 'query': query,
					'tvshowtitle': meta['rootname'], 'season': season, 'episode': episode, 'autoplay': 'true', 'meta': kodi_utils.json.dumps(meta)}
	if not first_run: url_params['background'] = 'true'
	return url_params

def play_random(tmdb_id):
	url_params = get_random_episode(tmdb_id)
	if not url_params: return {'pass': True}
	return kodi_utils.run_plugin(url_params)

def play_random_continual(tmdb_id):
	url_params = get_random_episode(tmdb_id, continual=True)
	if not url_params: return {'pass': True}
	player = DavidPlayer()
	Sources().playback_prep(url_params)
	url = kodi_utils.get_property('david_background_url')
	kodi_utils.clear_property('david_background_url')
	while player.isPlayingVideo(): kodi_utils.sleep(100)
	player.run(url)



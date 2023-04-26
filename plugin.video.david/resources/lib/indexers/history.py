# -*- coding: utf-8 -*-
from caches.main_cache import main_cache
from modules import kodi_utils
# logger = kodi_utils.logger

ls, sys, build_url, make_listitem, get_icon = kodi_utils.local_string, kodi_utils.sys, kodi_utils.build_url, kodi_utils.make_listitem, kodi_utils.get_icon
add_dir, add_items, set_content, end_directory = kodi_utils.add_dir, kodi_utils.add_items, kodi_utils.set_content, kodi_utils.end_directory
external_browse, set_view_mode, unquote = kodi_utils.external_browse, kodi_utils.set_view_mode, kodi_utils.unquote
icon, fanart = get_icon('search_history'), kodi_utils.addon_fanart
history_str, remove_str = '[B]%s:[/B] [I]%s[/I]' % (ls(32486).upper(), '%s'), ls(32786)
new_search_str = '[B]%s %s...[/B]' % (ls(32857).upper(), ls(32450).upper())
mode_dict = {'movie': ('movie_queries', {'mode': 'get_search_term', 'media_type': 'movie'}),
			'tvshow': ('tvshow_queries', {'mode': 'get_search_term', 'media_type': 'tv_show'}),
			'people': ('people_queries', {'mode': 'get_search_term', 'search_type': 'people'}),
			'furk_video': ('furk_video_queries', {'mode': 'get_search_term', 'search_type': 'furk_direct', 'media_type': 'video'}),
			'easynews_video': ('easynews_video_queries', {'mode': 'get_search_term', 'search_type': 'easynews_video'}),
			'imdb_keyword_movie': ('imdb_keyword_movie_queries', {'mode': 'get_search_term', 'search_type': 'imdb_keyword', 'media_type': 'movie'}),
			'imdb_keyword_tvshow': ('imdb_keyword_tvshow_queries', {'mode': 'get_search_term', 'search_type': 'imdb_keyword', 'media_type': 'tvshow'}),
			'tmdb_collections': ('tmdb_collections_queries', {'mode': 'get_search_term', 'search_type': 'tmdb_collections', 'media_type': 'movie'})}

def search_history(params):
	def _builder():
		for h in main_cache.get(setting_id):
			try:
				cm = []
				query = unquote(h)
				url_params['query'] = query
				display = history_str % query
				url = build_url(url_params)
				cm.append((remove_str,'RunPlugin(%s)' % build_url({'mode': 'remove_from_history', 'setting_id':setting_id, 'query': query})))
				listitem = make_listitem()
				listitem.setLabel(display)
				listitem.setArt({'icon': icon, 'poster': icon, 'thumb': icon, 'fanart': fanart, 'banner': icon})
				listitem.addContextMenuItems(cm)
				yield (url, listitem, False)
			except: pass
	handle = int(sys.argv[1])
	setting_id, action_dict = mode_dict[params['action']]
	url_params = dict(action_dict)
	add_dir(action_dict, new_search_str, handle, iconImage='search_new', isFolder=False)
	try: add_items(handle, list(_builder()))
	except: pass
	set_content(handle, '')
	end_directory(handle, False)
	if not external_browse(): set_view_mode('view.main', '')
	
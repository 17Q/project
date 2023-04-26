# -*- coding: utf-8 -*-
from apis import trakt_api
from indexers.movies import Movies
from indexers.tvshows import TVShows
from modules import kodi_utils
from modules.utils import paginate_list
from modules.settings import paginate, page_limit
# logger = kodi_utils.logger

ls, sys, make_listitem, build_url = kodi_utils.local_string, kodi_utils.sys, kodi_utils.make_listitem, kodi_utils.build_url
trakt_icon, fanart = kodi_utils.get_icon('trakt'), kodi_utils.addon_fanart
add2menu_str, add2folder_str, likelist_str, unlikelist_str = ls(32730), ls(32731), ls(32776), ls(32783)
newlist_str, deletelist_str, nextpage_str, jump2_str = ls(32780), ls(32781), ls(32799), ls(32964)

def search_trakt_lists(params):
	def _builder():
		for item in lists:
			try:
				list_key = item['type']
				list_info = item[list_key]
				if list_key == 'officiallist': continue
				item_count = list_info['item_count']
				if list_info['privacy'] in ('private', 'friends') or item_count == 0: continue
				name, user, slug = list_info['name'], list_info['username'], list_info['ids']['slug']
				if not slug: continue
				cm = []
				cm_append = cm.append
				url = build_url({'mode': 'trakt.list.build_trakt_list', 'user': user, 'slug': slug})
				cm_append((add2menu_str,'RunPlugin(%s)' % build_url({'mode': 'menu_editor.add_external', 'name': name, 'iconImage': 'trakt'})))
				cm_append((add2folder_str,'RunPlugin(%s)' % build_url({'mode': 'menu_editor.shortcut_folder_add_item', 'name': name, 'iconImage': 'trakt'})))
				cm_append((likelist_str,'RunPlugin(%s)' % build_url({'mode': 'trakt.trakt_like_a_list', 'user': user, 'list_slug': slug})))
				cm_append((unlikelist_str,'RunPlugin(%s)' % build_url({'mode': 'trakt.trakt_unlike_a_list', 'user': user, 'list_slug': slug})))
				display = '[B]%s[/B] | [I]%s (x%s)[/I]' % (name.upper(), user, str(item_count))
				listitem = make_listitem()
				listitem.setLabel(display)
				listitem.setArt({'icon': trakt_icon, 'poster': trakt_icon, 'thumb': trakt_icon, 'fanart': fanart, 'banner': trakt_icon})
				listitem.addContextMenuItems(cm)
				yield (url, listitem, True)
			except: pass
	try:
		handle = int(sys.argv[1])
		mode = params.get('mode')
		page = params.get('new_page', '1')
		search_title = params.get('search_title', None) or kodi_utils.dialog.input(ls(32036))
		if not search_title: return
		lists, pages = trakt_api.trakt_search_lists(search_title, page)
		kodi_utils.add_items(handle, list(_builder()))
		if pages > page: kodi_utils.add_dir({'mode': mode, 'search_title': search_title, 'new_page': str(int(page) + 1)}, nextpage_str, handle, iconImage='item_next')
	except: pass
	kodi_utils.set_content(handle, 'files')
	kodi_utils.end_directory(handle)
	if not kodi_utils.external_browse(): kodi_utils.set_view_mode('view.main')

def get_trakt_lists(params):
	def _process():
		for item in lists:
			try:
				if list_type == 'liked_lists': item = item['list']
				cm = []
				cm_append = cm.append
				name, user, slug = item['name'], item['user']['ids']['slug'], item['ids']['slug']
				item_count = item.get('item_count', None)
				if list_type == 'liked_lists': display = '%s (x%s) - [I]%s[/I]' % (name, item_count, user) if item_count else '%s - [I]%s[/I]' % (name, user)
				else: display = '%s (x%s)' % (name, item_count) if item_count else name
				url = build_url({'mode': 'trakt.list.build_trakt_list', 'user': user, 'slug': slug, 'list_type': list_type})
				cm_append((add2menu_str,'RunPlugin(%s)' % build_url({'mode': 'menu_editor.add_external', 'name': display, 'iconImage': 'trakt'})))
				cm_append((add2folder_str,'RunPlugin(%s)' % build_url({'mode': 'menu_editor.shortcut_folder_add_item', 'name': display, 'iconImage': 'trakt'})))
				if list_type == 'liked_lists': cm_append((unlikelist_str,'RunPlugin(%s)' % build_url({'mode': 'trakt.trakt_unlike_a_list', 'user': user, 'list_slug': slug})))
				else:
					cm_append((newlist_str,'RunPlugin(%s)' % build_url({'mode': 'trakt.make_new_trakt_list'})))
					cm_append((deletelist_str,'RunPlugin(%s)' % build_url({'mode': 'trakt.delete_trakt_list', 'user': user, 'list_slug': slug})))
				listitem = make_listitem()
				listitem.setLabel(display)
				listitem.setArt({'icon': trakt_icon, 'poster': trakt_icon, 'thumb': trakt_icon, 'fanart': fanart, 'banner': trakt_icon})
				listitem.addContextMenuItems(cm, replaceItems=False)
				yield (url, listitem, True)
			except: pass
	try:
		handle = int(sys.argv[1])
		list_type = params['list_type']
		lists = trakt_api.trakt_get_lists(list_type)
		kodi_utils.add_items(handle, list(_process()))
	except: pass
	kodi_utils.set_content(handle, 'files')
	kodi_utils.set_sort_method(handle, 'label')
	kodi_utils.end_directory(handle)
	if not kodi_utils.external_browse(): kodi_utils.set_view_mode('view.main')

def get_trakt_trending_popular_lists(params):
	def _process():
		for _list in lists:
			try:
				cm = []
				cm_append = cm.append
				item = _list['list']
				item_count = item.get('item_count', None)
				if item['user']['private'] or item_count == 0: continue
				name, user, slug = item['name'], item['user']['ids']['slug'], item['ids']['slug']
				if not slug: continue
				if item['type'] == 'official': user = 'Trakt Official'
				if not user: continue
				if item_count: display_name = '%s (x%s) - [I] %s[/I]' % (name, item_count, user)
				else: display_name = '%s - [I] %s[/I]' % (name, user)
				url = build_url({'mode': 'trakt.list.build_trakt_list', 'user': user, 'slug': slug, 'list_type': 'user_lists'})
				listitem = make_listitem()
				listitem.setLabel(display_name)
				listitem.setArt({'icon': trakt_icon, 'poster': trakt_icon, 'thumb': trakt_icon, 'fanart': fanart, 'banner': trakt_icon})
				cm_append((add2menu_str,'RunPlugin(%s)' % build_url({'mode': 'menu_editor.add_external', 'name': name, 'iconImage': 'trakt'})))
				cm_append((add2folder_str,'RunPlugin(%s)' % build_url({'mode': 'menu_editor.shortcut_folder_add_item', 'name': name, 'iconImage': 'trakt'})))
				if not user == 'Trakt Official':
					cm_append((likelist_str,'RunPlugin(%s)' % build_url({'mode': 'trakt.trakt_like_a_list', 'user': user, 'list_slug': slug})))
					cm_append((unlikelist_str,'RunPlugin(%s)' % build_url({'mode': 'trakt.trakt_unlike_a_list', 'user': user, 'list_slug': slug})))
				listitem.addContextMenuItems(cm)
				yield (url, listitem, True)
			except: pass
	try:
		handle = int(sys.argv[1])
		list_type = params['list_type']
		lists = trakt_api.trakt_trending_popular_lists(list_type)
		kodi_utils.add_items(handle, list(_process()))
	except: pass
	kodi_utils.set_content(handle, 'files')
	kodi_utils.end_directory(handle)
	if not kodi_utils.external_browse(): kodi_utils.set_view_mode('view.main')

def build_trakt_list(params):
	handle = int(sys.argv[1])
	is_widget = kodi_utils.external_browse()
	content = 'movies'
	try:
		user, slug, list_type = params.get('user'), params.get('slug'), params.get('list_type')
		page_no = int(params.get('new_page', '1'))
		result = trakt_api.get_trakt_list_contents(list_type, user, slug)
		movie_list = [{'media_ids': i['movie']['ids'], 'title': i['movie']['title']} for i in result if i['type'] == 'movie']
		tvshow_list = [{'media_ids': i['show']['ids'], 'title': i['show']['title']} for i in result if i['type'] == 'show']
		if len(movie_list) > len(tvshow_list): content, view_mode, trakt_list, function = 'movies', 'view.movies', movie_list, Movies
		else: content, view_mode, trakt_list, function = 'tvshows', 'view.tvshows', tvshow_list, TVShows
		if paginate():
			limit = page_limit()
			process_list, total_pages = paginate_list(trakt_list, page_no, limit)
		else: process_list, total_pages = trakt_list, 1
		if total_pages > 2 and not is_widget:
			kodi_utils.add_dir({'mode': 'build_navigate_to_page', 'media_type': 'Media', 'user': user, 'slug': slug, 'current_page': page_no, 'total_pages': total_pages,
							'transfer_mode': 'trakt.list.build_trakt_list', 'list_type': list_type}, jump2_str, handle, iconImage='item_jump', isFolder=False)
		item_list = function({'list': [i['media_ids'] for i in process_list], 'id_type': 'trakt_dict'}).worker()
		item_list.sort(key=lambda k: int(k[1].getProperty('david_sort_order')))
		kodi_utils.add_items(handle, item_list)
		if total_pages > page_no:
			kodi_utils.add_dir({'mode': 'trakt.list.build_trakt_list', 'user': user, 'slug': slug, 'new_page': str(page_no + 1), 'list_type': list_type},
								nextpage_str, handle, iconImage='item_next', isFolder=True)
	except: pass
	kodi_utils.set_content(handle, content)
	kodi_utils.end_directory(handle, False if is_widget else None)
	if params.get('refreshed'): kodi_utils.sleep(1500)
	if not is_widget: kodi_utils.set_view_mode(view_mode, content)

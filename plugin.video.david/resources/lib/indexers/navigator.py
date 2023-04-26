# -*- coding: utf-8 -*-
import os
from caches.navigator_cache import navigator_cache as nc
from modules import meta_lists as ml, kodi_utils as k, settings as s
from modules.debrid import debrid_enabled
from modules.utils import clean_file_name, normalize
from modules.watched_status import get_recently_watched
# logger = k.logger

get_setting = k.get_setting
tp, ls, sys, build_url, notification, addon, make_listitem, list_dirs = k.translate_path, k.local_string, k.sys, k.build_url, k.notification, k.addon, k.make_listitem, k.list_dirs
add_item, set_content, end_directory, set_view_mode, add_items, set_sort_method = k.add_item, k.set_content, k.end_directory, k.set_view_mode, k.add_items, k.set_sort_method
json, external_browse, close_all_dialog, sleep, execute_builtin, external_browse = k.json, k.external_browse, k.close_all_dialog, k.sleep, k.execute_builtin, k.external_browse
download_directory, furk_active, easynews_active, source_folders_directory, get_icon = s.download_directory, s.furk_active, s.easynews_active, s.source_folders_directory, k.get_icon
get_shortcut_folders, currently_used_list, get_shortcut_folder_contents, fanart = nc.get_shortcut_folders, nc.currently_used_list, nc.get_shortcut_folder_contents, k.addon_fanart
act_str, fl_str, vid_str, fl_str, se_str, acc_str, dl_str, people_str, keywords_str = ls(32489), ls(32490), ls(32491), ls(32493), ls(32450), ls(32494), ls(32107), ls(32507), ls(32092)
tools_str, manager_str, changelog_str, ext_str, short_str, source_str, cl_dbs_str, langinv_str = ls(32456), ls(32513), ls(32508), ls(32118), ls(32514), ls(32515), ls(32512), ls(33017)
user_str, ml_str, ll_str, rec_str, cal_str, lv_str, lu_str, k_str, genre_select_str = ls(32065), ls(32454), ls(32502), ls(32503), ls(32081), ls(32509), ls(32853), ls(32538), ls(32847)
recent_added_str, recently_aired_str, random_str, episodes_str, settings_str, multi_str, q_str = ls(32498), ls(32505), ls(32504), ls(32506), ls(32247), ls(32789), ls(32522)
log_utils_str, tips_use_str, views_str, updates_str, david_str, all_str, cache_str, clean_str = ls(32777), ls(32518), ls(32510), ls(32196), ls(32036), ls(32129), ls(32524), ls(32526)
discover_str, history_str, help_str, furk_str, easy_str, rd_str, pm_str, ad_str = ls(32451), ls(32486), ls(32487), ls(32069), ls(32070), ls(32054), ls(32061), ls(32063)
cloud_str, clca_str, trakt_str, imdb_str, coll_str, wlist_str, ls_str, fav_str = ls(32496), ls(32497), ls(32037), ls(32064), ls(32499), ls(32500), ls(32501), ls(32453)
_in_str, mov_str, tv_str, edit_str, browse_str, add_menu_str, s_folder_str = ls(32484), ls(32028), ls(32029), ls(32705), ls(32706), ls(32730), ls(32731)
root_str, season_str, images_str, make_short_str, delete_str = ls(32457), ls(32537), ls(32798), ls(32702), ls(32703)
new_str, spot_str, tips_str = ls(32857).upper(), ls(32858).upper(), ls(32546).upper()
clean_set_cache_str, search_str = '[B]%s:[/B] %s %s %s' % (settings_str.upper(), clean_str, settings_str, cache_str), '%s %s' % (se_str, history_str)
clear_all_str, clear_meta_str, clear_list_str, clear_trakt_str = clca_str % all_str, clca_str % ls(32527), clca_str % ls_str, clca_str % trakt_str
sources_folders_str, downloads_ins, because_str = '[B]%s (%s): %s[/B]\n     [COLOR=%s][I]%s[/I][/COLOR]', _in_str % (dl_str.upper(), '%s'), '[I]%s[/I]  [B]%s[/B]' % (ls(32474), '%s')
premium_files_str, ep_lists_str, clear_all_amble = ls(32485), '%s %s' % (episodes_str, ls_str), '[B][I][COLOR=grey] (%s %s & %s)[/COLOR][/I][/B]' % (ls(32189), fav_str, search_str)
clear_ad_str, clear_fav_str, clear_search_str, clear_all = clca_str % ad_str, clca_str % fav_str, clca_str % search_str, '[B]%s:[/B] %s' % (clear_all_str.upper(), clear_all_amble)
movh_str, tvh_str, tips_ins = '%s %s' % (mov_str, history_str), '%s %s' % (tv_str, history_str), '[B]%s[/B]: %s'  % (tips_str, '%s')
clean_databases_str, clean_all_str = '%s %s' % (clean_str, ls(32003)), '[B]%s:[/B] %s %s' % (settings_str.upper(), clean_str, settings_str)
kw_mov, kw_tv, col_str = '%s %s (%s)' % (imdb_str, keywords_str, mov_str), '%s %s (%s)' % (imdb_str, keywords_str, tv_str), '%s %s (%s)' % (mov_str, coll_str, ls(32068))
clear_imdb_str, clint_str, clext_str, clear_rd_str, clear_pm_str = clca_str % imdb_str, clca_str % ls(32096), clca_str % ext_str, clca_str % rd_str, clca_str % pm_str
mrec_str, mran_str, changelog_log_viewer_str = '%s %s' % (recent_added_str, mov_str), '%s %s' % (random_str, mov_str), '%s & %s' % (changelog_str, log_utils_str)
tvrec_str, tvran_str, ra_str = '%s %s' % (recent_added_str, tv_str), '%s %s' % (random_str, tv_str), '%s %s' % (recently_aired_str, episodes_str)
tu_str, pu_str, sea_str = '%s %s %s' % (ls(32458), user_str, ls_str), '%s %s %s' % (ls(32459), user_str, ls_str), '%s %s' % (ls(32477), ls_str)
shortcut_manager_str, source_manager_str = '%s %s' % (short_str, manager_str), '%s %s' % (source_str, manager_str)
klv_h_str, klu_h_str = '[B]%s[/B]: %s %s' % (log_utils_str.upper(), k_str, lv_str), '[B]%s[/B]: %s' % (log_utils_str.upper(), lu_str)
klvo_h_str = '[B]%s[/B]: %s %s (%s)' % (log_utils_str.upper(), k_str, lv_str, ls(32214))
trakt_watchlist_str, imdb_watchlist_str, imdb_lists_str = '%s %s' % (trakt_str, wlist_str), '%s %s' % (imdb_str, wlist_str), '%s %s' % (imdb_str, ls_str)
clear_info_ins, set_view_modes_ins = _in_str % (cache_str.upper(), '%s'), _in_str % (views_str.upper(), '%s')
alldebrid_ins, my_content_trakt_ins, my_content_imdb_ins = _in_str % (ad_str.upper(), '%s'), _in_str % (trakt_str.upper(), '%s'), _in_str % (imdb_str.upper(), '%s')
imdb_lists_ins, tools_ins, settings_ins = _in_str % (imdb_lists_str.upper(), '%s'), _in_str % (tools_str.upper(), '%s'), _in_str % (settings_str.upper(), '%s')
trakt_collections_ins, trakt_watchlists_ins = _in_str % ('%s %s' % (trakt_str.upper(), coll_str.upper()), '%s'), _in_str % (trakt_watchlist_str.upper(), '%s')
discover_main_ins, premium_ins, furk_ins = _in_str % (discover_str.upper(), '%s'), _in_str % (ls(32488).upper(), '%s'), _in_str % (furk_str.upper(), '%s %s')
easynews_ins, real_debrid_ins, premiumize_ins = _in_str % (easy_str.upper(), '%s'), _in_str % (rd_str.upper(), '%s'), _in_str % (pm_str.upper(), '%s')
trakt_lists_ins, trakt_recommendations_ins = _in_str % (trakt_str.upper(), '%s'), _in_str % (rec_str.upper(), '%s')
favorites_ins, imdb_watchlists_ins = _in_str % (fav_str.upper(), '%s'), _in_str % (imdb_watchlist_str.upper(), '%s')
run_plugin, container_update, activate_window, log_path = 'RunPlugin(%s)', 'Container.Update(%s)', 'ActivateWindow(Videos,%s)', 'special://home/addons/%s/changelog.txt'
folder_info = (('folder1', ls(32110)), ('folder2', ls(32111)), ('folder3', ls(32112)), ('folder4', ls(32113)), ('folder5', ls(32114)))
mt_str = tp(log_path % 'plugin.video.david/resources/text')
kl_loc, klo_loc = tp('special://logpath/kodi.log'), tp('special://logpath/kodi.old.log')
get_icon, fanart = 'special://home/addons/plugin.video.david/resources/artwork/%s', tp('special://home/addons/plugin.video.david/fanart.png')
non_folder_items = ('get_search_term', 'build_popular_people')

class Navigator:
	def __init__(self, params):
		self.params = params
		self.params_get = self.params.get
		self.list_name = self.params_get('action', 'RootList')

	def main(self):
		add_items(int(sys.argv[1]), list(self._process_main_list(currently_used_list(self.list_name))))
		self._end_directory()

	def discover_main(self):
		self.AD({'mode': 'discover.movie', 'media_type': 'movie'}, discover_main_ins % mov_str, 'discover.png')
		self.AD({'mode': 'discover.tvshow', 'media_type': 'tvshow'}, discover_main_ins % tv_str, 'discover.png')
		self.AD({'mode': 'discover.history', 'media_type': 'movie'}, discover_main_ins % movh_str, 'discover.png')
		self.AD({'mode': 'discover.history', 'media_type': 'tvshow'}, discover_main_ins % tvh_str, 'discover.png')
		self.AD({'mode': 'discover.help'}, discover_main_ins % help_str, 'information.png', False)
		self._end_directory()

	def furk(self):
		self.AD({'mode': 'search_history', 'action': 'furk_video'}, furk_ins % (se_str, ''), 'search.png')
		self.AD({'mode': 'furk.my_furk_files', 'list_type': 'file_get_video'}, furk_ins % (vid_str, fl_str), 'furk.png')
		self.AD({'mode': 'furk.my_furk_files', 'list_type': 'file_get_active'}, furk_ins % (act_str, dl_str), 'furk.png')
		self.AD({'mode': 'furk.my_furk_files', 'list_type': 'file_get_failed'}, furk_ins % (fl_str, dl_str), 'furk.png')
		self.AD({'mode': 'furk.account_info'}, furk_ins % (acc_str, ''), 'furk.png', False)
		self._end_directory()

	def easynews(self):
		self.AD({'mode': 'search_history', 'action': 'easynews_video'}, easynews_ins % se_str, 'search.png')
		self.AD({'mode': 'easynews.account_info'}, easynews_ins % acc_str, 'easynews.png', False)
		self._end_directory()

	def real_debrid(self):
		self.AD({'mode': 'real_debrid.rd_torrent_cloud'}, real_debrid_ins % cloud_str, 'realdebrid.png')
		self.AD({'mode': 'real_debrid.rd_downloads'}, real_debrid_ins % history_str, 'realdebrid.png')
		self.AD({'mode': 'real_debrid.rd_account_info'}, real_debrid_ins % acc_str, 'realdebrid.png', False)
		self._end_directory()

	def premiumize(self):
		self.AD({'mode': 'premiumize.pm_torrent_cloud'}, premiumize_ins % cloud_str, 'premiumize.png')
		self.AD({'mode': 'premiumize.pm_transfers'}, premiumize_ins % history_str, 'premiumize.png')
		self.AD({'mode': 'premiumize.pm_account_info'}, premiumize_ins % acc_str, 'premiumize.png', False)
		self._end_directory()

	def alldebrid(self):
		self.AD({'mode': 'alldebrid.ad_torrent_cloud'}, alldebrid_ins % cloud_str, 'alldebrid.png')
		self.AD({'mode': 'alldebrid.ad_account_info'}, alldebrid_ins % acc_str, 'alldebrid.png', False)
		self._end_directory()

	def favorites(self):
		self.AD({'mode': 'build_movie_list', 'action': 'favorites_movies'}, favorites_ins % mov_str, 'movies.png')
		self.AD({'mode': 'build_tvshow_list', 'action': 'favorites_tvshows'}, favorites_ins % tv_str, 'tvshows.png')
		self._end_directory()

	def my_content(self):
		trakt_status, imdb_status = get_setting('trakt.user') not in ('', None), get_setting('imdb_user') not in ('', None)
		if trakt_status or imdb_status:
			if trakt_status:
				self.AD({'mode': 'navigator.trakt_collections'}, my_content_trakt_ins % coll_str, 'trakt.png')
				self.AD({'mode': 'navigator.trakt_watchlists'}, my_content_trakt_ins % wlist_str, 'trakt.png')
				self.AD({'mode': 'navigator.trakt_lists'}, my_content_trakt_ins % ls_str, 'trakt.png')
			if imdb_status:
				self.AD({'mode': 'navigator.imdb_watchlists'}, my_content_imdb_ins % wlist_str, 'imdb.png')
				self.AD({'mode': 'navigator.imdb_lists'}, my_content_imdb_ins % ls_str, 'imdb.png')
		else: notification(33022)
		self._end_directory()

	def trakt_collections(self):
		self.AD({'mode': 'build_movie_list', 'action': 'trakt_collection'}, trakt_collections_ins % mov_str, 'trakt.png')
		self.AD({'mode': 'build_tvshow_list', 'action': 'trakt_collection'}, trakt_collections_ins % tv_str, 'trakt.png')
		self.AD({'mode': 'build_movie_list', 'action': 'trakt_collection_lists', 'new_page': 'recent'}, trakt_collections_ins % mrec_str, 'trakt.png')
		self.AD({'mode': 'build_movie_list', 'action': 'trakt_collection_lists', 'new_page': 'random'}, trakt_collections_ins % mran_str, 'trakt.png')
		self.AD({'mode': 'build_tvshow_list', 'action': 'trakt_collection_lists', 'new_page': 'recent'}, trakt_collections_ins % tvrec_str, 'trakt.png')
		self.AD({'mode': 'build_tvshow_list', 'action': 'trakt_collection_lists', 'new_page': 'random'}, trakt_collections_ins % tvran_str, 'trakt.png')
		self.AD({'mode': 'build_my_calendar', 'recently_aired': 'true'}, trakt_collections_ins % ra_str, 'trakt.png')
		self._end_directory()

	def trakt_watchlists(self):
		self.AD({'mode': 'build_movie_list', 'action': 'trakt_watchlist'}, trakt_watchlists_ins % mov_str, 'trakt.png')
		self.AD({'mode': 'build_tvshow_list', 'action': 'trakt_watchlist'}, trakt_watchlists_ins % tv_str, 'trakt.png')
		self._end_directory()

	def trakt_lists(self):
		self.AD({'mode': 'trakt.list.get_trakt_lists', 'list_type': 'my_lists', 'build_list': 'true'}, trakt_lists_ins % ml_str, 'trakt.png')
		self.AD({'mode': 'trakt.list.get_trakt_lists', 'list_type': 'liked_lists', 'build_list': 'true'}, trakt_lists_ins % ll_str, 'trakt.png')
		self.AD({'mode': 'navigator.trakt_recommendations'}, trakt_lists_ins % rec_str, 'trakt.png')
		self.AD({'mode': 'build_my_calendar'}, trakt_lists_ins % cal_str, 'trakt.png')
		self.AD({'mode': 'trakt.list.get_trakt_trending_popular_lists', 'list_type': 'trending'}, trakt_lists_ins % tu_str, 'trakt.png')
		self.AD({'mode': 'trakt.list.get_trakt_trending_popular_lists', 'list_type': 'popular'}, trakt_lists_ins % pu_str, 'trakt.png')
		self.AD({'mode': 'trakt.list.search_trakt_lists'}, trakt_lists_ins % sea_str, 'trakt.png')
		self._end_directory()

	def trakt_recommendations(self):
		self.AD({'mode': 'build_movie_list', 'action': 'trakt_recommendations', 'new_page': 'movies'}, trakt_recommendations_ins % mov_str, 'trakt.png')
		self.AD({'mode': 'build_tvshow_list', 'action': 'trakt_recommendations', 'new_page': 'shows'}, trakt_recommendations_ins % tv_str, 'trakt.png')
		self._end_directory()

	def imdb_watchlists(self):
		self.AD({'mode': 'build_movie_list', 'action': 'imdb_watchlist'}, imdb_watchlists_ins % mov_str, 'imdb.png')
		self.AD({'mode': 'build_tvshow_list', 'action': 'imdb_watchlist'}, imdb_watchlists_ins % tv_str, 'imdb.png')
		self._end_directory()

	def imdb_lists(self):
		self.AD({'mode': 'imdb_build_user_lists', 'media_type': 'movie'}, imdb_lists_ins % mov_str, 'imdb.png')
		self.AD({'mode': 'imdb_build_user_lists', 'media_type': 'tvshow'}, imdb_lists_ins % tv_str, 'imdb.png')
		self._end_directory()

	def search(self):
		self.AD({'mode': 'search_history', 'action': 'movie'}, _in_str % (se_str.upper(), mov_str), 'search-movies.png')
		self.AD({'mode': 'search_history', 'action': 'tvshow'}, _in_str % (se_str.upper(), tv_str), 'search-tvshows.png')
		self.AD({'mode': 'search_history', 'action': 'people'}, _in_str % (se_str.upper(), people_str), 'search-people.png')
		self.AD({'mode': 'search_history', 'action': 'imdb_keyword_movie'}, _in_str % (se_str.upper(), kw_mov), 'search-imdb.png')
		self.AD({'mode': 'search_history', 'action': 'imdb_keyword_tvshow'}, _in_str % (se_str.upper(), kw_tv), 'search-imdb.png')
		self.AD({'mode': 'search_history', 'action': 'tmdb_collections'}, _in_str % (se_str.upper(), col_str), 'search-tmdb.png')
		self._end_directory()

	def downloads(self):
		self.AD({'mode': 'navigator.folder_navigator', 'folder_path': download_directory('movie')}, downloads_ins % mov_str, 'movies.png')
		self.AD({'mode': 'navigator.folder_navigator', 'folder_path': download_directory('episode')}, downloads_ins % tv_str, 'tvshows.png')
		self.AD({'mode': 'navigator.folder_navigator', 'folder_path': download_directory('tools')}, downloads_ins % premium_files_str, 'tools.png')
		self.AD({'mode': 'browser_image', 'folder_path': download_directory('image')}, downloads_ins % images_str, 'popular-people.png', False)
		self._end_directory()

	def tools(self):
		self.AD({'mode': 'open_settings'}, settings_ins % david_str, 'tools.png', False)
		self.AD({'mode': 'open_settings', 'addon': 'script.module.qscrapers'}, settings_ins % q_str, 'tools.png', False)
		self.AD({'mode': 'navigator.log_utils'}, tools_ins % changelog_log_viewer_str, 'tools.png')
		self.AD({'mode': 'navigator.tips'}, tools_ins % tips_use_str, 'tools.png')
		self.AD({'mode': 'navigator.set_view_modes'}, tools_ins % views_str, 'tools.png')
		self.AD({'mode': 'navigator.clear_info'}, tools_ins % cl_dbs_str, 'tools.png')
		self.AD({'mode': 'navigator.shortcut_folders'}, tools_ins % shortcut_manager_str, 'tools.png')
		self.AD({'mode': 'navigator.sources_folders'}, tools_ins % source_manager_str, 'tools.png')
		self.AD({'mode': 'toggle_language_invoker'}, tools_ins % langinv_str, 'tools.png', False)
		furk, easynews, debrids = furk_active(), easynews_active(), debrid_enabled()
		if furk: self.AD({'mode': 'navigator.furk'}, premium_ins % furk_str, 'furk.png')
		if easynews: self.AD({'mode': 'navigator.easynews'}, premium_ins % easy_str, 'easynews.png')
		if 'Real-Debrid' in debrids: self.AD({'mode': 'navigator.real_debrid'}, premium_ins % rd_str, 'realdebrid.png')
		if 'Premiumize.me' in debrids: self.AD({'mode': 'navigator.premiumize'}, premium_ins % pm_str, 'premiumize.png')
		if 'AllDebrid' in debrids: self.AD({'mode': 'navigator.alldebrid'}, premium_ins % ad_str, 'alldebrid.png')
		self._end_directory()

# 	def settings(self):
# 		self.AD({'mode': 'open_settings'}, settings_ins % david_str, 'tools.png', False)
# 		self.AD({'mode': 'open_settings', 'addon': 'script.module.qscrapers'}, settings_ins % q_str, 'tools.png', False)
# 		self._end_directory()

	def addon_updates(self):
		self._end_directory()

	def clear_info(self):
		self.AD({'mode': 'clean_settings'}, clean_all_str, 'tools.png', False)
		self.AD({'mode': 'clear_settings_window_properties'}, clean_set_cache_str, 'tools.png', False)
		self.AD({'mode': 'clean_databases'}, clear_info_ins % clean_databases_str, 'tools.png', False)
		self.AD({'mode': 'clear_all_cache'}, clear_all, 'tools.png', False)
		self.AD({'mode': 'clear_favorites'}, clear_info_ins % clear_fav_str, 'tools.png', False)
		self.AD({'mode': 'clear_search_history'}, clear_info_ins % clear_search_str, 'tools.png', False)
		self.AD({'mode': 'clear_cache', 'cache': 'meta'}, clear_info_ins % clear_meta_str, 'tools.png', False)
		self.AD({'mode': 'clear_cache', 'cache': 'list'}, clear_info_ins % clear_list_str, 'tools.png', False)
		self.AD({'mode': 'clear_cache', 'cache': 'trakt'}, clear_info_ins % clear_trakt_str, 'tools.png', False)
		self.AD({'mode': 'clear_cache', 'cache': 'imdb'}, clear_info_ins % clear_imdb_str, 'tools.png', False)
		self.AD({'mode': 'clear_cache', 'cache': 'internal_scrapers'}, clear_info_ins % clint_str, 'tools.png', False)
		self.AD({'mode': 'clear_cache', 'cache': 'external_scrapers'}, clear_info_ins % clext_str, 'tools.png', False)
		self.AD({'mode': 'clear_cache', 'cache': 'rd_cloud'}, clear_info_ins % clear_rd_str, 'tools.png', False)
		self.AD({'mode': 'clear_cache', 'cache': 'pm_cloud'}, clear_info_ins % clear_pm_str, 'tools.png', False)
		self.AD({'mode': 'clear_cache', 'cache': 'ad_cloud'}, clear_info_ins % clear_ad_str, 'tools.png', False)
		self._end_directory()

	def set_view_modes(self):
		self.AD({'mode': 'choose_view', 'view_type': 'view.main', 'content': ''},set_view_modes_ins % root_str, 'tools.png')
		self.AD({'mode': 'choose_view', 'view_type': 'view.movies', 'content': 'movies'},set_view_modes_ins % mov_str, 'tools.png', external=False)
		self.AD({'mode': 'choose_view', 'view_type': 'view.tvshows', 'content': 'tvshows'},set_view_modes_ins % tv_str, 'tools.png', external=False)
		self.AD({'mode': 'choose_view', 'view_type': 'view.seasons', 'content': 'seasons'},set_view_modes_ins % season_str, 'tools.png', external=False)
		self.AD({'mode': 'choose_view', 'view_type': 'view.episodes', 'content': 'episodes'},set_view_modes_ins % episodes_str, 'tools.png', external=False)
		self.AD({'mode': 'choose_view', 'view_type': 'view.episode_lists', 'content': 'episodes'},set_view_modes_ins % ep_lists_str, 'tools.png', external=False)
		self.AD({'mode': 'choose_view', 'view_type': 'view.tools', 'content': 'files'},set_view_modes_ins % premium_files_str, 'tools.png', external=False)
		self._end_directory()

	def log_utils(self):
		mh_str = '[B]%s[/B]: %s  [I](v.%s)[/I]' % (changelog_str.upper(), david_str, addon().getAddonInfo('version'))
		self.AD({'mode': 'show_text', 'heading': mh_str, 'file': mt_str}, mh_str, 'userlists.png', False, False)
		self.AD({'mode': 'show_text', 'heading': klv_h_str, 'file': kl_loc, 'kodi_log': 'true'}, klv_h_str, 'userlists.png', False, False)
		self.AD({'mode': 'show_text', 'heading': klvo_h_str, 'file': klo_loc, 'kodi_log': 'true'}, klvo_h_str, 'userlists.png', False, False)
		self.AD({'mode': 'upload_logfile'}, klu_h_str, 'userlists.png', False, False)
		self._end_directory()

	def certifications(self):
		if self.params_get('menu_type') == 'movie': mode, action, certifications = 'build_movie_list', 'tmdb_movies_certifications', ml.movie_certifications
		else: mode, action, certifications = 'build_tvshow_list', 'trakt_tv_certifications', ml.tvshow_certifications
		for cert in certifications: self.AD({'mode': mode, 'action': action, 'certification': cert}, cert.upper(), 'certifications.png')
		self._end_directory()

	def languages(self):
		mode, action = ('build_movie_list', 'tmdb_movies_languages') if self.params_get('menu_type') == 'movie' else ('build_tvshow_list', 'tmdb_tv_languages')
		for lang in ml.languages: self.AD({'mode': mode, 'action': action, 'language': lang[1]}, lang[0], 'languages.png')
		self._end_directory()

	def years(self):		
		if self.params_get('menu_type') == 'movie': mode, action, years = 'build_movie_list', 'tmdb_movies_year', ml.years_movies
		else: mode, action, years = 'build_tvshow_list', 'tmdb_tv_year', ml.years_tvshows
		for i in years: self.AD({'mode': mode, 'action': action, 'year': str(i)}, str(i), 'years.png')
		self._end_directory()

	def networks(self):
		for item in sorted(ml.networks, key=lambda k: k['name']):
			self.AD({'mode': 'build_tvshow_list', 'action': 'tmdb_tv_networks', 'network_id': item['id']}, item['name'], item['logo'])
		self._end_directory()

	def genres(self):
		menu_type = self.params_get('menu_type')
		if menu_type == 'movie': genre_list, mode, action = ml.movie_genres, 'build_movie_list', 'tmdb_movies_genres'
		else: genre_list, mode, action = ml.tvshow_genres, 'build_tvshow_list', 'tmdb_tv_genres'
		self.AD({'mode': 'navigator.multiselect_genres', 'genre_list': json.dumps(genre_list), 'menu_type': menu_type}, multi_str, 'genres.png', False, False)
		for genre, value in sorted(genre_list.items()): self.AD({'mode': mode, 'action': action, 'genre_id': value[0]}, genre, value[1])
		self._end_directory()

	def multiselect_genres(self):
		def _builder():
			for genre, value in sorted(genre_list.items()):
				function_list_append(value[0])
				#yield {'line1': genre, 'icon': get_icon(value[1])}
				yield {'line1': genre, 'icon': tp(''.join([get_icon, value[1]]))}
		menu_type, genre_list = self.params['menu_type'], self.params['genre_list']
		function_list = []
		function_list_append = function_list.append
		get_icon = 'special://home/addons/plugin.video.david/resources/artwork/'
		genre_list = json.loads(genre_list)
		list_items = list(_builder())
		kwargs = {'items': json.dumps(list_items), 'heading': genre_select_str, 'enumerate': 'false', 'multi_choice': 'true', 'multi_line': 'false'}
		genre_ids = k.select_dialog(function_list, **kwargs)
		if genre_ids == None: return
		genre_id = ','.join(genre_ids)
		if menu_type == 'movie': url = {'mode': 'build_movie_list', 'action': 'tmdb_movies_genres', 'genre_id': genre_id}
		else: url = {'mode': 'build_tvshow_list', 'action': 'tmdb_tv_genres', 'genre_id': genre_id}
		if external_browse():
			close_all_dialog()
			sleep(50)
			execute_builtin(activate_window % build_url(url))
		return execute_builtin(container_update % build_url(url))

	def folder_navigator(self):
		def _process():
			for info in results:
				try:
					path = info[0]
					url = os.path.join(folder_path, path)
					listitem = make_listitem()
					listitem.setLabel(clean_file_name(normalize(path)))
					listitem.setArt({'fanart': fanart})
					yield (url, listitem, info[1])
				except: pass
		handle = int(sys.argv[1])
		folder_path = self.params_get('folder_path')
		dirs, files = list_dirs(folder_path)
		results = [(i, True) for i in dirs] + [(i, False) for i in files]
		item_list = list(_process())
		add_items(handle, item_list)
		set_sort_method(handle, 'files')
		self._end_directory()
	
	def sources_folders(self):
		for item in folder_info:
			for media_type in ('movie', 'tvshow'):
				setting_id, default_name = item[0], item[1]
				folder_path = source_folders_directory(media_type, setting_id) or ''
				display_name = get_setting('%s.display_name' % setting_id)
				if display_name == 'None': display_name = ''
				if folder_path: folder_display, color = folder_path, 'green'
				else: folder_display, color = 'Not Set', 'red'
				display = sources_folders_str % (item[1].upper(), media_type.upper(), display_name.upper(), color, folder_display)
				self.AD({'mode': 'folder_scraper_manager_choice','setting_id': setting_id, 'media_type': media_type, 'folder_path': folder_path, 'display_name': display_name,
						'default_name': default_name}, display, 'folder.png', isFolder=False, external=False)
		self._end_directory()
	
	def shortcut_folders(self):
		def _make_icon(chosen_icon):
			return tp(get_icon % chosen_icon)
		def _make_new_item():
			icon = _make_icon('new.png')
			display_name = '[I]%s...[/I]' % ls(32702)
			url_params = {'mode': 'menu_editor.shortcut_folder_make'}
			url = build_url(url_params)
			listitem = make_listitem()
			listitem.setLabel(display_name)
			listitem.setArt({'icon': icon, 'poster': icon, 'thumb': icon, 'fanart': fanart, 'banner': icon})
			add_item(handle, url, listitem, False)
		def _builder():
			#short_str, delete_str = ls(32514), ls(32703)
			icon = tp(get_icon % 'folder.png')
			for i in folders:
				try:
					cm = []
					name = i[0]
					url_params = {'mode': 'navigator.build_shortcut_folder_list', 'name': name, 'iconImage': 'folder', 'shortcut_folder': 'True', 'external_list_item': 'True'}
					url = build_url(url_params)
					listitem = make_listitem()
					listitem.setLabel('[B]%s : [/B] %s ' % (short_str.upper(), i[0]))
					listitem.setArt({'icon': icon, 'poster': icon, 'thumb': icon, 'fanart': fanart, 'banner': icon})
					cm.append((delete_str, run_plugin % build_url({'mode': 'menu_editor.shortcut_folder_delete', 'list_name': name})))
					listitem.addContextMenuItems(cm)
					yield (url, listitem, True)
				except: pass
		handle = int(sys.argv[1])
		_make_new_item()
		folders = get_shortcut_folders()
		if folders: add_items(handle, list(_builder()))
		self._end_directory()
	
	def tips(self):
		tips_location = 'special://home/addons/plugin.video.david/resources/text/tips'
		files = sorted(list_dirs(tips_location)[1])
		tips_location = tips_location + '/%s'
		tips_list = []
		tips_append = tips_list.append
		for item in files:
			tip = item.replace('.txt', '')[4:]
			if '!!' in tip:
				if '!!HELP!!' in tip: tip, sort_order = tip.replace('!!HELP!!', '[COLOR crimson]%s!!![/COLOR] ' % help_str.upper()), 0
				elif '!!NEW!!' in tip: tip, sort_order = tip.replace('!!NEW!!', '[COLOR chartreuse]%s!![/COLOR] ' % new_str), 1
				else: tip, sort_order = tip.replace('!!SPOTLIGHT!!', '[COLOR orange]%s![/COLOR] ' % spot_str), 2
			else: sort_order = 3
			tip_name = tips_ins % tip
			action = {'mode': 'show_text', 'heading': tip, 'file': tp(tips_location % item)}
			tips_append((action, tip_name, sort_order))
		item_list = sorted(tips_list, key=lambda x: x[2])
		for c, i in enumerate(item_list, 1): self.AD(i[0], '[B]%02d. [/B]%s' % (c, i[1]), 'information.png', False, False)
		self._end_directory()

	def because_you_watched(self):
		media_type = self.params_get('menu_type')
		mode, action = ('build_movie_list', 'tmdb_movies_recommendations') if media_type == 'movie' else ('build_tvshow_list', 'tmdb_tv_recommendations')
		recently_watched = get_recently_watched(media_type, short_list=0)
		for item in recently_watched:
			if media_type == 'movie': name, tmdb_id = because_str % item['title'], item['media_id']
			else: name, tmdb_id = because_str % '%s - %sx%s' % (item['title'], str(item['season']), str(item['episode'])), item['media_ids']['tmdb']
			self.AD({'mode': mode, 'action': action, 'tmdb_id': tmdb_id}, name, 'because_you_watched', external=False)
		self._end_directory()
	
	def build_shortcut_folder_list(self):
		def _process():
			for item_position, item in enumerate(contents):
				try:
					cm = []
					is_folder = item['mode'] not in non_folder_items
					item_get = item.get
					name = item_get('name', 'Error: No Name')
					icon = item_get('iconImage') if item_get('network_id', '') != '' else tp(get_icon % item_get('iconImage'))
					url = build_url(item)
					cm.append((edit_str, run_plugin % build_url({'mode': 'menu_editor.edit_menu_shortcut_folder', 'active_list': list_name, 'position': item_position})))
					listitem = make_listitem()
					listitem.setLabel(name)
					listitem.setArt({'icon': icon, 'poster': icon, 'thumb': icon, 'fanart': fanart, 'banner': icon})
					listitem.addContextMenuItems(cm)
					yield (url, listitem, is_folder)
				except: pass
		handle = int(sys.argv[1])
		list_name = self.params_get('name')
		contents = get_shortcut_folder_contents(list_name)
		add_items(handle, list(_process()))
		self._end_directory()
	
	def _process_main_list(self, list_items):
		for item_position, item in enumerate(list_items):
			try:
				cm = []
				cm_append = cm.append
				item_get = item.get
				iconImage = item_get('iconImage')
				icon = iconImage if iconImage.startswith('http') else tp(get_icon % iconImage)
				cm_append((edit_str, run_plugin % build_url({'mode': 'menu_editor.edit_menu', 'active_list': self.list_name, 'position': item_position})))
				cm_append((browse_str, run_plugin % build_url({'mode': 'menu_editor.browse', 'active_list': self.list_name})))
				listitem = make_listitem()
				listitem.setLabel(ls(item_get('name', '')))
				listitem.setArt({'icon': icon, 'poster': icon, 'thumb': icon, 'fanart': fanart, 'banner': icon, 'landscape': icon})
				listitem.addContextMenuItems(cm)
				yield (build_url(item), listitem, item_get('mode', '') not in non_folder_items)
			except: pass

	def AD(self, url_params, list_name, iconImage='folder', isFolder=True, external=True):
		icon = iconImage if 'network_id' in url_params else tp(get_icon % iconImage)
		url_params['iconImage'] = icon
		url = build_url(url_params)
		listitem = make_listitem()
		listitem.setLabel(list_name)
		listitem.setArt({'icon': icon, 'poster': icon, 'thumb': icon, 'fanart': fanart, 'banner': icon, 'landscape': icon})
		if external:
			cm = []
			cm_append = cm.append
			cm_append((add_menu_str, run_plugin % build_url({'mode': 'menu_editor.add_external', 'name': list_name, 'iconImage': iconImage})))
			cm_append((s_folder_str, run_plugin % build_url({'mode': 'menu_editor.shortcut_folder_add_item', 'name': list_name, 'iconImage': iconImage})))
			listitem.addContextMenuItems(cm)
		add_item(int(sys.argv[1]), url, listitem, isFolder)

	def _end_directory(self):
		handle = int(sys.argv[1])
		set_content(handle, '')
		end_directory(handle)
		if not external_browse(): set_view_mode('view.main', '')

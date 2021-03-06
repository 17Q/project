# # -*- coding: utf-8 -*-
# from davidmeta.utils import logger

def movie_meta(id_type, media_id, user_info, hours=720):
    from davidmeta.build_meta import getMovieMeta
    return getMovieMeta(id_type, media_id, user_info, hours)

def tvshow_meta(id_type, media_id, user_info, hours=96):
    from davidmeta.build_meta import getTVShowMeta
    return getTVShowMeta(id_type, media_id, user_info, hours)

def all_episodes_meta(media_id, tvdb_id, seasons, tmdb_data, user_info, hours=24):
    from davidmeta.build_meta import getAllEpisodes
    return getAllEpisodes(media_id, tvdb_id, seasons, tmdb_data, user_info, hours)

def season_episodes_meta(media_id, tvdb_id, season, seasons, tmdb_data, user_info, all_episodes=False, hours=96):
    from davidmeta.build_meta import getSeasonEpisodes
    return getSeasonEpisodes(media_id, tvdb_id, season, seasons, tmdb_data, user_info, all_episodes, hours)

def delete_cache_item(db_type, id_type, media_id):
    from davidmeta.metacache import MetaCache
    return MetaCache().delete(db_type, id_type, media_id)

def use_animated_artwork():
    from davidmeta.utils import get_gif_data
    return get_gif_data()

def retrieve_user_info():
    from davidmeta.utils import user_info
    return user_info()

def choose_language():
    from davidmeta.utils import choose_language, open_settings
    success = choose_language()
    if success: delete_meta_cache(silent=True)
    open_settings('4.1')

def check_meta_database():
    from davidmeta.metacache import MetaCache
    MetaCache().check_database()

def delete_meta_cache(silent=False):
    try:
        if not silent:
            import xbmcgui
            if not xbmcgui.Dialog().yesno('Are you sure?','David Meta will Clear all Metadata.'): return False
        from davidmeta.metacache import MetaCache
        MetaCache().delete_all()
        return True
    except:
        return False

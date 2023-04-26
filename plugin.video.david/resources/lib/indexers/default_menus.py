# -*- coding: utf-8 -*-

root_list = [

			# MOVIES
			{'name': 'Movies',
			'iconImage': 'movies.png',
			'mode': 'navigator.main',
			'action': 'MovieList'},

			# TV SHOWS
			{'name': 'TV Shows',
			'iconImage': 'tvshows.png',
			'mode': 'navigator.main',
			'action': 'TVShowList'},

			# MY MOVIES TRAKT
			{'name': 'My Movies (Trakt)',
			'iconImage': 'mymovies.png',
			'mode': 'navigator.main',
			'action': 'MovieListTrakt'},

			# MY TV SHOWS TRAKT
			{'name': 'My TV Shows (Trakt)',
			'iconImage': 'mytvshows.png',
			'mode': 'navigator.main',
			'action': 'TVShowListTrakt'},

			### DISCOVER *** NEVER USE THIS THING, DELETE??? ***
			{'name': 'Discover',
			'iconImage': 'discover.png',
			'mode': 'navigator.discover_main'},

			### POPULAR PEOPLE *** NEVER USE THIS THING, DELETE??? ***
			{'name': 'Popular People',
			'iconImage': 'genres.png',
			'mode': 'build_popular_people'},

			### FAVORITES *** NEVER USE THIS THING, DELETE??? ***
			{'name': 'Favorites',
			'iconImage': 'favorites.png',
			'mode': 'navigator.favorites'},

 			### MY LISTS *** DELETE ***
# 			{'name': 'My Lists',
# 			'iconImage': 'lists',
# 			'mode': 'navigator.my_content'},

			# DOWNLOADS
			{'name': 'Downloads',
			'iconImage': 'downloads.png',
			'mode': 'navigator.downloads'},

			# MY SERVICES *** MOVED TO TOOLS ***
# 			{'name': 'My Services',
# 			'iconImage': 'premium.png',
# 			'mode': 'navigator.tools'},

			# SEARCH ADD MOVIE SEARCH TO MOVIES AND TV SEARCH TO TV SHOWS *** 
			{'name': 'Search',
			'iconImage': 'search.png',
			'mode': 'navigator.search'},

			# SETTINGS AND TOOLS
			{'name': 'Tools',
			'iconImage': 'tools.png',
			'mode': 'navigator.tools'}]


movie_list = [

			# MOVIES TRENDING
			{'name': 'Trending',
			'iconImage': 'trending.png',
			'mode': 'build_movie_list',
			'action': 'trakt_movies_trending'},

			# MOVIES POPULAR
			{'name': 'Popular',
			'iconImage': 'popular.png',
			'mode': 'build_movie_list',
			'action': 'tmdb_movies_popular'},

			# MOVIE PREMIERS
			{'name': 'Premiers',
			'action': 'tmdb_movies_premieres',
			'iconImage': 'premiers.png',
			'mode': 'build_movie_list'},

			# MOVIES LATEST RELEASES
			{'name': 'Latest Releases',
			'iconImage': 'latest-movies.png',
			'mode': 'build_movie_list',
			'action': 'tmdb_movies_latest_releases'},

			# MOVIES MOST WATCHED THIS WEEK
			{'name': 'Most Watched This Week',
			'iconImage': 'most-watched.png',
			'mode': 'build_movie_list',
			'action': 'trakt_movies_most_watched'},

			# MOVIES TOP 19 BOX OFFICE
			{'name': 'Top 10 Box Office',
			'action': 'trakt_movies_top10_boxoffice',
			'iconImage': 'box-office.png',
			'mode': 'build_movie_list'},

			# MOVIES BLOCKBUSTERS
			{'name': 'Blockbusters',
			'iconImage': 'most-voted.png',
			'mode': 'build_movie_list',
			'action': 'tmdb_movies_blockbusters'},

			# MOVIES IN THEATERS
			{'name': 'In Theaters',
			'iconImage': 'in-theaters.png',
			'mode': 'build_movie_list',
			'action': 'tmdb_movies_in_theaters'},

			# MOVIES UP COMING
			{'name': 'Up Coming',
			'iconImage': 'up-coming.png',
			'mode': 'build_movie_list',
			'action': 'tmdb_movies_upcoming'},

			# MOVIES OSCAR WINNERS
			{'name': 'Oscar Winners',
			'iconImage': 'oscar-winners.png',
			'mode': 'build_movie_list',
			'action': 'imdb_movies_oscar_winners'},

			# MOVIES GENRES
			{'name': 'Genres',
			'iconImage': 'genres.png',
			'mode': 'navigator.genres',
			'menu_type': 'movie'},

			# MOVIES LANGUAGES
			{'name': 'Languages',
			'iconImage': 'languages.png',
			'mode': 'navigator.languages',
			'menu_type': 'movie'},

			# MOVIES YEARS
			{'name': 'Years',
			'iconImage': 'years.png',
			'mode': 'navigator.years',
			'menu_type': 'movie'},

			# MOVIES CERTIFICATIONS
			{'name': 'Certifications',
			'iconImage': 'certifications.png',
			'mode': 'navigator.certifications',
			'menu_type': 'movie'},

			# MOVIES BECAUSE YOU WATCHED
			{'name': 'Because You Watched',
			'iconImage': 'because-you-watched.png',
			'mode': 'navigator.because_you_watched',
			'menu_type': 'movie'},

			# MOVIES WATCHED 
			{'name': 'Watched',
			'iconImage': 'watched.png',
			'mode': 'build_movie_list',
			'action': 'watched_movies'},

			# MOVIES RECENTLY WATCHED
			{'name': 'Recently Watched',
			'iconImage': 'because-you-watched.png',
			'mode': 'build_movie_list',
			'action': 'recent_watched_movies'},

			# MOVIES IN PROGRESS
			{'name': 'In Progress',
			'iconImage': 'in-progress-movies.png',
			'mode': 'build_movie_list',
			'action': 'in_progress_movies'}]
			
	
movie_list_trakt = [
			
			# MOVIES TRAKT COLLECTION
			{'name': 'Trakt: Collection',
			'action': 'trakt_collection',
			'iconImage': 'trakt.png',
			'mode': 'build_movie_list'},
			
			# MOVIES TRAKT WATCHLIST
			{'name': 'Trakt: Watchlist',
			'action': 'trakt_watchlist',
			'iconImage': 'trakt.png',
			'mode': 'build_movie_list'},
			
			# MOVIES TRAKT MY LISTS		
			{'name': 'Trakt: My Lists',
			'list_type': 'my_lists',
			'iconImage': 'trakt.png',
			'mode': 'trakt.list.get_trakt_lists'},
			
			# MOVIES TRAKT LIKED LISTS					
			{'name': 'Trakt: Liked Lists',
			'list_type': 'liked_lists',
			'iconImage': 'trakt.png',
			'mode': 'trakt.list.get_trakt_lists'},
			
			# MOVIES TRAKT RECOMMEMDED							
			{'name': 'Trakt: Recommended',
			'action': 'trakt_recommendations',
			'new_page': 'movies',
			'iconImage': 'trakt.png',
			'mode': 'build_movie_list'},
			
			# MOVIES TRAKT TRENDING USER LISTS								
			{'name': 'Trakt: Trending User Lists',
			'list_type': 'trending',
			'iconImage': 'trakt.png',
			'mode': 'trakt.list.get_trakt_trending_popular_lists'},
			
			# MOVIES TRAKT POPULAR USER LISTS								
			{'name': 'Trakt: Popular User Lists',
			'list_type': 'popular',
			'iconImage': 'trakt.png',
			'mode': 'trakt.list.get_trakt_trending_popular_lists'},	
			
			# MOVIES TRAKT SEARCH LISTS								
			{'name': 'Trakt: Search Lists',
			'action': 'trakt',
			'iconImage': 'trakt.png',
			'mode': 'trakt.list.search_trakt_lists'},
			
			# MOVIES IMDb WATCHLISTS *** FIX ***								
			{'name': 'IMDb: Watchlists',
			'action': 'imdb_watchlist',
			'iconImage': 'imdb.png',
			'mode': 'build_movie_list'},
			
			# MOVIES IMDb USER LISTS								
			{'name': 'IMDb: User Lists',
			'media_type': 'movie',
			'iconImage': 'imdb.png',
			'mode': 'imdb_build_user_lists'}]


tvshow_list = [

			# TV SHOWS TRENDING
			{'name': 'Trending',
			'action': 'trakt_tv_trending',
			'iconImage': 'trending.png',
			'mode': 'build_tvshow_list'},
			
			# TV SHOWS POPULAR
			{'name': 'Popular',
			'action': 'tmdb_tv_popular',
			'iconImage': 'popular.png',
			'mode': 'build_tvshow_list'},
			
			# TV SHOWS PREMIERES
			{'name': 'Premieres',
			'action': 'tmdb_tv_premieres',
			'iconImage': 'premiers.png',
			'mode': 'build_tvshow_list'},
			
			# TV SHOWS AIRING TODAY
			{'name': 'Airing Today',
			'action': 'tmdb_tv_airing_today',
			'iconImage': 'airing-today.png',
			'mode': 'build_tvshow_list'},
			
			# TV SHOWS ON THE AIR
			{'name': 'On the Air',
			'action': 'tmdb_tv_on_the_air',
			'iconImage': 'on-the-air.png',
			'mode': 'build_tvshow_list'},
			
			# TV SHOWS UP COMING
			{'name': 'Up Coming',
			'iconImage': 'up-coming.png',
			'mode': 'build_tvshow_list',
			'action': 'tmdb_tv_upcoming'},
			
			# TV SHOWS MOST WATCHED THIS WEEK
			{'name': 'Most Watched This Week',
			'iconImage': 'most-watched.png',
			'mode': 'build_tvshow_list',
			'action': 'trakt_tv_most_watched'},
			
			# TV SHOWS GENRES
			{'name': 'Genres',
			'iconImage': 'genres.png',
			'mode': 'navigator.genres',
			'menu_type': 'tvshow'},
			
			# TV SHOWS NETWORKS
			{'name': 'Networks',
			'iconImage': 'networks.png',
			'mode': 'navigator.networks',
			'menu_type': 'tvshow'},
			
			# TV SHOWS LANGUAGES
			{'name': 'Languages',
			'iconImage': 'languages.png',
			'mode': 'navigator.languages',
			'menu_type': 'tvshow'},
			
			# TV SHOWS YEARS
			{'name': 'Years',
			'iconImage': 'years.png',
			'mode': 'navigator.years',
			'menu_type': 'tvshow'},
			
			# TV SHOWS CERTIFICATIONS
			{'name': 'Certifications',
			'iconImage': 'certifications.png',
			'mode': 'navigator.certifications',
			'menu_type': 'tvshow'},
			
			# TV SHOWS BECAUSE YOU WATCHED
			{'name': 'Because You Watched',
			'iconImage': 'because-you-watched.png',
			'mode': 'navigator.because_you_watched',
			'menu_type': 'tvshow'},
			
			# TV SHOWS WATCHED
			{'name': 'Watched',
			'iconImage': 'watched.png',
			'mode': 'build_tvshow_list',
			'action': 'watched_tvshows'},
			
			# TV SHOWS IN PORGRESS TV SHOWS
			{'name': 'In Progress TV Shows',
			'action': 'in_progress_tvshows',
			'iconImage': 'in-progress-tvshows.png',
			'mode': 'build_tvshow_list'},
			
			# TV SHOWS NUMBER OF RATINGS
			{'name': 'Number of Ratings',
			'iconImage': 'watched.png',
			'mode': 'build_recently_watched_episode'},
			
			# TV SHOWS IN PROGRESS EPISODES
			{'name': 'In Progress Episodes',
			'iconImage': 'in-progress-episodes.png',
			'mode': 'build_in_progress_episode'},
			
			# TV SHOWS NEXT EPSODES
			{'name': 'Next Episodes',
			'iconImage': 'next-episodes.png',
			'mode': 'build_next_episode'}]
			
	
tvshow_list_trakt = [

			# TV SHOW TRAKT PROGRESS
			{'name': 'Trakt: Progress',
			#'action': 'next_episodes',
			'iconImage': 'trakt.png',
			'mode': 'build_next_episode'},

			# TV SHOW TRAKT COLLECTION
			{'name': 'Trakt: Collection',
			'action': 'trakt_collection',
			'iconImage': 'trakt.png',
			'mode': 'build_tvshow_list'},

			# TV SHOW TRAKT WATCHLIST
			{'name': 'Trakt: Watchlist',
			'action': 'trakt_watchlist',
			'iconImage': 'trakt.png',
			'mode': 'build_tvshow_list'},

			# TV SHOW TRAKT MY LISTS
			{'name': 'Trakt: My Lists',
			'list_type': 'my_lists',
			'iconImage': 'trakt.png',
			'mode': 'trakt.list.get_trakt_lists'},

			# TV SHOW TRAKT LIKED LISTS
			{'name': 'Trakt: Liked Lists',
			'list_type': 'liked_lists',
			'iconImage': 'trakt.png',
			'mode': 'trakt.list.get_trakt_lists'},

			# TVSHOW TRAKT RECOMMENDED
			{'name': 'Trakt: Recommended',
			'action': 'trakt_recommendations',
			'new_page': 'shows',
			'iconImage': 'trakt.png',
			'mode': 'build_tvshow_list'},

			# TV SHOWS TRAKT CALENDAR
			{'name': 'Trakt: Calendar',
			'action': 'recently_aired',
			'iconImage': 'trakt.png',
			'mode': 'build_my_calendar'},

			# TV SHOWS TRAKT TRENDING USER LISTS
			{'name': 'Trakt: Trending User Lists',
			'list_type': 'trending',
			'iconImage': 'trakt.png',
			'mode': 'trakt.list.get_trakt_trending_popular_lists'},

			# TV SHOWS TRAKT POPULAR USER LISTS
			{'name': 'Trakt: Popular User Lists',
			'list_type': 'popular',
			'iconImage': 'trakt.png',
			'mode': 'trakt.list.get_trakt_trending_popular_lists'},	

			# TV SHOWS TRAKT SEARCH LISTS
			{'name': 'Trakt: Search Lists',
			'action': 'trakt',
			'iconImage': 'trakt.png',
			'mode': 'trakt.list.search_trakt_lists'},

			# TV SHOWS IMDb WATCHLISTS *** FIX ***
			{'name': 'IMDb: Watchlists',
			'action': 'imdb_watchlist',
			'iconImage': 'imdb.png',
			'mode': 'build_tvshow_list'},

			# TV SHOWS IMDb USER LISTS
			{'name': 'IMDb: User Lists',
			'media_type': 'tvshow',
			'iconImage': 'imdb.png',
			'mode': 'imdb_build_user_lists'}]


default_menu_items = ('RootList', 'MovieList', 'TVShowList', 'MovieListTrakt', 'TVShowListTrakt')
main_menus = {'RootList': root_list, 'MovieList': movie_list, 'TVShowList': tvshow_list, 'MovieListTrakt': movie_list_trakt, 'TVShowListTrakt': tvshow_list_trakt}
main_menu_items = {'RootList': {'name': 'root', 'iconImage': 'david.png', 'mode': 'navigator.main', 'action': 'RootList'},
					'MovieList': root_list[0],
					'TVShowList': root_list[1],
					'MovieListTrakt': root_list[2],
					'TVShowListTrakt': root_list[3]}



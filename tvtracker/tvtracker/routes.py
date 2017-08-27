def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('view_show', '/shows/{show_id}')
    config.add_route('login', '/login')
    config.add_route('watchlist', '/watchlist')
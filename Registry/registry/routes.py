def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('login', '/login')
    config.add_route('history', '/history')
    config.add_route('aboutme', '/aboutme')
    config.add_route('registration', '/registration')

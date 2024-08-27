from flask import request, session, g

# Dictionary mapping languages to flag emojis
supported_languages = {
    'en': '🇺🇸',
    'fr': '🇫🇷',
    'zh': '🇹🇼',  # 正體字
    'es': '🇪🇸',
    'de': '🇩🇪',
    'sw': '🇰🇪',
    'vi': '🇻🇳',
    'tl': '🇵🇭',
    'th': '🇹🇭',
}

def get_locale():
    if 'lang' in request.args:
        lang = request.args.get('lang')
        if lang in supported_languages:
            session['lang'] = lang
            return session['lang']
    elif 'lang' in session:
        return session.get('lang')
    return request.accept_languages.best_match(supported_languages.keys())

def get_timezone():
    user = getattr(g, 'user', None)
    if user is not None:
        return user.timezone

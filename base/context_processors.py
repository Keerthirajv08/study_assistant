def theme_context(request):
    """Make theme data available to all templates"""
    return {
        'current_theme': request.session.get('theme', 'light'),
        'is_dark': request.session.get('theme', 'light') == 'dark',
    }